#!/usr/bin/env python3
"""
C言語単体テスト自動生成ツール
MC/DC 100% カバレッジ + Unity テストフレームワーク

開発手順:
  ① AI自身でテスト対象C関数を新規作成 (function/ フォルダ)
  ② MC/DC 100%真偽表 (Excelファイル) を作成 (answer_unit_test/ フォルダ)
  ③ 解答単体テストコードを作成 (answer_unit_test/ フォルダ)
  ④ 真偽表と単体テストコードを導くPythonコード (generator/generate.py) を作成
  ⑤ Pythonコードを実行して真偽表と単体テストコードを作成 (work/ フォルダ)
  ⑥ 解答 (answer_unit_test/) とwork/ を全関数分比較
  ⑦ 比較NG → 原因追究して generate.py を修正、⑤へ (最大5回)
  ⑧ 比較OK → GITコミットして①へ。5回繰り返したら終了。
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

import anthropic
import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill

# ─────────────────────────── 定数 ───────────────────────────
BASE_DIR = Path(__file__).parent
FUNCTION_DIR = BASE_DIR / "function"
ANSWER_DIR = BASE_DIR / "answer_unit_test"
WORK_DIR = BASE_DIR / "work"
GENERATOR_DIR = BASE_DIR / "generator"
UNITY_SRC_DIR = BASE_DIR / "Unity" / "src"

MAX_ITERATIONS = 5   # 全体ループ上限
MAX_RETRIES = 5      # 比較失敗時のリトライ上限

MODEL = "claude-opus-4-6"

# 各イテレーションの関数複雑度説明
COMPLEXITY_DESCRIPTIONS = [
    "Simple: 2 integer parameters, exactly 1 if statement using AND (&&) of exactly 2 comparison conditions.",
    "Medium-low: 2-3 integer parameters, 1 if statement using 3 conditions combined with && and ||.",
    "Medium: 3 integer parameters, 2 separate if statements, each with 2 conditions using && or ||. Different return values.",
    "Medium-high: 3 integer parameters, 2 if statements where the second has 3 conditions using &&, ||, and !.",
    "Complex: 4 integer parameters, 3 if statements with mixed conditions using &&, ||, !. Different return values.",
]

# ─────────────────────────── ディレクトリ準備 ───────────────────────────
def ensure_dirs():
    for d in [FUNCTION_DIR, ANSWER_DIR, WORK_DIR, GENERATOR_DIR]:
        d.mkdir(exist_ok=True)
    init_file = GENERATOR_DIR / "__init__.py"
    if not init_file.exists():
        init_file.touch()


# ─────────────────────────── Claude API ヘルパー ───────────────────────────
def call_claude(client: anthropic.Anthropic, prompt: str,
                system: str = None, max_tokens: int = 8192) -> str:
    """Claudeを呼び出してテキストを返す (ストリーミング対応)"""
    kwargs = {
        "model": MODEL,
        "max_tokens": max_tokens,
        "thinking": {"type": "adaptive"},
        "messages": [{"role": "user", "content": prompt}],
    }
    if system:
        kwargs["system"] = system

    with client.messages.stream(**kwargs) as stream:
        return stream.get_final_message().content[-1].text


def extract_json(text: str) -> dict:
    """Claude応答からJSONを抽出する"""
    # コードブロック内を試みる
    m = re.search(r"```(?:json)?\s*([\s\S]+?)\s*```", text)
    if m:
        return json.loads(m.group(1))
    # 直接パース
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    # { } ブロックを探す
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1:
        return json.loads(text[start : end + 1])
    raise ValueError(f"JSON を抽出できません:\n{text[:600]}")


def extract_code(text: str, lang: str = "") -> str:
    """Claude応答からコードブロックを抽出する"""
    m = re.search(rf"```(?:{lang})?\s*([\s\S]+?)\s*```", text)
    if m:
        return m.group(1).strip()
    return text.strip()


# ─────────────────────────── ① C関数生成 ───────────────────────────
def generate_c_function(client: anthropic.Anthropic, iteration: int) -> dict:
    """Claudeを使ってC言語の関数を生成する"""
    func_name = f"func_{iteration + 1:03d}"
    complexity = COMPLEXITY_DESCRIPTIONS[iteration]

    prompt = f"""Create a C language function for MC/DC unit testing.

Function name: {func_name}
Complexity: {complexity}

Strict requirements:
- Only int type parameters and int return type
- Only if statements (no loops, no switch, no nested function calls)
- Conditions use comparison operators: >, <, >=, <=, ==, !=
- Boolean operators: &&, ||, ! only
- Each if branch returns a DIFFERENT non-zero int value
- A final "return 0;" as default at the end
- Include a .h header file with the declaration and include guard

Output ONLY valid JSON (no markdown):
{{
  "header_content": "<complete content of {func_name}.h>",
  "source_content": "<complete content of {func_name}.c>"
}}"""

    response = call_claude(client, prompt, max_tokens=4096)
    data = extract_json(response)
    return data


# ─────────────────────────── ② 真偽表データ生成 ───────────────────────────
def generate_truth_table_data(client: anthropic.Anthropic,
                               source_content: str,
                               func_name: str) -> dict:
    """ClaudeにC関数を解析させてMC/DC真偽表データをJSONで返す"""

    prompt = f"""Analyze this C function and create a complete MC/DC 100% truth table.

C source:
```c
{source_content}
```

Rules for MC/DC:
- Identify every if statement (numbered IF1, IF2, ...)
- Label each atomic comparison as A, B, C, ... (e.g. A = "a > 0")
- For N atomic conditions, generate EXACTLY N+1 test cases (minimum MC/DC set)
- For each condition X, there must exist a pair of test cases where:
    * Only X's truth value differs
    * The overall decision outcome changes
- For each test case, provide actual integer parameter values that satisfy the conditions
- The "expected_return" is what the ACTUAL function returns for those parameter values
  (considering ALL if statements, not just the one being tested)

Output ONLY valid JSON (no markdown):
{{
  "function_name": "{func_name}",
  "parameters": ["a", "b"],
  "if_statements": [
    {{
      "if_id": "IF1",
      "condition_expression": "a > 0 && b > 0",
      "atomic_conditions": [
        {{"id": "A", "expression": "a > 0", "variable": "a", "operator": ">", "threshold": 0}},
        {{"id": "B", "expression": "b > 0", "variable": "b", "operator": ">", "threshold": 0}}
      ],
      "test_cases": [
        {{
          "tc_id": "TC1",
          "condition_values": {{"A": true, "B": true}},
          "decision": true,
          "param_values": {{"a": 1, "b": 1}},
          "expected_return": 1,
          "mcdc_note": "A: TC1-TC2, B: TC1-TC3"
        }}
      ]
    }}
  ]
}}"""

    response = call_claude(client, prompt, max_tokens=8192)
    return extract_json(response)


# ─────────────────────────── ② Excelファイル保存 ───────────────────────────
def save_truth_table_excel(truth_table_data: dict, output_path: Path):
    """真偽表データをExcelファイルとして保存する"""
    wb = openpyxl.Workbook()
    wb.remove(wb.active)  # デフォルトシートを削除

    hdr_font = Font(bold=True, color="FFFFFF")
    hdr_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    center = Alignment(horizontal="center")

    params = truth_table_data["parameters"]

    for if_stmt in truth_table_data["if_statements"]:
        ws = wb.create_sheet(title=if_stmt["if_id"])
        conditions = if_stmt["atomic_conditions"]

        # ヘッダー行
        headers = (
            ["TC"]
            + params
            + [c["expression"] for c in conditions]
            + ["Decision", "Return"]
        )
        for col, h in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=h)
            cell.font = hdr_font
            cell.fill = hdr_fill
            cell.alignment = center
            ws.column_dimensions[
                openpyxl.utils.get_column_letter(col)
            ].width = max(12, len(str(h)) + 2)

        # データ行
        for row_idx, tc in enumerate(if_stmt["test_cases"], 2):
            col = 1
            ws.cell(row=row_idx, column=col, value=tc["tc_id"])
            col += 1
            for p in params:
                ws.cell(row=row_idx, column=col, value=tc["param_values"].get(p, 0))
                col += 1
            for cond in conditions:
                val = tc["condition_values"].get(cond["id"], False)
                ws.cell(row=row_idx, column=col, value="T" if val else "F")
                col += 1
            ws.cell(row=row_idx, column=col, value="T" if tc["decision"] else "F")
            col += 1
            ws.cell(row=row_idx, column=col, value=tc["expected_return"])

    wb.save(output_path)


# ─────────────────────────── ③ Unityテストコード生成 ───────────────────────────
def generate_test_code(client: anthropic.Anthropic,
                       func_name: str,
                       truth_table_data: dict) -> str:
    """真偽表データをもとにUnityテストコードを生成する"""

    params = truth_table_data["parameters"]
    tc_list = []
    for if_stmt in truth_table_data["if_statements"]:
        if_id = if_stmt["if_id"]
        cond_expr = if_stmt["condition_expression"]
        for tc in if_stmt["test_cases"]:
            param_str = ", ".join(str(tc["param_values"][p]) for p in params)
            tc_list.append(
                f'  IF={if_id}, TC={tc["tc_id"]}, '
                f'params=({param_str}), '
                f'expected={tc["expected_return"]}, '
                f'condition="{cond_expr}"'
            )

    tc_summary = "\n".join(tc_list)

    prompt = f"""Generate Unity unit test code for the C function "{func_name}".

Test cases (all must be included):
{tc_summary}

Output format requirements:
1. First line: #include "unity.h"
2. Second line: #include "{func_name}.h"
3. Empty line
4. void setUp(void) {{}}
5. void tearDown(void) {{}}
6. Empty line
7. For each test case, generate:
   /* <IF_ID>: condition_expression */
   void test_{func_name}_<IF_ID>_<TC_ID>(void) {{
       TEST_ASSERT_EQUAL_INT(<expected>, {func_name}(<param_values>));
   }}
   (followed by empty line)
8. int main(void) with UNITY_BEGIN(), all RUN_TEST() calls, return UNITY_END();

Output ONLY the complete C source code (no markdown, no explanation):"""

    response = call_claude(client, prompt, max_tokens=4096)
    return extract_code(response, "c")


# ─────────────────────────── ④ generate.py 作成/更新 ───────────────────────────
_GENERATOR_SPEC = """\
STRICT OUTPUT SPECIFICATION for generate.py:

Excel truth table (work/<func_name>_truth_table.xlsx):
  - One sheet per if-statement, sheet name = "IF1", "IF2", etc.
  - Row 1 headers: ["TC", param1, param2, ..., cond_expr1, cond_expr2, ..., "Decision", "Return"]
    * Header cells: bold white font, blue (#4472C4) fill, center aligned
  - Row 2+: one row per test case
    * TC column: "TC1", "TC2", ...
    * Parameter columns: actual integer values (int)
    * Atomic condition columns: "T" or "F" string
    * Decision column: "T" or "F" string
    * Return column: integer value

Unity test code (work/<func_name>_test.c):
  - Exact format:
    #include "unity.h"
    #include "<func_name>.h"
    (empty line)
    void setUp(void) {}
    void tearDown(void) {}
    (empty line)
    /* IF1: <condition_expression> */
    void test_<func_name>_IF1_TC1(void) {
        TEST_ASSERT_EQUAL_INT(<expected>, <func_name>(<params>));
    }
    (empty line)
    ... (all test cases for all if-statements) ...
    int main(void) {
        UNITY_BEGIN();
        RUN_TEST(test_<func_name>_IF1_TC1);
        ... (all tests) ...
        return UNITY_END();
    }
"""


def create_generator(client: anthropic.Anthropic,
                     sample_c_code: str,
                     sample_truth_table: dict,
                     sample_test_code: str,
                     func_name: str) -> str:
    """generate.py のソースコードをClaudeに生成させる"""

    prompt = f"""Create a complete Python script "generator/generate.py" that automatically
generates MC/DC truth tables and Unity test code from a C source file.

This script must be PURE PYTHON with NO AI/Claude API calls — purely algorithmic.
Allowed libraries: re, sys, os, itertools, pathlib, openpyxl, openpyxl.styles

=== SAMPLE C FUNCTION ===
{sample_c_code}

=== EXPECTED TRUTH TABLE JSON ===
{json.dumps(sample_truth_table, indent=2)}

=== EXPECTED UNITY TEST CODE ===
{sample_test_code}

=== STRICT OUTPUT SPECIFICATION ===
{_GENERATOR_SPEC}

=== ALGORITHM REQUIREMENTS ===

1. ARGUMENT: sys.argv[1] = path to C source file

2. PARSE FUNCTION SIGNATURE:
   - Extract function name and parameter names from "int func_name(int a, int b, ...)"

3. PARSE IF STATEMENTS:
   - Find all "if (...)" conditions in the function body (not else-if)
   - Extract the condition expression inside the parentheses
   - Number them IF1, IF2, ...

4. PARSE ATOMIC CONDITIONS from condition expression:
   - Match pattern: variable op literal  (e.g. "a > 0", "b != 5", "c <= 10")
   - Supported operators: >, <, >=, <=, ==, !=
   - Label them A, B, C, ... in order found
   - Handle negation "!" in front of sub-expressions

5. EVALUATE BOOLEAN EXPRESSION:
   - Replace each condition label (A, B, C) with Python True/False
   - Replace C operators: && → and, || → or, ! → not
   - Use eval() to compute the decision outcome

6. MC/DC ALGORITHM:
   a. Enumerate all 2^N truth combinations for N atomic conditions
   b. Evaluate decision for each combination
   c. For each condition X (index i):
      - Find pairs (combo_j, combo_k) where:
        * Only condition i differs
        * Decision outcome differs
      → These are "independence pairs" for condition X
   d. Greedy selection: repeatedly pick the index that covers the most
      uncovered (condition, pair) requirements until all conditions are covered
   e. Result: minimum set of 2^i indices achieving MC/DC (N+1 test cases for N conditions)

7. MAP BOOL TO C VALUES:
   For condition "var op threshold":
   - op ">":  true → threshold+1,  false → threshold
   - op "<":  true → threshold-1,  false → threshold
   - op ">=": true → threshold,    false → threshold-1
   - op "<=": true → threshold,    false → threshold+1
   - op "==": true → threshold,    false → threshold+1
   - op "!=": true → threshold+1,  false → threshold

8. SIMULATE FUNCTION EXECUTION to get expected return value:
   - For each test case, evaluate each if-condition in order using actual param values
   - Return the value from the FIRST matching if-branch
   - If no if-branch matches, return the default return value (last "return N;" in function)

9. OUTPUT DIRECTORY: Always write to "work/" relative to the script's parent-parent directory
   (i.e., Path(__file__).parent.parent / "work")

Output ONLY the complete Python script (no markdown, no explanation):"""

    response = call_claude(client, prompt, max_tokens=16000)
    return extract_code(response, "python")


# ─────────────────────────── ⑤ generator実行 ───────────────────────────
def run_generator_on_all(accumulated_funcs: list) -> tuple[bool, str]:
    """全蓄積関数に対して generator/generate.py を実行する"""
    generator_path = GENERATOR_DIR / "generate.py"
    if not generator_path.exists():
        return False, "generator/generate.py が存在しません"

    # workディレクトリをクリア
    for f in WORK_DIR.glob("*.xlsx"):
        f.unlink()
    for f in WORK_DIR.glob("*.c"):
        f.unlink()

    for func_name in accumulated_funcs:
        c_file = FUNCTION_DIR / f"{func_name}.c"
        if not c_file.exists():
            return False, f"{c_file} が存在しません"

        result = subprocess.run(
            ["python3", str(generator_path), str(c_file)],
            capture_output=True,
            text=True,
            cwd=str(BASE_DIR),
        )
        if result.returncode != 0:
            return False, (
                f"{func_name} の処理でエラー:\n"
                f"STDOUT: {result.stdout}\n"
                f"STDERR: {result.stderr}"
            )

    return True, ""


# ─────────────────────────── ⑥ 比較ロジック ───────────────────────────
def compare_excel(work_path: Path, answer_path: Path, func_name: str) -> list:
    """2つのExcelファイルを意味的に比較してミスマッチリストを返す"""
    mismatches = []

    try:
        wb_w = openpyxl.load_workbook(work_path)
        wb_a = openpyxl.load_workbook(answer_path)
    except Exception as e:
        return [f"Excelロードエラー: {e}"]

    sheets_w = sorted(wb_w.sheetnames)
    sheets_a = sorted(wb_a.sheetnames)

    if sheets_w != sheets_a:
        mismatches.append(
            f"シート名が異なります: work={sheets_w}, answer={sheets_a}"
        )
        return mismatches

    for sheet in sheets_a:
        ws_w = wb_w[sheet]
        ws_a = wb_a[sheet]

        # ヘッダー比較
        hdrs_a = [ws_a.cell(1, c).value for c in range(1, ws_a.max_column + 1)]
        hdrs_w = [ws_w.cell(1, c).value for c in range(1, ws_w.max_column + 1)]
        if hdrs_a != hdrs_w:
            mismatches.append(
                f"[{sheet}] ヘッダー不一致:\n  answer={hdrs_a}\n  work={hdrs_w}"
            )

        # 行数比較
        if ws_w.max_row != ws_a.max_row:
            mismatches.append(
                f"[{sheet}] 行数不一致: work={ws_w.max_row}, answer={ws_a.max_row}"
            )

        # 各TC の Return 列比較
        ret_col_a = ws_a.max_column
        ret_col_w = ws_w.max_column
        for row in range(2, ws_a.max_row + 1):
            tc_id = ws_a.cell(row, 1).value
            ret_a = ws_a.cell(row, ret_col_a).value
            # workから同じTC_IDを探す
            found = False
            for wrow in range(2, ws_w.max_row + 1):
                if ws_w.cell(wrow, 1).value == tc_id:
                    found = True
                    ret_w = ws_w.cell(wrow, ret_col_w).value
                    if ret_a != ret_w:
                        mismatches.append(
                            f"[{sheet}] {tc_id}: Return不一致 answer={ret_a}, work={ret_w}"
                        )
                    break
            if not found:
                mismatches.append(f"[{sheet}] {tc_id} が work に存在しません")

    return mismatches


def compare_c_files(work_path: Path, answer_path: Path) -> list:
    """2つのUnityテストCファイルを比較する"""
    mismatches = []
    try:
        wc = work_path.read_text()
        ac = answer_path.read_text()
    except Exception as e:
        return [f"Cファイル読み込みエラー: {e}"]

    # TEST_ASSERT_EQUAL_INT呼び出しを抽出して比較
    pattern = r"TEST_ASSERT_EQUAL_INT\s*\(\s*(-?\d+)\s*,\s*\w+\s*\([^)]*\)\s*\)"
    asserts_w = sorted(re.findall(pattern, wc))
    asserts_a = sorted(re.findall(pattern, ac))

    if asserts_w != asserts_a:
        mismatches.append(
            f"TEST_ASSERT_EQUAL_INT の期待値リストが異なります:\n"
            f"  answer={asserts_a}\n  work={asserts_w}"
        )

    # テスト関数名を抽出して比較
    funcs_w = sorted(re.findall(r"void\s+(test_\w+)\s*\(void\)", wc))
    funcs_a = sorted(re.findall(r"void\s+(test_\w+)\s*\(void\)", ac))
    if funcs_w != funcs_a:
        mismatches.append(
            f"テスト関数名が異なります:\n  answer={funcs_a}\n  work={funcs_w}"
        )

    return mismatches


def compare_all_files(accumulated_funcs: list) -> dict:
    """全蓄積関数の work vs answer を比較してミスマッチ辞書を返す"""
    all_mismatches = {}

    for func_name in accumulated_funcs:
        mismatches = []

        work_xlsx = WORK_DIR / f"{func_name}_truth_table.xlsx"
        answer_xlsx = ANSWER_DIR / f"{func_name}_truth_table.xlsx"
        if not work_xlsx.exists():
            mismatches.append(f"work Excel が存在しません: {work_xlsx.name}")
        elif not answer_xlsx.exists():
            mismatches.append(f"answer Excel が存在しません: {answer_xlsx.name}")
        else:
            mismatches.extend(compare_excel(work_xlsx, answer_xlsx, func_name))

        work_c = WORK_DIR / f"{func_name}_test.c"
        answer_c = ANSWER_DIR / f"{func_name}_test.c"
        if not work_c.exists():
            mismatches.append(f"work Cファイルが存在しません: {work_c.name}")
        elif not answer_c.exists():
            mismatches.append(f"answer Cファイルが存在しません: {answer_c.name}")
        else:
            mismatches.extend(compare_c_files(work_c, answer_c))

        if mismatches:
            all_mismatches[func_name] = mismatches

    return all_mismatches


# ─────────────────────────── ⑦ generate.py 修正 ───────────────────────────
def fix_generator(client: anthropic.Anthropic,
                  mismatches: dict,
                  run_error: str,
                  accumulated_funcs: list) -> str:
    """ミスマッチ情報をもとにClaudeに generate.py を修正させる"""
    generator_path = GENERATOR_DIR / "generate.py"
    current_code = generator_path.read_text() if generator_path.exists() else ""

    # サンプルのCコードを収集（最大2関数）
    c_samples = {}
    for fn in accumulated_funcs[:2]:
        cf = FUNCTION_DIR / f"{fn}.c"
        if cf.exists():
            c_samples[fn] = cf.read_text()

    # answer の真偽表JSONも収集
    answer_samples = {}
    for fn in accumulated_funcs[:2]:
        jf = ANSWER_DIR / f"{fn}_truth_table.json"
        if jf.exists():
            try:
                answer_samples[fn] = json.loads(jf.read_text())
            except Exception:
                pass

    problem_desc = ""
    if run_error:
        problem_desc = f"実行エラー:\n{run_error}\n"
    if mismatches:
        problem_desc += f"比較ミスマッチ:\n{json.dumps(mismatches, indent=2, ensure_ascii=False)}\n"

    prompt = f"""The Python generator script has bugs. Fix it based on the problems below.

=== PROBLEMS ===
{problem_desc}

=== CURRENT generate.py ===
```python
{current_code}
```

=== C FUNCTIONS THAT CAUSED FAILURES ===
{json.dumps(c_samples, indent=2, ensure_ascii=False)}

=== EXPECTED TRUTH TABLE DATA ===
{json.dumps(answer_samples, indent=2, ensure_ascii=False)}

=== STRICT OUTPUT SPECIFICATION ===
{_GENERATOR_SPEC}

Analyze the root cause carefully and output the COMPLETE fixed Python script
(no markdown, no explanation, pure Python code only):"""

    response = call_claude(client, prompt, max_tokens=16000)
    return extract_code(response, "python")


# ─────────────────────────── ⑧ Gitコミット ───────────────────────────
def git_commit(iteration: int, func_name: str):
    """現在の状態をGitにコミットする"""
    subprocess.run(["git", "add", "-A"], check=True, cwd=str(BASE_DIR))
    msg = (
        f"[iter {iteration + 1}] Add {func_name}: "
        f"MC/DC truth table and Unity tests"
    )
    subprocess.run(["git", "commit", "-m", msg], check=True, cwd=str(BASE_DIR))
    print(f"  ✓ Gitコミット完了: {msg}")


# ─────────────────────────── メインループ ───────────────────────────
def main():
    print("=" * 60)
    print("  C言語単体テスト自動生成ツール (MC/DC 100% + Unity)")
    print("=" * 60)

    ensure_dirs()
    client = anthropic.Anthropic()
    accumulated_funcs: list[str] = []

    for iteration in range(MAX_ITERATIONS):
        func_name = f"func_{iteration + 1:03d}"
        print(f"\n{'=' * 60}")
        print(f"  イテレーション {iteration + 1}/{MAX_ITERATIONS}: {func_name}")
        print("=" * 60)

        # ─── ① C関数生成 ───
        print(f"\n[Step 1] C関数を生成: {func_name}")
        func_data = generate_c_function(client, iteration)

        header_path = FUNCTION_DIR / f"{func_name}.h"
        source_path = FUNCTION_DIR / f"{func_name}.c"
        header_path.write_text(func_data["header_content"])
        source_path.write_text(func_data["source_content"])
        print(f"  保存: {header_path.relative_to(BASE_DIR)}")
        print(f"  保存: {source_path.relative_to(BASE_DIR)}")
        print(f"\n  生成コード:\n{func_data['source_content']}")

        # ─── ② 真偽表 (answer) 生成 ───
        print(f"\n[Step 2] MC/DC真偽表を生成 (answer)")
        truth_table_data = generate_truth_table_data(
            client, func_data["source_content"], func_name
        )
        answer_xlsx = ANSWER_DIR / f"{func_name}_truth_table.xlsx"
        answer_json = ANSWER_DIR / f"{func_name}_truth_table.json"
        save_truth_table_excel(truth_table_data, answer_xlsx)
        answer_json.write_text(json.dumps(truth_table_data, indent=2, ensure_ascii=False))
        print(f"  保存: {answer_xlsx.relative_to(BASE_DIR)}")

        # ─── ③ Unityテストコード (answer) 生成 ───
        print(f"\n[Step 3] Unityテストコードを生成 (answer)")
        test_code = generate_test_code(client, func_name, truth_table_data)
        answer_c = ANSWER_DIR / f"{func_name}_test.c"
        answer_c.write_text(test_code)
        print(f"  保存: {answer_c.relative_to(BASE_DIR)}")

        accumulated_funcs.append(func_name)

        # ─── ④ generate.py 作成/更新 ───
        generator_path = GENERATOR_DIR / "generate.py"
        action = "更新" if generator_path.exists() else "作成"
        print(f"\n[Step 4] generator/generate.py を{action}")
        gen_code = create_generator(
            client,
            func_data["source_content"],
            truth_table_data,
            test_code,
            func_name,
        )
        generator_path.write_text(gen_code)
        print(f"  保存: {generator_path.relative_to(BASE_DIR)}")

        # ─── ⑤-⑦ 実行・比較・修正ループ ───
        success = False
        for retry in range(MAX_RETRIES):
            print(f"\n[Step 5] generate.py を実行 (試行 {retry + 1}/{MAX_RETRIES})")
            run_ok, run_error = run_generator_on_all(accumulated_funcs)

            if not run_ok:
                print(f"  ✗ 実行エラー:\n{run_error}")
                print(f"\n[Step 7] generate.py を修正 (実行エラー)")
                fixed = fix_generator(client, {}, run_error, accumulated_funcs)
                generator_path.write_text(fixed)
                continue

            print(f"\n[Step 6] 比較: work/ vs answer_unit_test/")
            mismatches = compare_all_files(accumulated_funcs)

            if not mismatches:
                print("  ✓ すべてのファイルが一致しました！")
                success = True
                break
            else:
                print("  ✗ ミスマッチを検出:")
                for fn, issues in mismatches.items():
                    print(f"    [{fn}]")
                    for issue in issues:
                        print(f"      - {issue}")
                print(f"\n[Step 7] generate.py を修正 (ミスマッチ)")
                fixed = fix_generator(client, mismatches, "", accumulated_funcs)
                generator_path.write_text(fixed)

        if not success:
            print(
                f"\n{'=' * 60}"
                f"\n  FAILURE: {MAX_RETRIES}回リトライしても修正できませんでした"
                f"\n  イテレーション {iteration + 1} で開発終了"
                f"\n{'=' * 60}"
            )
            sys.exit(1)

        # ─── ⑧ Gitコミット ───
        print(f"\n[Step 8] Gitコミット")
        try:
            git_commit(iteration, func_name)
        except subprocess.CalledProcessError as e:
            print(f"  ✗ Gitコミット失敗: {e}")

    print(f"\n{'=' * 60}")
    print(f"  SUCCESS: 全 {MAX_ITERATIONS} イテレーション完了！")
    print("=" * 60)


if __name__ == "__main__":
    main()
