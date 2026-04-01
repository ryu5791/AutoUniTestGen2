import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "WBS"

# ---- Colors ----
def fill(hex_color):
    return PatternFill(start_color=hex_color, end_color=hex_color, fill_type="solid")

HEADER_BG   = fill("D9E1F2")
GRAY_ROW    = fill("F2F2F2")
TODAY_COL   = fill("FFF2CC")
BLUE_BAR    = fill("4472C4")   # 一柳
GREEN_BAR   = fill("70AD47")   # 木口
PINK_BAR    = fill("FF9999")   # 富養

# ---- Date columns (weekdays only) ----
# index: 0=3/31, 1=4/1, 2=4/2, 3=4/3, 4=4/6, 5=4/7, 6=4/8, 7=4/9, 8=4/10,
#        9=4/13, 10=4/14, 11=4/15, 12=4/16, 13=4/17
dates = [
    ("3/31","火"),("4/1","水"),("4/2","木"),("4/3","金"),
    ("4/6","月"),("4/7","火"),("4/8","水"),("4/9","木"),("4/10","金"),
    ("4/13","月"),("4/14","火"),("4/15","水"),("4/16","木"),("4/17","金"),
]
TODAY_IDX = 2   # 4/2

FIXED_COLS = 5   # タスク/備考/見積/進捗率/担当

# ---- Column widths ----
ws.column_dimensions["A"].width = 28
ws.column_dimensions["B"].width = 22
ws.column_dimensions["C"].width = 7
ws.column_dimensions["D"].width = 8
ws.column_dimensions["E"].width = 6
for i in range(len(dates)):
    ws.column_dimensions[get_column_letter(FIXED_COLS + 1 + i)].width = 4.2

# ---- Helper: border ----
thin = Side(style="thin", color="BFBFBF")
med  = Side(style="medium", color="000000")

def thin_border():
    return Border(left=thin, right=thin, top=thin, bottom=thin)

def red_lr_border(left=False, right=False):
    red = Side(style="medium", color="FF0000")
    return Border(
        left=red if left else thin,
        right=red if right else thin,
        top=thin, bottom=thin
    )

# ---- Header row ----
headers = ["タスク", "備考", "見積(h)", "進捗率\n(%)", "担当"]
for col, h in enumerate(headers, 1):
    c = ws.cell(row=1, column=col, value=h)
    c.font = Font(bold=True, size=9)
    c.fill = HEADER_BG
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    c.border = thin_border()

for i, (date, day) in enumerate(dates):
    col = FIXED_COLS + 1 + i
    c = ws.cell(row=1, column=col, value=f"{date}\n({day})")
    c.font = Font(bold=True, size=8)
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    if i == TODAY_IDX:
        c.fill = fill("FFE699")
    else:
        c.fill = HEADER_BG
    if i == TODAY_IDX:
        c.border = Border(left=med, right=med, top=med, bottom=thin)
    else:
        c.border = thin_border()

ws.row_dimensions[1].height = 32

# ---- Task data ----
# (task, notes, est_h, progress, assignee, [(bar_start, bar_end, bar_fill), ...])
# bar indices are 0-based into the dates list
tasks = [
    ("見積、計画",          "",                                      "",  100, "一柳", []),
    ("git登録(IO-A10)",    "",                                      "",  100, "富養", []),
    ("ポート設定",          "HDSをベースに変更",                      "",  100, "木口", []),
    ("EMC向け　割込み設定、設計", "",                                 "",   70, "一柳", [(0, 2, BLUE_BAR)]),
    ("EMC向け　接点処理追加",    "",                                  4,  100, "一柳", [(0, 1, BLUE_BAR)]),
    ("EMC向け　音声処理移植",    "HDSから移植",                        8,  100, "一柳", [(0, 1, BLUE_BAR)]),
    ("EMC向け　LED処理",         "",                                  4,  100, "一柳", [(0, 0, BLUE_BAR)]),
    ("EMC向け　FLASH書込み",     "",                                 20,   "", "木口", [(4, 7, GREEN_BAR)]),
    ("EMC向け　音声切り替え",    "アクティブ・パッシブスピーカー切替", "",   0, "一柳", [(2, 5, BLUE_BAR)]),
    ("EMC向け　システムテスト設計","",                                4,   10, "一柳", [(5, 7, BLUE_BAR)]),
    ("EMC向け　システムテスト実施","",                                8,    0, "木口", [(7, 10, GREEN_BAR)]),
    ("",                    "",                                      "",   "", "",    []),
    ("VP-A10 音声作成ツール　仕様決め", "",                           "",   30, "富養", [(0, 2, PINK_BAR)]),
    ("VP-A10 音声作成ツール　実装", "システムテスト開始前に実装完",  "",   "", "富養", [(1, 7, PINK_BAR)]),
    ("",                    "",                                      "",   "", "",    []),
    ("VP-A10 音声書込み（CAN経由）検討", "ボトルネックの原因を前倒しで検討するため", "", 30, "富養", [(0, 3, PINK_BAR)]),
    ("",                    "",                                      "",   "", "",    []),
    ("VP-A10 新機能設計",    "",                                      "",   "", "一柳", [(8, 13, BLUE_BAR)]),
    ("VP-A10 システムテスト設計", "",                                 "",   "", "一柳", [(8, 13, BLUE_BAR)]),
]

ASSIGNEE_COLOR = {"一柳": fill("DCE6F1"), "木口": fill("EBF1DE"), "富養": fill("FFCCCC"), "": None}

for row_i, (task, notes, est, prog, assignee, bars) in enumerate(tasks):
    row = row_i + 2
    ws.row_dimensions[row].height = 17

    row_bg = ASSIGNEE_COLOR.get(assignee)

    vals = [task, notes, est if est != "" else None, prog if prog != "" else None, assignee]
    for col, v in enumerate(vals, 1):
        c = ws.cell(row=row, column=col, value=v)
        c.font = Font(size=9)
        c.border = thin_border()
        if row_bg:
            c.fill = row_bg
        if col == 1:
            c.alignment = Alignment(horizontal="left", vertical="center", indent=1)
        elif col in (3, 4):
            c.alignment = Alignment(horizontal="right", vertical="center")
        else:
            c.alignment = Alignment(horizontal="center", vertical="center")

    # Gantt cells
    bar_cols = {}
    for (s, e, bf) in bars:
        for bi in range(s, e + 1):
            bar_cols[bi] = bf

    for i in range(len(dates)):
        col = FIXED_COLS + 1 + i
        c = ws.cell(row=row, column=col)
        if i in bar_cols:
            c.fill = bar_cols[i]
        elif row_bg:
            c.fill = row_bg

        # Today column red border
        if i == TODAY_IDX:
            c.border = Border(left=med, right=med, top=thin, bottom=thin)
        else:
            c.border = thin_border()

# Today column: bottom border for last row
last_row = len(tasks) + 1
for i in range(len(dates)):
    col = FIXED_COLS + 1 + i
    c = ws.cell(row=last_row, column=col)
    if i == TODAY_IDX:
        c.border = Border(left=med, right=med, top=thin, bottom=med)

# Freeze panes (freeze header row and first column)
ws.freeze_panes = "F2"

out = "/home/user/AutoUniTestGen2/WBS.xlsx"
wb.save(out)
print(f"Saved: {out}")
