#!/usr/bin/env python3
"""
MC/DC解析エンジン
条件式からMC/DC 100%カバレッジのテストケースを生成する
"""

import re
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass, field
from itertools import product


@dataclass
class Condition:
    """単一条件を表すクラス"""
    expression: str
    variable_name: str = ""  # 変数名（比較式の場合）


@dataclass
class TestCase:
    """テストケースを表すクラス"""
    test_number: int
    condition_expression: str  # 元の条件式
    truth_values: str  # 真偽値 (例: "TF", "T", "FF")
    expected_result: str = ""  # 期待される結果


@dataclass
class TruthTable:
    """真偽表を表すクラス"""
    function_name: str
    test_cases: List[TestCase] = field(default_factory=list)


class MCDCAnalyzer:
    """MC/DC解析エンジン"""

    def __init__(self):
        self.truth_tables: List[TruthTable] = []

    def analyze_condition(self, condition: str) -> List[Tuple[str, List[str]]]:
        """
        条件式を解析してMC/DCテストケースを生成する

        Args:
            condition: 条件式の文字列

        Returns:
            (条件式, 真偽値リスト) のタプルのリスト
        """
        # 論理演算子の有無をチェック
        has_or = '||' in condition
        has_and = '&&' in condition

        if has_or or has_and:
            # 複合条件式の場合
            return self._analyze_compound_condition(condition)
        else:
            # 単純条件式の場合
            return [(condition, ["T", "F"])]

    def _analyze_compound_condition(self, condition: str) -> List[Tuple[str, List[str]]]:
        """
        複合条件式（&&や||を含む）を解析してMC/DCテストケースを生成する

        MC/DC (Modified Condition/Decision Coverage) の要件:
        - 各条件が独立して結果に影響を与えることを示す
        - 全ての条件の真偽の組み合わせを網羅する必要はないが、
          各条件が結果に影響を与える組み合わせをテストする
        """
        # 条件を分割
        sub_conditions = self._split_conditions(condition)
        num_conditions = len(sub_conditions)

        # 2つの条件を持つ複合式の場合（最も一般的）
        if num_conditions == 2:
            if '||' in condition:
                # OR条件の場合: TF, FT, FF
                return [
                    (condition, ["TF"]),  # 左がTrue、右がFalse → True
                    (condition, ["FT"]),  # 左がFalse、右がTrue → True
                    (condition, ["FF"]),  # 両方False → False
                ]
            elif '&&' in condition:
                # AND条件の場合: TT, TF, FT
                return [
                    (condition, ["TT"]),  # 両方True → True
                    (condition, ["TF"]),  # 左がTrue、右がFalse → False
                    (condition, ["FT"]),  # 左がFalse、右がTrue → False
                ]

        # 3つ以上の条件を持つ場合（複雑な式）
        # 完全なMC/DCカバレッジのため、全ての組み合わせを生成
        truth_combinations = []

        if '||' in condition and '&&' not in condition:
            # 全てORの場合
            # 少なくとも1つがTrueになるケースと、全てFalseのケースをテスト
            # 各条件が独立して結果に影響することを示す
            for i in range(num_conditions):
                # i番目だけTrue、他はFalse
                truth_value = ['F'] * num_conditions
                truth_value[i] = 'T'
                truth_combinations.append((condition, [''.join(truth_value)]))
            # 全てFalse
            truth_combinations.append((condition, ['F' * num_conditions]))

        elif '&&' in condition and '||' not in condition:
            # 全てANDの場合
            # 全てTrueのケースと、各条件が独立してFalseになるケースをテスト
            # 全てTrue
            truth_combinations.append((condition, ['T' * num_conditions]))
            # 各条件が独立してFalseになるケース
            for i in range(num_conditions):
                # i番目だけFalse、他はTrue
                truth_value = ['T'] * num_conditions
                truth_value[i] = 'F'
                truth_combinations.append((condition, [''.join(truth_value)]))

        else:
            # ANDとORが混在する場合（最も複雑）
            # 完全な真偽表を生成
            truth_values = list(product(['T', 'F'], repeat=num_conditions))
            for tv in truth_values:
                truth_combinations.append((condition, [''.join(tv)]))

        return truth_combinations if truth_combinations else [(condition, ["T", "F"])]

    def _split_conditions(self, condition: str) -> List[str]:
        """
        複合条件式を個別の条件に分割する

        例: "(a == b) || (c != d)" -> ["(a == b)", "(c != d)"]
        """
        # まず、括弧で囲まれた条件を抽出
        conditions = []

        # パターン1: 括弧で囲まれた条件
        paren_pattern = r'\([^()]+\)'
        matches = re.findall(paren_pattern, condition)

        if matches:
            return matches

        # パターン2: 論理演算子で分割
        # ||または&&で分割（ただし括弧内は除く）
        parts = re.split(r'\s*(\|\||&&)\s*', condition)

        # 論理演算子を除外して条件だけを抽出
        conditions = [p.strip() for p in parts if p.strip() and p not in ['||', '&&']]

        return conditions if conditions else [condition]

    def generate_truth_table(self, function_name: str, if_statements: List) -> TruthTable:
        """
        関数のif文から真偽表を生成する

        Args:
            function_name: 関数名
            if_statements: IfStatementのリスト

        Returns:
            TruthTable オブジェクト
        """
        truth_table = TruthTable(function_name=function_name)
        test_number = 1

        for if_stmt in if_statements:
            condition = if_stmt.condition

            # 条件を解析してテストケースを生成
            test_cases_data = self.analyze_condition(condition)

            for cond, truth_values_list in test_cases_data:
                for truth_values in truth_values_list:
                    test_case = TestCase(
                        test_number=test_number,
                        condition_expression=cond,
                        truth_values=truth_values,
                        expected_result=""  # 後で手動で設定
                    )
                    truth_table.test_cases.append(test_case)
                    test_number += 1

        self.truth_tables.append(truth_table)
        return truth_table

    def format_truth_table_text(self, truth_table: TruthTable) -> str:
        """
        真偽表をテキスト形式でフォーマットする（デバッグ用）
        """
        lines = []
        lines.append(f"Function: {truth_table.function_name}")
        lines.append("-" * 80)
        lines.append(f"{'No.':<5} | {'Truth':<6} | {'Condition':<50} | {'Expected':<10}")
        lines.append("-" * 80)

        for tc in truth_table.test_cases:
            lines.append(
                f"{tc.test_number:<5} | {tc.truth_values:<6} | "
                f"{tc.condition_expression:<50} | {tc.expected_result:<10}"
            )

        lines.append("-" * 80)
        return '\n'.join(lines)


def main():
    """テスト用メイン関数"""
    # テスト用の条件式
    test_conditions = [
        "(f4() & 0xdf) != 0",
        "(mx63 == m47) || (mx63 == m46)",
        "(mx63 == m48) || (mx63 == mx2)",
        "((a > 10) && (b < 20)) || (c == 30)",
        "v10 > 30",
    ]

    analyzer = MCDCAnalyzer()

    print("MC/DC Test Case Generation")
    print("=" * 80)

    for cond in test_conditions:
        print(f"\nCondition: {cond}")
        print("-" * 80)

        test_cases = analyzer.analyze_condition(cond)

        for i, (condition, truth_values_list) in enumerate(test_cases, 1):
            for truth_values in truth_values_list:
                print(f"  Test {i}: {truth_values} - {condition}")


if __name__ == "__main__":
    main()
