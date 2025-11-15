#!/usr/bin/env python3
"""
Unity単体テストコード生成器
真偽表からUnityフレームワークの単体テストコードを生成する
"""

import re
import subprocess
from typing import List, Dict, Set
from datetime import datetime
from mcdc_analyzer import TruthTable, TestCase
from c_parser import FunctionInfo

# バージョン情報
VERSION = "1.0.0"

def get_git_revision():
    """Gitリビジョン情報を取得する"""
    try:
        result = subprocess.run(
            ['git', 'rev-parse', '--short', 'HEAD'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return "unknown"
    except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
        return "unknown"


class UnityTestGenerator:
    """Unity単体テストコード生成器クラス"""

    def __init__(self, function_info: FunctionInfo, truth_table: TruthTable):
        self.function_info = function_info
        self.truth_table = truth_table
        self.mock_functions: Set[str] = set()
        self.stub_functions: Set[str] = set()
        self.extracted_functions: Set[str] = set()

    def _extract_function_calls(self, condition: str) -> List[str]:
        """
        条件式から関数呼び出しを抽出する

        例: "(f4() & 0xdf) != 0" -> ["f4"]
        """
        # 関数呼び出しパターン: 関数名(引数)
        pattern = r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\('
        matches = re.findall(pattern, condition)

        # 予約語を除外
        keywords = {'if', 'while', 'for', 'switch', 'sizeof', 'return'}
        functions = [m for m in matches if m not in keywords]

        return functions

    def _generate_mock_function(self, func_name: str) -> str:
        """
        モック関数を生成する
        呼び出し回数カウント機能付き
        """
        code_lines = []

        # 呼び出し回数カウンタ
        code_lines.append(f"static uint32_t mock_{func_name}_call_count = 0;")
        code_lines.append(f"static int16_t mock_{func_name}_return_value = 0;")
        code_lines.append("")

        # モック関数本体（簡易版: int16_t返却を仮定）
        code_lines.append(f"static int16_t {func_name}(void)")
        code_lines.append("{")
        code_lines.append(f"    mock_{func_name}_call_count++;")
        code_lines.append(f"    return mock_{func_name}_return_value;")
        code_lines.append("}")
        code_lines.append("")

        return '\n'.join(code_lines)

    def _generate_stub_function(self, func_name: str) -> str:
        """
        スタブ関数を生成する
        呼び出し回数カウント機能付き
        """
        code_lines = []

        # 呼び出し回数カウンタ
        code_lines.append(f"static uint32_t stub_{func_name}_call_count = 0;")
        code_lines.append("")

        # スタブ関数本体（簡易版: void返却を仮定）
        code_lines.append(f"static void {func_name}(void)")
        code_lines.append("{")
        code_lines.append(f"    stub_{func_name}_call_count++;")
        code_lines.append("}")
        code_lines.append("")

        return '\n'.join(code_lines)

    def _sanitize_test_name(self, condition: str) -> str:
        """
        条件式からテスト名用の文字列を生成する

        例: "(mx63 == m47) || (mx63 == m46)" -> "mx63_eq_m47_or_mx63_eq_m46"
        """
        # 記号を単語に変換
        name = condition
        name = re.sub(r'==', '_eq_', name)
        name = re.sub(r'!=', '_ne_', name)
        name = re.sub(r'<=', '_le_', name)
        name = re.sub(r'>=', '_ge_', name)
        name = re.sub(r'<', '_lt_', name)
        name = re.sub(r'>', '_gt_', name)
        name = re.sub(r'\|\|', '_or_', name)
        name = re.sub(r'&&', '_and_', name)
        name = re.sub(r'[^a-zA-Z0-9_]', '_', name)
        name = re.sub(r'_+', '_', name)
        name = name.strip('_')

        # 最大長を制限（60文字）
        if len(name) > 60:
            name = name[:60]

        return name

    def _generate_test_function(self, test_case: TestCase) -> str:
        """
        1つのテストケース用のテスト関数を生成する
        """
        code_lines = []

        # テスト名を生成
        condition_name = self._sanitize_test_name(test_case.condition_expression)
        test_name = f"test_{test_case.test_number:02d}_{condition_name}_{test_case.truth_values}"

        # テスト関数のヘッダーコメント
        code_lines.append(f"// Test No.{test_case.test_number}")
        code_lines.append(f"// 対象分岐: if ({test_case.condition_expression})")
        code_lines.append(f"// 真偽値: {test_case.truth_values}")

        # 真偽値の詳細を解説
        sub_conditions = self._split_condition(test_case.condition_expression)
        if len(test_case.truth_values) == len(sub_conditions):
            for i, (cond, truth) in enumerate(zip(sub_conditions, test_case.truth_values)):
                code_lines.append(f"// {cond.strip():<50} :{truth}")

        code_lines.append(f"// 期待動作: {test_case.expected_result if test_case.expected_result else 'TODO: 期待動作を記載'}")
        code_lines.append(f"static void {test_name}(void)")
        code_lines.append("{")

        # テスト本体
        code_lines.append("    // TODO: Setup test conditions")
        code_lines.append("")

        # 関数呼び出しを抽出してモック/スタブの初期化
        functions = self._extract_function_calls(test_case.condition_expression)
        for func in functions:
            if func in self.mock_functions:
                code_lines.append(f"    // Reset mock: {func}")
                code_lines.append(f"    mock_{func}_call_count = 0;")
                code_lines.append(f"    mock_{func}_return_value = 0; // TODO: Set appropriate value")
            elif func in self.stub_functions:
                code_lines.append(f"    // Reset stub: {func}")
                code_lines.append(f"    stub_{func}_call_count = 0;")

        if functions:
            code_lines.append("")

        # テスト対象関数の呼び出し
        code_lines.append(f"    // Execute test target function")
        code_lines.append(f"    {self.function_info.name}();")
        code_lines.append("")

        # アサーション
        code_lines.append("    // Assertions")
        for func in functions:
            if func in self.mock_functions:
                code_lines.append(f"    TEST_ASSERT_EQUAL(1, mock_{func}_call_count); // TODO: Set expected count")
            elif func in self.stub_functions:
                code_lines.append(f"    TEST_ASSERT_EQUAL(1, stub_{func}_call_count); // TODO: Set expected count")

        code_lines.append("    // TODO: Add more assertions")

        code_lines.append("}")
        code_lines.append("")

        return '\n'.join(code_lines)

    def _split_condition(self, condition: str) -> List[str]:
        """
        複合条件を個別条件に分割する（MC/DCアナライザーと同じロジック）
        """
        # 括弧で囲まれた条件を抽出
        paren_pattern = r'\([^()]+\)'
        matches = re.findall(paren_pattern, condition)

        if matches:
            return matches

        # 論理演算子で分割
        parts = re.split(r'\s*(\|\||&&)\s*', condition)
        conditions = [p.strip() for p in parts if p.strip() and p not in ['||', '&&']]

        return conditions if conditions else [condition]

    def generate_test_code(self) -> str:
        """
        完全なUnity単体テストコードを生成する
        """
        code_lines = []

        # リビジョン情報を取得
        revision = get_git_revision()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # ヘッダー
        code_lines.append("/*")
        code_lines.append(f" * Unity Unit Test for {self.function_info.name}")
        code_lines.append(" * Auto-generated by C Unit Test Generator")
        code_lines.append(f" * Version: {VERSION} | Revision: {revision}")
        code_lines.append(f" * Generated: {timestamp}")
        code_lines.append(" */")
        code_lines.append("")
        code_lines.append("#include \"unity.h\"")
        code_lines.append("#include <stdint.h>")
        code_lines.append("#include <stdbool.h>")
        code_lines.append("")

        # 全ての条件式から関数呼び出しを抽出
        all_functions = set()
        for test_case in self.truth_table.test_cases:
            functions = self._extract_function_calls(test_case.condition_expression)
            all_functions.update(functions)

        # モックとスタブに分類（簡易版: 全てモックとして扱う）
        self.mock_functions = all_functions

        # プロトタイプ宣言セクション
        code_lines.append("/* ============================================")
        code_lines.append(" * Function Prototypes")
        code_lines.append(" * ============================================ */")
        code_lines.append("")

        # テスト関数のプロトタイプ宣言
        code_lines.append("// Test functions")
        for test_case in self.truth_table.test_cases:
            condition_name = self._sanitize_test_name(test_case.condition_expression)
            test_name = f"test_{test_case.test_number:02d}_{condition_name}_{test_case.truth_values}"
            code_lines.append(f"static void {test_name}(void);")
        code_lines.append("")

        # モック関数の宣言
        if self.mock_functions:
            code_lines.append("// Mock functions")
            for func in sorted(self.mock_functions):
                code_lines.append(f"static int16_t {func}(void); // TODO: Adjust return type")
            code_lines.append("")

        # スタブ関数の宣言
        if self.stub_functions:
            code_lines.append("// Stub functions")
            for func in sorted(self.stub_functions):
                code_lines.append(f"static void {func}(void); // TODO: Adjust signature")
            code_lines.append("")

        # テスト対象関数の宣言
        code_lines.append("// Test target function")
        code_lines.append(f"static void {self.function_info.name}(void); // TODO: Adjust signature")
        code_lines.append("")

        # setUp/tearDown
        code_lines.append("/* ============================================")
        code_lines.append(" * Unity Setup and Teardown")
        code_lines.append(" * ============================================ */")
        code_lines.append("")
        code_lines.append("void setUp(void)")
        code_lines.append("{")
        code_lines.append("    // Initialize test environment")
        code_lines.append("}")
        code_lines.append("")
        code_lines.append("void tearDown(void)")
        code_lines.append("{")
        code_lines.append("    // Cleanup test environment")
        code_lines.append("}")
        code_lines.append("")

        # モック/スタブ関数の実装
        code_lines.append("/* ============================================")
        code_lines.append(" * Mock/Stub Functions")
        code_lines.append(" * ============================================ */")
        code_lines.append("")

        for func in sorted(self.mock_functions):
            code_lines.append(self._generate_mock_function(func))

        for func in sorted(self.stub_functions):
            code_lines.append(self._generate_stub_function(func))

        # テスト関数の実装
        code_lines.append("/* ============================================")
        code_lines.append(" * Test Functions")
        code_lines.append(" * ============================================ */")
        code_lines.append("")

        for test_case in self.truth_table.test_cases:
            code_lines.append(self._generate_test_function(test_case))

        # テスト対象関数（元のソースから貼り付け用のプレースホルダー）
        code_lines.append("/* ============================================")
        code_lines.append(" * Test Target Function")
        code_lines.append(" * (Copy from original source file)")
        code_lines.append(" * ============================================ */")
        code_lines.append("")
        code_lines.append(f"// TODO: Copy the implementation of {self.function_info.name}() here")
        code_lines.append("")

        return '\n'.join(code_lines)

    def save_to_file(self, output_path: str):
        """
        テストコードをファイルに保存する
        """
        test_code = self.generate_test_code()

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(test_code)

        print(f"Unity test code saved to: {output_path}")


def main():
    """テスト用メイン関数"""
    from c_parser import FunctionInfo, IfStatement
    from mcdc_analyzer import TruthTable, TestCase

    # テスト用のダミーデータ
    func_info = FunctionInfo(
        name="Utf1",
        return_type="static void",
        parameters=["void"],
        body_start_line=1921,
        body_end_line=2042
    )

    truth_table = TruthTable(function_name="Utf1")
    truth_table.test_cases = [
        TestCase(1, "(f4() & 0xdf) != 0", "T", "v9が7"),
        TestCase(2, "(f4() & 0xdf) != 0", "F", "v9!=7"),
        TestCase(3, "(mx63 == m47) || (mx63 == m46)", "TF", ""),
        TestCase(4, "(mx63 == m47) || (mx63 == m46)", "FT", ""),
    ]

    # テストコード生成
    generator = UnityTestGenerator(func_info, truth_table)
    generator.save_to_file("test_Utf1.c")
    print("Test code generated successfully!")


if __name__ == "__main__":
    main()
