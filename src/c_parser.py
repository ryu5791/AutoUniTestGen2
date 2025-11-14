#!/usr/bin/env python3
"""
C言語パーサー
C言語ファイルを解析してif文、switch文を抽出する
"""

import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class Condition:
    """条件式を表すクラス"""
    expression: str  # 条件式の文字列
    line_number: int  # 行番号
    parent_conditions: List[str] = field(default_factory=list)  # 親のif条件（ネスト構造用）


@dataclass
class IfStatement:
    """if文を表すクラス"""
    condition: str
    line_number: int
    full_expression: str  # 完全な式
    has_else: bool = False
    has_elif: bool = False
    nested_level: int = 0  # ネストレベル


@dataclass
class SwitchStatement:
    """switch文を表すクラス"""
    variable: str
    line_number: int
    cases: List[str] = field(default_factory=list)
    has_default: bool = False
    nested_level: int = 0


@dataclass
class FunctionInfo:
    """関数情報を表すクラス"""
    name: str
    return_type: str
    parameters: List[str]
    body_start_line: int
    body_end_line: int
    if_statements: List[IfStatement] = field(default_factory=list)
    switch_statements: List[SwitchStatement] = field(default_factory=list)


class CParser:
    """C言語パーサークラス"""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.content = ""
        self.lines = []
        self.functions: List[FunctionInfo] = []

    def load_file(self):
        """ファイルを読み込む"""
        with open(self.file_path, 'r', encoding='utf-8') as f:
            self.content = f.read()
            self.lines = self.content.split('\n')

    def preprocess_content(self) -> str:
        """
        プリプロセス: コメントを除去、マクロを簡略化
        """
        # 単一行コメントを除去
        content = re.sub(r'//.*?$', '', self.content, flags=re.MULTILINE)
        # 複数行コメントを除去
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        return content

    def extract_functions(self) -> List[FunctionInfo]:
        """
        関数を抽出する
        簡易的な関数抽出ロジック
        """
        content = self.preprocess_content()
        functions = []

        # 関数パターン: static void Utf1(void) のような形式
        # より柔軟なパターンマッチング
        function_pattern = r'((?:static|extern|inline)?\s*\w+\s+\*?\s*\w+\s*\([^)]*\))\s*\{'

        for match in re.finditer(function_pattern, content):
            func_signature = match.group(1).strip()
            func_start = match.start()

            # 行番号を計算
            line_number = content[:func_start].count('\n') + 1

            # 関数名を抽出
            name_match = re.search(r'(\w+)\s*\(', func_signature)
            if name_match:
                func_name = name_match.group(1)
            else:
                continue

            # 戻り値の型を抽出
            return_type_match = re.match(r'((?:static|extern|inline)?\s*\w+(?:\s+\w+)*)\s+\*?\s*\w+\s*\(', func_signature)
            return_type = return_type_match.group(1).strip() if return_type_match else ""

            # パラメータを抽出
            params_match = re.search(r'\((.*?)\)', func_signature)
            parameters = [p.strip() for p in params_match.group(1).split(',') if p.strip()] if params_match else []

            # 関数の終わりを見つける（対応する閉じ括弧）
            brace_count = 1
            body_start = match.end()
            i = body_start

            while i < len(content) and brace_count > 0:
                if content[i] == '{':
                    brace_count += 1
                elif content[i] == '}':
                    brace_count -= 1
                i += 1

            body_end = i
            body_end_line = content[:body_end].count('\n') + 1

            func_info = FunctionInfo(
                name=func_name,
                return_type=return_type,
                parameters=parameters,
                body_start_line=line_number,
                body_end_line=body_end_line
            )

            # 関数本体からif文とswitch文を抽出
            function_body = content[body_start:body_end]
            func_info.if_statements = self.extract_if_statements(function_body, line_number)
            func_info.switch_statements = self.extract_switch_statements(function_body, line_number)

            functions.append(func_info)

        self.functions = functions
        return functions

    def extract_if_statements(self, code: str, start_line: int) -> List[IfStatement]:
        """
        if文を抽出する
        """
        if_statements = []

        # if文のパターン（より厳密に）
        # if (condition) のパターンをマッチ
        pattern = r'\bif\s*\(([^)]+(?:\([^)]*\)[^)]*)*)\)'

        for match in re.finditer(pattern, code):
            condition = match.group(1).strip()

            # 行番号を計算
            offset = match.start()
            line_number = start_line + code[:offset].count('\n')

            # ネストレベルを計算（簡易版）
            nested_level = self._calculate_nested_level(code, offset)

            if_stmt = IfStatement(
                condition=condition,
                line_number=line_number,
                full_expression=condition,
                nested_level=nested_level
            )

            if_statements.append(if_stmt)

        return if_statements

    def extract_switch_statements(self, code: str, start_line: int) -> List[SwitchStatement]:
        """
        switch文を抽出する
        """
        switch_statements = []

        # switch文のパターン
        pattern = r'\bswitch\s*\(([^)]+)\)\s*\{'

        for match in re.finditer(pattern, code):
            variable = match.group(1).strip()

            # 行番号を計算
            offset = match.start()
            line_number = start_line + code[:offset].count('\n')

            # switch文の本体を抽出
            switch_start = match.end()
            brace_count = 1
            i = switch_start

            while i < len(code) and brace_count > 0:
                if code[i] == '{':
                    brace_count += 1
                elif code[i] == '}':
                    brace_count -= 1
                i += 1

            switch_body = code[switch_start:i]

            # caseラベルを抽出
            cases = []
            case_pattern = r'\bcase\s+([^:]+):'
            for case_match in re.finditer(case_pattern, switch_body):
                cases.append(case_match.group(1).strip())

            # defaultがあるか確認
            has_default = bool(re.search(r'\bdefault\s*:', switch_body))

            nested_level = self._calculate_nested_level(code, offset)

            switch_stmt = SwitchStatement(
                variable=variable,
                line_number=line_number,
                cases=cases,
                has_default=has_default,
                nested_level=nested_level
            )

            switch_statements.append(switch_stmt)

        return switch_statements

    def _calculate_nested_level(self, code: str, position: int) -> int:
        """
        指定位置のネストレベルを計算する
        """
        # 現在位置までの開き括弧と閉じ括弧の数で判定
        level = 0
        for i in range(position):
            if code[i] == '{':
                level += 1
            elif code[i] == '}':
                level -= 1
        return max(0, level - 1)  # 関数本体の括弧を除く

    def parse(self) -> List[FunctionInfo]:
        """
        ファイルをパースして関数情報を返す
        """
        self.load_file()
        return self.extract_functions()

    def find_function_by_name(self, func_name: str) -> Optional[FunctionInfo]:
        """
        関数名で関数情報を検索する
        """
        for func in self.functions:
            if func.name == func_name:
                return func
        return None


def main():
    """テスト用メイン関数"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python c_parser.py <c_file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    parser = CParser(file_path)
    functions = parser.parse()

    print(f"Found {len(functions)} functions:")
    for func in functions:
        print(f"\nFunction: {func.name}")
        print(f"  Return type: {func.return_type}")
        print(f"  Parameters: {func.parameters}")
        print(f"  Lines: {func.body_start_line}-{func.body_end_line}")
        print(f"  If statements: {len(func.if_statements)}")
        print(f"  Switch statements: {len(func.switch_statements)}")

        if func.if_statements:
            print(f"\n  If conditions:")
            for i, if_stmt in enumerate(func.if_statements, 1):
                print(f"    {i}. Line {if_stmt.line_number}: {if_stmt.condition}")


if __name__ == "__main__":
    main()
