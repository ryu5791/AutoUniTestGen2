#!/usr/bin/env python3
"""
MC/DC解析エンジンのテスト
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from mcdc_analyzer import MCDCAnalyzer

# ユーザーが指摘した条件式
test_condition = "(Utx104.Utm11.Utm14 == UtD27) && ((UtD39 == 1) || (UtD39 == 2) || (UtD39 == 3) || (UtD39 == 6) || (UtD39 == 7) || (UtD39 == 8)) && (UtD38 == 0)"

analyzer = MCDCAnalyzer()

print("テスト対象条件式:")
print(test_condition)
print()

# 条件を分割してみる
detailed_conditions = analyzer._split_conditions_detailed(test_condition)
print(f"分割された条件 ({len(detailed_conditions)}個):")
for i, cond in enumerate(detailed_conditions, 1):
    print(f"  {i}. {cond}")
print()

# MC/DCテストケースを生成
test_cases = analyzer.analyze_condition(test_condition)

print(f"生成されたテストケース ({len(test_cases)}個):")
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
