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
        sub_conditions = self._split_conditions_detailed(condition)
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
        # 完全なMC/DCカバレッジのため、適切な組み合わせを生成
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
            # MC/DCカバレッジを満たすテストケースを生成
            truth_combinations = self._generate_mcdc_for_mixed_condition(condition, sub_conditions)

        return truth_combinations if truth_combinations else [(condition, ["T", "F"])]

    def _generate_mcdc_for_mixed_condition(self, condition: str, sub_conditions: List[str]) -> List[Tuple[str, List[str]]]:
        """
        ANDとORが混在する複雑な条件式のMC/DCテストケースを生成する

        A && (B1 || B2 || ... || Bn) && C のような構造を検出して、MC/DCカバレッジを満たす
        テストケースを生成する。

        Args:
            condition: 元の条件式
            sub_conditions: 分割された条件のリスト

        Returns:
            (条件式, 真偽値リスト) のタプルのリスト
        """
        num_conditions = len(sub_conditions)
        truth_combinations = []

        # 条件式の構造を解析
        # 最も外側の&&で分割してOR部分を検出
        and_parts = self._split_by_and(condition)

        if len(and_parts) >= 2:
            # A && B && C のような構造
            # OR条件を含む部分を検出
            or_groups = []
            single_conditions = []

            for part in and_parts:
                if '||' in part:
                    # OR条件を含む部分
                    or_conditions = self._split_by_or(part)
                    or_groups.append(or_conditions)
                else:
                    # 単一条件
                    single_conditions.append(part)

            # MC/DCテストケースを生成
            if or_groups:
                # A && (B1 || B2 || ... || Bn) && C のケース
                # 基本ケース: 最初のOR条件のみ真、他のOR条件は偽、AND条件は真
                base_case = []
                current_idx = 0

                for i, part in enumerate(and_parts):
                    if '||' not in part:
                        # 単一AND条件は真に
                        base_case.append('T')
                        current_idx += 1
                    else:
                        # OR条件の最初だけ真に、残りは偽
                        or_count = part.count('||') + 1
                        base_case.append('T')  # 最初のOR条件のみT
                        for _ in range(or_count - 1):
                            base_case.append('F')  # 残りのOR条件はF
                        current_idx += or_count

                truth_combinations.append((condition, [''.join(base_case)]))

                # 各AND条件の独立性をテスト
                # 単一AND条件の位置を記録（最初のAND条件のみ）
                and_condition_indices = []
                current_idx = 0

                for i, part in enumerate(and_parts):
                    if '||' not in part:
                        # 単一AND条件の位置を記録
                        and_condition_indices.append((i, current_idx))
                        current_idx += 1
                    else:
                        # OR条件グループをスキップ
                        or_count = part.count('||') + 1
                        current_idx += or_count

                # 最初のAND条件を偽にするテストケース（通常は最初のAND条件）
                if and_condition_indices:
                    first_and_idx = and_condition_indices[0][1]
                    test_case = base_case.copy()
                    test_case[first_and_idx] = 'F'
                    truth_combinations.append((condition, [''.join(test_case)]))

                # OR条件の独立性をテスト
                # 全てのOR条件を偽にする（OR全体が偽になる）
                or_false_case = []
                current_idx = 0
                for part in and_parts:
                    if '||' in part:
                        or_count = part.count('||') + 1
                        # 全てのOR条件を偽に
                        for j in range(or_count):
                            or_false_case.append('F')
                        current_idx += or_count
                    else:
                        # AND条件は真に
                        or_false_case.append('T')
                        current_idx += 1
                truth_combinations.append((condition, [''.join(or_false_case)]))

                # 残りのAND条件を偽にするテストケース（2番目以降）
                for part_idx, idx in and_condition_indices[1:]:
                    test_case = base_case.copy()
                    test_case[idx] = 'F'
                    truth_combinations.append((condition, [''.join(test_case)]))

                # 各OR条件（2番目以降）を真にするテストケース
                # まず、各ANDパートの開始インデックスを記録
                and_part_indices = []
                current_idx = 0
                for part in and_parts:
                    and_part_indices.append(current_idx)
                    if '||' in part:
                        or_count = part.count('||') + 1
                        current_idx += or_count
                    else:
                        current_idx += 1

                # OR条件グループを探して、各OR条件（2番目以降）を真にする
                for part_idx, part in enumerate(and_parts):
                    if '||' in part:
                        or_count = part.count('||') + 1
                        or_start_idx = and_part_indices[part_idx]

                        # 2番目以降のOR条件を個別に真にする
                        for j in range(1, or_count):
                            test_case = []
                            for p_idx, p in enumerate(and_parts):
                                p_start_idx = and_part_indices[p_idx]

                                if '||' not in p:
                                    # 単一AND条件は真に
                                    test_case.append('T')
                                else:
                                    # OR条件グループ
                                    oc = p.count('||') + 1
                                    if p_idx == part_idx:
                                        # このOR条件グループ: j番目のみ真、残りは偽
                                        for k in range(oc):
                                            if k == j:
                                                test_case.append('T')
                                            else:
                                                test_case.append('F')
                                    else:
                                        # 他のOR条件グループ: 最初のみ真、残りは偽
                                        test_case.append('T')
                                        for k in range(1, oc):
                                            test_case.append('F')

                            truth_combinations.append((condition, [''.join(test_case)]))
            else:
                # OR条件がない場合は通常のAND処理
                truth_combinations.append((condition, ['T' * num_conditions]))
                for i in range(num_conditions):
                    truth_value = ['T'] * num_conditions
                    truth_value[i] = 'F'
                    truth_combinations.append((condition, [''.join(truth_value)]))
        else:
            # 単純な構造の場合は全組み合わせ
            truth_values = list(product(['T', 'F'], repeat=num_conditions))
            for tv in truth_values:
                truth_combinations.append((condition, [''.join(tv)]))

        return truth_combinations

    def _split_by_and(self, condition: str) -> List[str]:
        """
        条件式を最も外側の&&で分割する

        Args:
            condition: 条件式

        Returns:
            分割された条件のリスト
        """
        # 括弧の深さを追跡しながら&&で分割
        parts = []
        current_part = ""
        depth = 0
        i = 0

        while i < len(condition):
            char = condition[i]

            if char == '(':
                depth += 1
                current_part += char
            elif char == ')':
                depth -= 1
                current_part += char
            elif char == '&' and i + 1 < len(condition) and condition[i + 1] == '&' and depth == 0:
                # 最も外側の&&を見つけた
                if current_part.strip():
                    parts.append(current_part.strip())
                current_part = ""
                i += 1  # &&の2文字目をスキップ
            else:
                current_part += char

            i += 1

        if current_part.strip():
            parts.append(current_part.strip())

        return parts

    def _split_by_or(self, condition: str) -> List[str]:
        """
        条件式を最も外側の||で分割する（括弧を除去）

        Args:
            condition: 条件式

        Returns:
            分割された条件のリスト
        """
        # 外側の括弧を除去
        condition = condition.strip()
        if condition.startswith('(') and condition.endswith(')'):
            # 対応する括弧かチェック
            depth = 0
            for i, char in enumerate(condition):
                if char == '(':
                    depth += 1
                elif char == ')':
                    depth -= 1
                if depth == 0 and i == len(condition) - 1:
                    condition = condition[1:-1].strip()
                    break

        # 括弧の深さを追跡しながら||で分割
        parts = []
        current_part = ""
        depth = 0
        i = 0

        while i < len(condition):
            char = condition[i]

            if char == '(':
                depth += 1
                current_part += char
            elif char == ')':
                depth -= 1
                current_part += char
            elif char == '|' and i + 1 < len(condition) and condition[i + 1] == '|' and depth == 0:
                # 最も外側の||を見つけた
                if current_part.strip():
                    parts.append(current_part.strip())
                current_part = ""
                i += 1  # ||の2文字目をスキップ
            else:
                current_part += char

            i += 1

        if current_part.strip():
            parts.append(current_part.strip())

        return parts

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

    def _split_conditions_detailed(self, condition: str) -> List[str]:
        """
        複合条件式を詳細に個別の条件に分割する（ネスト構造対応）

        例: "(Utx104.Utm11.Utm14 == UtD27) && ((UtD39 == 1) || (UtD39 == 2)) && (UtD38 == 0)"
             -> ["Utx104.Utm11.Utm14 == UtD27", "UtD39 == 1", "UtD39 == 2", "UtD38 == 0"]
        """
        conditions = []

        # ANDで最上位レベルを分割
        and_parts = self._split_by_and(condition)

        for part in and_parts:
            # 各部分がOR条件を含むかチェック
            if '||' in part:
                # OR条件を分割
                or_conditions = self._split_by_or(part)
                for or_cond in or_conditions:
                    # 括弧を除去して追加
                    clean_cond = or_cond.strip()
                    if clean_cond.startswith('(') and clean_cond.endswith(')'):
                        clean_cond = clean_cond[1:-1].strip()
                    conditions.append(clean_cond)
            else:
                # 単一条件（括弧を除去）
                clean_cond = part.strip()
                if clean_cond.startswith('(') and clean_cond.endswith(')'):
                    clean_cond = clean_cond[1:-1].strip()
                conditions.append(clean_cond)

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
