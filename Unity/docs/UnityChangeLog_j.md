[和訳]
# Unity Test - 変更履歴（Change Log）

## 注意事項

このドキュメントは、Unityプロジェクトのコアソースファイルおよびスクリプトに対する主な機能追加や修正内容をまとめたものです。  
より詳細な履歴はGitHubの履歴で確認できます。

現在、このプロジェクトでは変更内容をより詳細に記録しています。過去のリリースについては、履歴を遡るほど詳細が少なくなっています。

- 2012年以前は、プロジェクトはSourceForge.netでホストされていました。
- 2008年以前は、プロジェクトは社内プロジェクトであり、一般公開されていませんでした。

---

## ログ

### Unity 2.6.1（2025年1月）

**新機能:**
- 厳密なマッチャーとして `-n` コマンドラインオプションを再追加

**主なバグ修正:**
- コマンドラインオプションの不一致選択時の問題を防止

**その他:**
- gccでの変換警告への対策
- 冗長なラインキャストの削除
- より多くの内部関数をstatic化

---

### Unity 2.6.0（2024年3月）

**新機能:**
- 配列やwithinなどの不足していたバリエーションを追加
- `TEST_PRINTF()` を追加
- `TEST_MATRIX()` および `TEST_RANGE()` オプションとドキュメントを追加
- テスト依存関係を判定するための `TEST_SOURCE_FILE()` 検索サポートを追加
- Unity BDDプラグインを追加
- テスト実行時間を報告する `UNITY_INCLUDE_EXEC_TIME` オプションを追加
- テスト中断の基盤メカニズムをユーザーが上書き可能に
- 浮動小数点・倍精度用の `NOT_EQUAL*` および `NOT_WITHIN*` チェックを追加

**主なバグ修正:**
- NaNおよびInfinityのより移植性の高い検証。`UNITY_IS_NAN` および `UNITY_IS_INF` オプションを追加
- `UNITY_PROGMEM` 設定オプションを追加
- 配列使用時の16進値オーバーフロー検出の修正
- Ruby標準の変更によるスクリプトの不具合修正

**その他:**
- 片方がnullの場合のポインタ比較を回避し、コンパイラ警告を防止
- ドキュメントの大幅な改善
- 最新のRubyスタイル仕様に合わせて更新
- Meson、CMake、PlatformIOビルド対応

---

### Unity 2.5.2（2021年1月）

- RUN_TESTマクロおよび生成されるRUN_TESTの改良
- `UNITY_TEST_ASSERT_BIT(S)_HIGH` の修正
- CMockによる詳細トラッキングの処理をよりクリーンに

---

### Unity 2.5.1（2020年5月）

主にバグ修正と安定性向上のリリース。追加機能:

- オプションの TEST_PRINTF マクロ
- セルフテスト手順の改善

---

### Unity 2.5.0（2019年10月）

前回のリリースからかなり時間が経ちましたが、ついにリリース！  
ここにすべてを挙げるには多すぎるため、主なハイライトのみ記載します。

- より標準準拠（ただし、どんな癖のあるコンパイラもサポートする方針は維持）
- より多くの専門的なアサーションでテストフィードバックを強化
- 統合例を多数追加
- 多数のバグ修正と微調整

---

### Unity 2.4.3（2017年11月）

- suiteSetUp() および suiteTearDown() を通常のC関数として提供可能に
- 整数の Greater Than / Less Than アサーションの修正と拡張
- テスト結果のカラー表示オプションを内蔵
- ドキュメントの更新

---

### Unity 2.4.2（2017年9月）

- `UNTY_TEST_ASSERT_EACH_EQUAL_*` のバグ修正
- `TEST_ASSERT_GREATER_THAN` および `TEST_ASSERT_LESS_THAN` を追加
- スタイル未指定時に名前変更を止めるようモジュールジェネレーターを更新
- 精度向上のためカスタム浮動小数点出力処理を整理
- 部分一致時の誤った行番号の整理
- よく使われる関数名を変数名に使った際の警告を削減

---

### Unity 2.4.1（2017年4月）

- テストランナージェネレーターでdefineやヘッダーの挿入が可能に
- printfに依存しない組み込みの浮動小数点出力ルーチンを追加
- 新しいコーディング・命名規約に更新
- ドキュメントをPDFからMarkdownに変更
- 多数の小さなバグ修正（多くはコミュニティからの提供！）
- コーディング規約のCIによる自動チェックを実施

---

### Unity 2.4.0（2016年10月）

- SourceForgeからの移行と多数のバグ修正

---

# Unity Test - Change Log

## A Note

This document captures significant features and fixes to the Unity project core source files 
and scripts. More detail can be found in the history on Github. 

This project is now tracking changes in more detail. Previous releases get less detailed as
we move back in histroy. 

Prior to 2012, the project was hosted on SourceForge.net
Prior to 2008, the project was an internal project and not released to the public.

## Log

### Unity 2.6.1 (Jan 2025)

New Features:
  
  - Add `-n` comand line option as strict matcher again

Significant Bugfixes:

  - Protect against problems when mis-matched command line options selected

Other:

  - Protect against Conversion warnings in gcc
  - Remove Redundant line-casts
  - Make more internal functions static

### Unity 2.6.0 (Mar 2024)

New Features:

  - Fill out missing variations of arrays, within, etc. 
  - Add `TEST_PRINTF()`
  - Add `TEST_MATRIX()` and `TEST_RANGE()` options and documentation
  - Add support for searching `TEST_SOURCE_FILE()` for determining test dependencies
  - Add Unity BDD plugin
  - Add `UNITY_INCLUDE_EXEC_TIME` option to report test times
  - Allow user to override test abort underlying mechanism
  - Add `NOT_EQUAL*` and `NOT_WITHIN*` checks for floats and doubles 

Significant Bugfixes:

  - More portable validation of NaN and Infinity. Added `UNITY_IS_NAN` and `UNITY_IS_INF` options
  - Add `UNITY_PROGMEM` configuration option
  - Fix overflow detection of hex values when using arrays
  - Fix scripts broken by Ruby standard changes

Other:

  - Avoid pointer comparison when one is null to avoid compiler warnings
  - Significant improvements to documentation
  - Updates to match latest Ruby style specification
  - Meson, CMake, PlatformIO builds

### Unity 2.5.2 (January 2021)

  - improvements to RUN_TEST macro and generated RUN_TEST
  - Fix `UNITY_TEST_ASSERT_BIT(S)_HIGH`
  - Cleaner handling of details tracking by CMock

### Unity 2.5.1 (May 2020)

Mostly a bugfix and stability release.
Bonus Features:

  - Optional TEST_PRINTF macro
  - Improve self-testing procedures.

### Unity 2.5.0 (October 2019)

It's been a LONG time since the last release of Unity. Finally, here it is!
There are too many updates to list here, so some highlights:

  - more standards compliant (without giving up on supporting ALL compilers, no matter how quirky)
  - many more specialized assertions for better test feedback
  - more examples for integrating into your world
  - many many bugfixes and tweaks

### Unity 2.4.3 (November 2017)

  - Allow suiteSetUp() and suiteTearDown() to be povided as normal C functions
  - Fix & Expand Greater Than / Less Than assertions for integers
  - Built-in option to colorize test results
  - Documentation updates

### Unity 2.4.2 (September 2017)

  - Fixed bug in UNTY_TEST_ASSERT_EACH_EQUAL_*
  - Added TEST_ASSERT_GREATER_THAN and TEST_ASSERT_LESS_THAN
  - Updated Module Generator to stop changing names when no style given
  - Cleanup to custom float printing for accuracy
  - Cleanup incorrect line numbers are partial name matching
  - Reduce warnings from using popular function names as variable names

### Unity 2.4.1 (April 2017)

  - test runner generator can inject defines as well as headers
  - added a built-in floating point print routine instead of relying on printf
  - updated to new coding and naming standard
  - updated documentation to be markdown instead of pdf
  - fixed many many little bugs, most of which were supplied by the community (you people are awesome!)
  - coding standard actually enforced in CI

### Unity 2.4.0 (October, 2016)

  - port from SourceForge and numerous bugfixes
