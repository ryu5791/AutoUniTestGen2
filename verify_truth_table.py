#!/usr/bin/env python3
"""
特定のif文の真偽表を確認するスクリプト
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from c_parser import CParser
from mcdc_analyzer import MCDCAnalyzer

# ファイルをパース
parser = CParser("test/22_obfuscated.c")
functions = parser.parse()

# Utf1関数を見つける
utf1 = None
for func in functions:
    if func.name == "Utf1":
        utf1 = func
        break

if not utf1:
    print("Utf1関数が見つかりませんでした")
    sys.exit(1)

print(f"Utf1関数のif文数: {len(utf1.if_statements)}")
print()

# 6番目の条件式を詳細に表示
print("6番目の条件式の詳細:")
if len(utf1.if_statements) >= 6:
    print(utf1.if_statements[5].condition)
print()

# 特定の条件式を見つける
target_condition = None
for i, if_stmt in enumerate(utf1.if_statements):
    # 条件式を正規化（スペースと改行を除去）して比較
    normalized = if_stmt.condition.replace('\n', ' ').replace('\t', ' ')
    normalized = ' '.join(normalized.split())

    if "Utx104.Utm11.Utm14 == UtD27" in normalized and "UtD39 == 1" in normalized:
        print(f"条件式#{i+1}を発見:")
        print(f"  {normalized}")
        print()
        target_condition = normalized
        break

if target_condition:
    # MC/DC解析
    analyzer = MCDCAnalyzer()
    test_cases = analyzer.analyze_condition(target_condition)

    print("生成されたテストケース:")
    for i, (cond, truth_values_list) in enumerate(test_cases, 1):
        for truth_values in truth_values_list:
            print(f"  {i}. {truth_values}")

    print()
    print("期待される真偽表:")
    expected = [
        "TTFFFFFT",
        "FTFFFFFT",
        "TFFFFFFT",
        "TTFFFFFF",
        "TFTFFFFT",
        "TFFTFFFT",
        "TFFFTFFT",
        "TFFFFTFT",
        "TFFFFFTT"
    ]
    for i, tv in enumerate(expected, 1):
        print(f"  {i}. {tv}")

    print()

    # 検証
    actual = [truth_values_list[0] for cond, truth_values_list in test_cases]
    if actual == expected:
        print("✓ 真偽表が期待通りに生成されました！")
    else:
        print("✗ 真偽表が期待と異なります")
else:
    print("対象の条件式が見つかりませんでした")
