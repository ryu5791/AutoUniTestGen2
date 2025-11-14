#!/usr/bin/env python3
"""
Excel真偽表生成器
MC/DC真偽表をExcelファイルとして出力する
"""

from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from openpyxl.utils import get_column_letter
from typing import List
from mcdc_analyzer import TruthTable, TestCase


class TruthTableExcelGenerator:
    """Excel真偽表生成器クラス"""

    def __init__(self):
        self.workbook = None

    def create_truth_table_excel(self, truth_table: TruthTable, output_path: str):
        """
        真偽表をExcelファイルとして生成する

        Args:
            truth_table: TruthTable オブジェクト
            output_path: 出力ファイルパス
        """
        self.workbook = Workbook()
        ws = self.workbook.active
        ws.title = "Truth Table"

        # スタイル定義
        header_font = Font(bold=True, size=11)
        header_fill = PatternFill(start_color="CCCCCC", end_color="CCCCCC", fill_type="solid")
        border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )
        center_alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        left_alignment = Alignment(horizontal='left', vertical='center', wrap_text=True)

        # ヘッダー行
        headers = ["No.", "真偽", "判定文", "期待値"]
        for col_num, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col_num)
            cell.value = header
            cell.font = header_font
            cell.fill = header_fill
            cell.border = border
            cell.alignment = center_alignment

        # 列幅を設定
        ws.column_dimensions['A'].width = 8   # No.
        ws.column_dimensions['B'].width = 10  # 真偽
        ws.column_dimensions['C'].width = 60  # 判定文
        ws.column_dimensions['D'].width = 20  # 期待値

        # データ行
        for row_num, test_case in enumerate(truth_table.test_cases, 2):
            # No.
            cell = ws.cell(row=row_num, column=1)
            cell.value = test_case.test_number
            cell.border = border
            cell.alignment = center_alignment

            # 真偽
            cell = ws.cell(row=row_num, column=2)
            cell.value = test_case.truth_values
            cell.border = border
            cell.alignment = center_alignment

            # 判定文
            cell = ws.cell(row=row_num, column=3)
            cell.value = f"if ({test_case.condition_expression})"
            cell.border = border
            cell.alignment = left_alignment

            # 期待値（空欄）
            cell = ws.cell(row=row_num, column=4)
            cell.value = test_case.expected_result
            cell.border = border
            cell.alignment = center_alignment

        # 行の高さを自動調整
        for row in ws.iter_rows(min_row=2, max_row=len(truth_table.test_cases) + 1):
            ws.row_dimensions[row[0].row].height = 30

        # 保存
        self.workbook.save(output_path)
        print(f"Truth table saved to: {output_path}")

    def create_multiple_truth_tables(self, truth_tables: List[TruthTable], output_path: str):
        """
        複数の真偽表を1つのExcelファイル（複数シート）として生成する

        Args:
            truth_tables: TruthTable オブジェクトのリスト
            output_path: 出力ファイルパス
        """
        self.workbook = Workbook()
        # デフォルトシートを削除
        if 'Sheet' in self.workbook.sheetnames:
            del self.workbook['Sheet']

        for truth_table in truth_tables:
            self._create_sheet_for_truth_table(truth_table)

        # 保存
        self.workbook.save(output_path)
        print(f"Truth tables (all functions) saved to: {output_path}")

    def _create_sheet_for_truth_table(self, truth_table: TruthTable):
        """
        1つの真偽表用のシートを作成する
        """
        # シート名を関数名にする（Excelの制限に合わせて31文字まで）
        sheet_name = truth_table.function_name[:31]
        ws = self.workbook.create_sheet(title=sheet_name)

        # スタイル定義
        header_font = Font(bold=True, size=11)
        header_fill = PatternFill(start_color="CCCCCC", end_color="CCCCCC", fill_type="solid")
        border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )
        center_alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        left_alignment = Alignment(horizontal='left', vertical='center', wrap_text=True)

        # ヘッダー行
        headers = ["No.", "真偽", "判定文", "期待値"]
        for col_num, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col_num)
            cell.value = header
            cell.font = header_font
            cell.fill = header_fill
            cell.border = border
            cell.alignment = center_alignment

        # 列幅を設定
        ws.column_dimensions['A'].width = 8
        ws.column_dimensions['B'].width = 10
        ws.column_dimensions['C'].width = 60
        ws.column_dimensions['D'].width = 20

        # データ行
        for row_num, test_case in enumerate(truth_table.test_cases, 2):
            # No.
            cell = ws.cell(row=row_num, column=1)
            cell.value = test_case.test_number
            cell.border = border
            cell.alignment = center_alignment

            # 真偽
            cell = ws.cell(row=row_num, column=2)
            cell.value = test_case.truth_values
            cell.border = border
            cell.alignment = center_alignment

            # 判定文
            cell = ws.cell(row=row_num, column=3)
            cell.value = f"if ({test_case.condition_expression})"
            cell.border = border
            cell.alignment = left_alignment

            # 期待値
            cell = ws.cell(row=row_num, column=4)
            cell.value = test_case.expected_result
            cell.border = border
            cell.alignment = center_alignment

        # 行の高さ
        for row in ws.iter_rows(min_row=2, max_row=len(truth_table.test_cases) + 1):
            ws.row_dimensions[row[0].row].height = 30


def main():
    """テスト用メイン関数"""
    from mcdc_analyzer import MCDCAnalyzer, TestCase, TruthTable

    # テスト用の真偽表を作成
    truth_table = TruthTable(function_name="Utf1")

    test_cases = [
        TestCase(1, "(f4() & 0xdf) != 0", "T", "v9が7"),
        TestCase(2, "(f4() & 0xdf) != 0", "F", "v9!=7"),
        TestCase(3, "(mx63 == m47) || (mx63 == m46)", "TF", ""),
        TestCase(4, "(mx63 == m47) || (mx63 == m46)", "FT", ""),
        TestCase(5, "(mx63 == m47) || (mx63 == m46)", "FF", ""),
    ]

    truth_table.test_cases = test_cases

    # Excelファイル生成
    generator = TruthTableExcelGenerator()
    generator.create_truth_table_excel(truth_table, "test_truth_table.xlsx")
    print("Test Excel file created successfully!")


if __name__ == "__main__":
    main()
