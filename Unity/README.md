[和訳]
Unity Testプロジェクトへようこそ。これはThrowTheSwitch.orgが主に開発しているプロジェクトの一つです。
Unity TestはC言語向けのユニットテストフレームワークで、組み込みツールチェーンとの連携に重点を置いています。

このプロジェクトは、マイクロコントローラ（大・小）をターゲットとしたコードのテストを目的としています。
コア部分は単一のCファイルと2つのヘッダーファイルで構成されており、既存のビルド設定に簡単に追加できます。
任意のコンパイラを使用でき、多くのビルドシステム（Make、CMakeなど）とも互換性があります。

もし手間を省きたい場合は、ThrowTheSwitch.orgが提供するビルドツールのCeedlingも検討できます。

Unityの使い方に不慣れな方は、Getting Started Guide（導入ガイド）を参照してください。

また、Change Log（変更履歴）や既知の問題もドキュメントに掲載しています。

使い始めるには
docsフォルダ内に、Unityの使い方やヒントを記載したGetting Started Guideがあります。

Unity Assertion（アサーション）概要
Unityにはさまざまな検証用マクロが用意されています。以下はその一部です。

基本的な妥当性検証
TEST_ASSERT_TRUE(condition)
条件式が真（true）であれば成功、偽（false）なら失敗します。

TEST_ASSERT_FALSE(condition)
条件式が偽（false）であれば成功、真（true）なら失敗します。

TEST_ASSERT(condition)
TEST_ASSERT_TRUEの別表記です。

TEST_ASSERT_UNLESS(condition)
TEST_ASSERT_FALSEの別表記です。

TEST_FAIL()
失敗とみなします。

TEST_FAIL_MESSAGE(message)
失敗理由のメッセージを出力します。

数値の検証（整数）
TEST_ASSERT_EQUAL_INT(expected, actual)
期待値と実測値が等しいか比較します。

TEST_ASSERT_EQUAL_INT8/16/32/64(expected, actual)
サイズを指定した整数比較。

TEST_ASSERT_EQUAL_UINT(expected, actual)
符号なし整数の比較。

TEST_ASSERT_EQUAL_UINT8/16/32/64(expected, actual)
サイズを指定した符号なし整数比較。

TEST_ASSERT_EQUAL_HEX(expected, actual)
16進数表記で比較。

TEST_ASSERT_EQUAL_HEX8/16/32/64(expected, actual)
サイズを指定した16進数比較。

TEST_ASSERT(expected, actual)
TEST_ASSERT_EQUAL_INTの別表記。

TEST_ASSERT_INT_WITHIN(delta, expected, actual)
期待値の±delta範囲内かどうかを検証。

TEST_ASSERT_GREATER_THAN(threshold, actual)
実測値が閾値より大きいか。

TEST_ASSERT_LESS_THAN(threshold, actual)
実測値が閾値より小さいか。

配列の比較
TEST_ASSERT_EQUAL_HEX8_ARRAY(expected, actual, elements)
配列の内容を比較。

TEST_ASSERT_EACH_EQUAL_INT32(expected, actual, elements)
配列の全要素が特定値と等しいか。

ビット演算の検証
TEST_ASSERT_BITS(mask, expected, actual)
マスクされたビットだけ比較。

TEST_ASSERT_BITS_HIGH(mask, actual)
マスクされたビットがすべて高（1）か。

TEST_ASSERT_BITS_LOW(mask, actual)
マスクされたビットがすべて低（0）か。

TEST_ASSERT_BIT_HIGH(bit, actual)
指定ビットが高（1）か。

TEST_ASSERT_BIT_LOW(bit, actual)
指定ビットが低（0）か。

浮動小数点数の検証
TEST_ASSERT_FLOAT_WITHIN(delta, expected, actual)
小さな範囲内に収まるか。

TEST_ASSERT_DOUBLE_WITHIN(delta, expected, actual)
double精度の比較。

TEST_ASSERT_EQUAL_FLOAT/DOUBLE(expected, actual)
小さな差範囲内で等しいとみなす。

TEST_ASSERT_NOT_EQUAL_FLOAT/DOUBLE(expected, actual)
差が一定範囲外か。

TEST_ASSERT_LESS_THAN_FLOAT/DOUBLE(threshold, actual)
小なり。

TEST_ASSERT_GREATER_THAN_FLOAT/DOUBLE(threshold, actual)
大なり。

文字列の比較
TEST_ASSERT_EQUAL_STRING(expected, actual)
null終端文字列の比較。

TEST_ASSERT_EQUAL_STRING_LEN(expected, actual, len)
指定長まで比較。

TEST_ASSERT_EQUAL_STRING_MESSAGE(expected, actual, message)
メッセージ付き。

TEST_ASSERT_EQUAL_STRING_LEN_MESSAGE(expected, actual, len, message)
長さとメッセージ付き。

ポインタの検証
TEST_ASSERT_NULL(pointer)
NULLか。

TEST_ASSERT_NOT_NULL(pointer)
NULLでないか。

メモリの比較
TEST_ASSERT_EQUAL_MEMORY(expected, actual, len)
メモリブロックの比較。
補足
\\_MESSAGEを付けると、失敗時に追加のメッセージを出力できます。
まとめ
Unity Testは、組み込みシステム向けに設計された軽量なC言語用のユニットテストフレームワークです。多彩なアサーションマクロを備え、整数、浮動小数点、文字列、配列、ビット操作など多岐にわたる検証が可能です。

--------------------------------------
# Unity Test ![CI][]

__Copyright (c) 2007 - 2024 Unity Project by Mike Karlesky, Mark VanderVoord, and Greg Williams__

Welcome to the Unity Test Project, one of the main projects of ThrowTheSwitch.org.
Unity Test is a unit testing framework built for C, with a focus on working with embedded toolchains.

This project is made to test code targetting microcontrollers big and small.
The core project is a single C file and a pair of headers, allowing it to be added to your existing build setup without too much headache.
You may use any compiler you wish, and may use most existing build systems including Make, CMake, etc.
If you'd like to leave the hard work to us, you might be interested in Ceedling, a build tool also by ThrowTheSwitch.org.

If you're new to Unity, we encourage you to tour the [getting started guide][].

You can also find the [change log][] and [known issues][] in our documentation.

## Getting Started

The [docs][] folder contains a [getting started guide][] and much more tips about using Unity.

## Unity Assertion Summary

For the full list, see [UnityAssertionsReference.md][].

### Basic Validity Tests

    TEST_ASSERT_TRUE(condition)

Evaluates whatever code is in condition and fails if it evaluates to false

    TEST_ASSERT_FALSE(condition)

Evaluates whatever code is in condition and fails if it evaluates to true

    TEST_ASSERT(condition)

Another way of calling `TEST_ASSERT_TRUE`

    TEST_ASSERT_UNLESS(condition)

Another way of calling `TEST_ASSERT_FALSE`

    TEST_FAIL()
    TEST_FAIL_MESSAGE(message)

This test is automatically marked as a failure.
The message is output stating why.

### Numerical Assertions: Integers

    TEST_ASSERT_EQUAL_INT(expected, actual)
    TEST_ASSERT_EQUAL_INT8(expected, actual)
    TEST_ASSERT_EQUAL_INT16(expected, actual)
    TEST_ASSERT_EQUAL_INT32(expected, actual)
    TEST_ASSERT_EQUAL_INT64(expected, actual)

Compare two integers for equality and display errors as signed integers.
A cast will be performed to your natural integer size so often this can just be used.
When you need to specify the exact size, you can use a specific version.

    TEST_ASSERT_EQUAL_UINT(expected, actual)
    TEST_ASSERT_EQUAL_UINT8(expected, actual)
    TEST_ASSERT_EQUAL_UINT16(expected, actual)
    TEST_ASSERT_EQUAL_UINT32(expected, actual)
    TEST_ASSERT_EQUAL_UINT64(expected, actual)

Compare two integers for equality and display errors as unsigned integers.
Like INT, there are variants for different sizes also.

    TEST_ASSERT_EQUAL_HEX(expected, actual)
    TEST_ASSERT_EQUAL_HEX8(expected, actual)
    TEST_ASSERT_EQUAL_HEX16(expected, actual)
    TEST_ASSERT_EQUAL_HEX32(expected, actual)
    TEST_ASSERT_EQUAL_HEX64(expected, actual)

Compares two integers for equality and display errors as hexadecimal.
Like the other integer comparisons, you can specify the size... 
here the size will also affect how many nibbles are shown (for example, `HEX16` will show 4 nibbles).

    TEST_ASSERT_EQUAL(expected, actual)

Another way of calling TEST_ASSERT_EQUAL_INT

    TEST_ASSERT_INT_WITHIN(delta, expected, actual)

Asserts that the actual value is within plus or minus delta of the expected value.
This also comes in size specific variants.

    TEST_ASSERT_GREATER_THAN(threshold, actual)

Asserts that the actual value is greater than the threshold.
This also comes in size specific variants.

    TEST_ASSERT_LESS_THAN(threshold, actual)

Asserts that the actual value is less than the threshold.
This also comes in size specific variants.

### Arrays

    _ARRAY

You can append `_ARRAY` to any of these macros to make an array comparison of that type.
Here you will need to care a bit more about the actual size of the value being checked.
You will also specify an additional argument which is the number of elements to compare.
For example:

    TEST_ASSERT_EQUAL_HEX8_ARRAY(expected, actual, elements)

    _EACH_EQUAL

Another array comparison option is to check that EVERY element of an array is equal to a single expected value.
You do this by specifying the EACH_EQUAL macro.
For example:

    TEST_ASSERT_EACH_EQUAL_INT32(expected, actual, elements)

### Numerical Assertions: Bitwise

    TEST_ASSERT_BITS(mask, expected, actual)

Use an integer mask to specify which bits should be compared between two other integers.
High bits in the mask are compared, low bits ignored.

    TEST_ASSERT_BITS_HIGH(mask, actual)

Use an integer mask to specify which bits should be inspected to determine if they are all set high.
High bits in the mask are compared, low bits ignored.

    TEST_ASSERT_BITS_LOW(mask, actual)

Use an integer mask to specify which bits should be inspected to determine if they are all set low.
High bits in the mask are compared, low bits ignored.

    TEST_ASSERT_BIT_HIGH(bit, actual)

Test a single bit and verify that it is high.
The bit is specified 0-31 for a 32-bit integer.

    TEST_ASSERT_BIT_LOW(bit, actual)

Test a single bit and verify that it is low.
The bit is specified 0-31 for a 32-bit integer.

### Numerical Assertions: Floats

    TEST_ASSERT_FLOAT_WITHIN(delta, expected, actual)
    TEST_ASSERT_DOUBLE_WITHIN(delta, expected, actual)

Asserts that the actual value is within plus or minus delta of the expected value.

    TEST_ASSERT_FLOAT_NOT_WITHIN(delta, expected, actual)
    TEST_ASSERT_DOUBLE_NOT_WITHIN(delta, expected, actual)

Asserts that the actual value is NOT within plus or minus delta of the expected value.

    TEST_ASSERT_EQUAL_FLOAT(expected, actual)
    TEST_ASSERT_EQUAL_DOUBLE(expected, actual)

Asserts that two floating point values are "equal" within a small % delta of the expected value.

    TEST_ASSERT_NOT_EQUAL_FLOAT(expected, actual)
    TEST_ASSERT_NOT_EQUAL_DOUBLE(expected, actual)

Asserts that two floating point values are NOT "equal" within a small % delta of the expected value.

    TEST_ASSERT_LESS_THAN_FLOAT(threshold, actual)
    TEST_ASSERT_LESS_THAN_DOUBLE(threshold, actual)
    TEST_ASSERT_GREATER_THAN_FLOAT(threshold, actual)
    TEST_ASSERT_GREATER_THAN_DOUBLE(threshold, actual)

Asserts that the actual value is less than or greater than the threshold.

There are also `LESS_OR_EQUAL` and `GREATER_OR_EQUAL` variations.
These obey the same rules for equality as do `TEST_ASSERT_EQUAL_FLOAT` and `TEST_ASSERT_EQUAL_DOUBLE`:
If the two values are within a small % delta of the expected value, the assertion will pass.

### String Assertions

    TEST_ASSERT_EQUAL_STRING(expected, actual)

Compare two null-terminate strings.
Fail if any character is different or if the lengths are different.

    TEST_ASSERT_EQUAL_STRING_LEN(expected, actual, len)

Compare two strings.
Fail if any character is different, stop comparing after len characters.

    TEST_ASSERT_EQUAL_STRING_MESSAGE(expected, actual, message)

Compare two null-terminate strings.
Fail if any character is different or if the lengths are different.
Output a custom message on failure.

    TEST_ASSERT_EQUAL_STRING_LEN_MESSAGE(expected, actual, len, message)

Compare two strings.
Fail if any character is different, stop comparing after len characters.
Output a custom message on failure.

### Pointer Assertions

Most pointer operations can be performed by simply using the integer comparisons above.
However, a couple of special cases are added for clarity.

    TEST_ASSERT_NULL(pointer)

Fails if the pointer is not equal to NULL

    TEST_ASSERT_NOT_NULL(pointer)

Fails if the pointer is equal to NULL

### Memory Assertions

    TEST_ASSERT_EQUAL_MEMORY(expected, actual, len)

Compare two blocks of memory.
This is a good generic assertion for types that can't be coerced into acting like standard types... 
but since it's a memory compare, you have to be careful that your data types are packed.

### \_MESSAGE

You can append `\_MESSAGE` to any of the macros to make them take an additional argument.
This argument is a string that will be printed at the end of the failure strings.
This is useful for specifying more information about the problem.

[CI]: https://github.com/ThrowTheSwitch/Unity/workflows/CI/badge.svg
[getting started guide]: docs/UnityGettingStartedGuide.md
[change log]: docs/UnityChangeLog.md
[known issues]: docs/UnityKnownIssues.md
[docs]: docs/
[UnityAssertionsReference.md]: docs/UnityAssertionsReference.md
