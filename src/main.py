#!/usr/bin/env python3
"""
C言語単体テスト自動生成ツール メインスクリプト

使用方法:
    python main.py <c_file> [options]

例:
    python main.py test.c --function Utf1 --output-dir ./output
"""

import sys
import os
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

# 同じディレクトリのモジュールをインポート
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from c_parser import CParser
from mcdc_analyzer import MCDCAnalyzer
from truth_table_excel import TruthTableExcelGenerator
from unity_test_generator import UnityTestGenerator
from io_table_excel import IOTableExcelGenerator

# バージョン情報
VERSION = "1.0.0"

def get_git_revision():
    """Gitリビジョン情報を取得する"""
    try:
        # カレントディレクトリを取得
        script_dir = os.path.dirname(os.path.abspath(__file__))
        repo_dir = os.path.dirname(script_dir)

        # git rev-parseでコミットハッシュを取得
        result = subprocess.run(
            ['git', 'rev-parse', '--short', 'HEAD'],
            cwd=repo_dir,
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0:
            commit_hash = result.stdout.strip()

            # ブランチ名を取得
            branch_result = subprocess.run(
                ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                cwd=repo_dir,
                capture_output=True,
                text=True,
                timeout=5
            )

            branch = branch_result.stdout.strip() if branch_result.returncode == 0 else "unknown"

            return f"{commit_hash} ({branch})"
        else:
            return "unknown"
    except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
        return "unknown"


class CUnitTestGenerator:
    """C言語単体テスト自動生成ツール メインクラス"""

    def __init__(self, c_file_path: str, output_dir: str = None, function_name: str = None):
        self.c_file_path = c_file_path
        self.output_dir = output_dir or "./output"
        self.target_function_name = function_name
        self.parser = None
        self.analyzer = None

    def run(self):
        """メイン処理を実行"""
        # リビジョン情報を取得
        revision = get_git_revision()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print("=" * 80)
        print("C言語単体テスト自動生成ツール")
        print(f"Version: {VERSION} | Revision: {revision}")
        print(f"Generated: {timestamp}")
        print("=" * 80)
        print()

        # 出力ディレクトリを作成
        os.makedirs(self.output_dir, exist_ok=True)

        # ステップ1: C言語ファイルをパース
        print("[Step 1] C言語ファイルをパース中...")
        self.parser = CParser(self.c_file_path)
        functions = self.parser.parse()
        print(f"  → {len(functions)} 個の関数を検出しました")

        if not functions:
            print("エラー: 関数が見つかりませんでした")
            return

        # 対象関数を選択
        if self.target_function_name:
            target_function = self.parser.find_function_by_name(self.target_function_name)
            if not target_function:
                print(f"エラー: 関数 '{self.target_function_name}' が見つかりませんでした")
                return
            target_functions = [target_function]
        else:
            # 全ての関数を対象にする
            target_functions = functions

        print(f"  → 対象関数: {', '.join([f.name for f in target_functions])}")
        print()

        # 各関数に対して処理を実行
        self.analyzer = MCDCAnalyzer()

        for func in target_functions:
            print(f"[関数: {func.name}]")
            print("-" * 80)

            # ステップ2: MC/DC真偽表を生成
            print("[Step 2] MC/DC真偽表を生成中...")
            if not func.if_statements:
                print(f"  → 警告: 関数 '{func.name}' にif文が見つかりませんでした")
                continue

            truth_table = self.analyzer.generate_truth_table(func.name, func.if_statements)
            print(f"  → {len(truth_table.test_cases)} 個のテストケースを生成しました")
            print()

            # ステップ3: Excel真偽表を出力
            print("[Step 3] Excel真偽表を出力中...")
            truth_table_path = os.path.join(self.output_dir, f"{func.name}_truth_table.xlsx")
            excel_generator = TruthTableExcelGenerator()
            excel_generator.create_truth_table_excel(truth_table, truth_table_path)
            print()

            # ステップ4: Unityテストコードを生成
            print("[Step 4] Unityテストコードを生成中...")
            test_code_path = os.path.join(self.output_dir, f"test_{func.name}.c")
            test_generator = UnityTestGenerator(func, truth_table)
            test_generator.save_to_file(test_code_path)
            print()

            # ステップ5: Input/Output一覧表を生成
            print("[Step 5] Input/Output一覧表を生成中...")
            io_table_path = os.path.join(self.output_dir, f"{func.name}_io_table.xlsx")
            io_generator = IOTableExcelGenerator()
            io_generator.create_io_table_excel(truth_table, io_table_path)
            print()

        print("=" * 80)
        print("処理が完了しました！")
        print(f"出力ディレクトリ: {os.path.abspath(self.output_dir)}")
        print("=" * 80)
        print()
        print("生成されたファイル:")
        for func in target_functions:
            if func.if_statements:
                print(f"  - {func.name}_truth_table.xlsx  : 真偽表")
                print(f"  - test_{func.name}.c           : Unityテストコード")
                print(f"  - {func.name}_io_table.xlsx    : Input/Output一覧表")
                print()

        print("次のステップ:")
        print("  1. Excel真偽表を確認し、期待値を入力してください")
        print("  2. Unityテストコードを確認し、TODOコメントを埋めてください")
        print("  3. Input/Output一覧表を確認し、入出力値を記入してください")
        print("  4. テスト対象関数の実装をテストコードにコピーしてください")
        print()


def main():
    """CLIエントリーポイント"""
    parser = argparse.ArgumentParser(
        description="C言語単体テスト自動生成ツール - MC/DC 100%カバレッジの真偽表とUnityテストコードを生成します",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # 単一の関数に対してテストを生成
  python main.py test.c --function Utf1 --output-dir ./output

  # ファイル内の全ての関数に対してテストを生成
  python main.py test.c --output-dir ./output

  # カレントディレクトリに出力
  python main.py test.c --function Utf1
        """
    )

    parser.add_argument(
        'c_file',
        help='テスト対象のCソースファイルのパス'
    )

    parser.add_argument(
        '-f', '--function',
        dest='function_name',
        help='テスト対象の関数名（指定しない場合は全ての関数が対象）'
    )

    parser.add_argument(
        '-o', '--output-dir',
        dest='output_dir',
        default='./output',
        help='出力ディレクトリのパス（デフォルト: ./output）'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='詳細な出力を表示'
    )

    args = parser.parse_args()

    # ファイルの存在確認
    if not os.path.exists(args.c_file):
        print(f"エラー: ファイル '{args.c_file}' が見つかりません")
        sys.exit(1)

    # ツールを実行
    try:
        tool = CUnitTestGenerator(
            c_file_path=args.c_file,
            output_dir=args.output_dir,
            function_name=args.function_name
        )
        tool.run()

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
