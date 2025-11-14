[和訳]
# ThrowTheSwitch.org プロジェクトへの貢献について

👍🎉 _まず最初に、貴重なお時間を割いて貢献してくださりありがとうございます！_ 🎉👍

以下は、ThrowTheSwitch.org のプロジェクトやウェブサイト（throwtheswitch.org または GitHub 上の ThrowTheSwitch 組織）への貢献に関するガイドラインです。これらは主にガイドラインであり、厳密なルールではありません。最善の判断を用い、プルリクエストでこのドキュメント自体への変更をお気軽にご提案下さい。

---

### 目次

- [行動規範](#book-行動規範)
- [質問の仕方](#bulb-質問の仕方)
- [問題 の作成](#inbox_tray-問題-の作成)
- [機能リクエスト](#love_letter-機能リクエスト)
- [問題 のトリアージ](#mag-問題-のトリアージ)
- [プルリクエストの提出](#repeat-プルリクエストの提出)
- [コミットメッセージの書き方](#memo-コミットメッセージの書き方)
- [コードレビュー](#white_check_mark-コードレビュー)
- [コーディングスタイル](#nail_care-コーディングスタイル)
- [オリジン証明書](#medal_sports-オリジン証明書)
- [クレジット](#pray-クレジット)

---

## :book: 行動規範

[行動規範](CODE_OF_CONDUCT.md) を必ずご確認ください。この規範は常に適用です。本プロジェクトに貢献するすべての方に遵守していただくようお願いいたします。良き人でありましょう！

---

## :bulb: 質問の仕方

> **注意:** 質問のために問題を作成しないでください。公式フォーラムがありますので、質問がある場合はそちらでコミュニティからアドバイスを受けてください。

* [ThrowTheSwitch フォーラム](https://throwtheswitch.org/forums)

#### 始める前に知っておくべきこと

ThrowTheSwitch では多くのオープンソースプロジェクトをホストしています。多くのユーザーにとって Ceedling が入門編となります。Ceedling は Unity Test（柔軟なCテストフレームワーク）と CMock（C用モック生成ツール）を基盤として構築されており、他の多くのオープンソースや商用ツールを連携します。質問やアイデアはできるだけ適切なツールに向けてください。私たちも最善を尽くして案内しますが、場合によっては別のサブツールを案内することもあります。

主なプロジェクト例：

- [Ceedling](https://www.github.com/throwtheswitch/ceedling) -- Cアプリケーション（特に組み込みC）のテスト用ビルドコーディネータ
- [CMock](https://www.github.com/throwtheswitch/cmock) -- Cでスタブやモック、スケルトンを自動生成するモックツール
- [Unity](https://www.github.com/throwtheswitch/unity) -- C（特に組み込みC）向けユニットテストフレームワーク
- [MadScienceLabDocker](https://www.github.com/throwtheswitch/madsciencelabdocker) -- Ceedling をすぐに使い始めるための Docker イメージ
- [CException](https://www.github.com/throwtheswitch/cexception) -- Cでシンプルな例外処理を実現するフレームワーク

他にも多くありますが、まずはこのリストから始めてみてください。

---

## :inbox_tray:問題の作成

[問題を作成する](https://help.github.com/en/github/managing-your-work-on-github/creating-an-問題)前に、プロジェクトの最新版を使用しているか確認してください。最新版でない場合は、まずアップデートして問題が解決するか試してください。

### :beetle: バグ報告やその他の問題

問題に遭遇した際に詳細に問題を報告することは、プロジェクトへの素晴らしい貢献です。よく書かれたバグ報告は常に歓迎いたします。:v:

要するに、**自分が受け取りたいチケットを提供してください**。

- 新しい問題を作成する前に **ドキュメントを確認** してください。
- **重複問題を作成しないでください！** 既存の問題を検索し、同じ問題が報告されていないか確認してください。既存の問題があれば、追加情報をコメントしてください。「私も同じ問題があります」とだけでも、優先度の判断に役立ちます。
- 既存問題への単なる賛同は、**[リアクション](https://github.blog/2016-03-10-add-reactions-to-pull-requests-問題s-and-comments/)** を使い、コメントは控えてください。
- **問題 テンプレートを完全に記入してください。** バグ報告テンプレートには、迅速かつ効率的に対応するために必要な情報が含まれています。明確・簡潔・具体的に記載し、再現手順、スタックトレース、コンパイラエラー、ライブラリやOSのバージョン、スクリーンショット（必要な場合）など、できる限り多くの情報を提供してください。
- **[GitHubフレーバードMarkdown](https://help.github.com/en/github/writing-on-github/basic-writing-and-formatting-syntax)** を使ってください。特にコードブロックやコンソール出力はバッククォート（```）で囲ってください。可読性が向上します。

---

## :seedling: 機能リクエスト

機能リクエストも歓迎します！私たちはすべての答えを持っているわけではなく、ソフトウェアを共に作る協働体験を大切にしています。ただし、すべてのリクエストが受け入れられるとは限りません。[フィーチャークリープ](https://ja.wikipedia.org/wiki/フィーチャークリー プ)を避けたいからです。素晴らしいアイデアでも、プロジェクトの範囲外の場合もあります。受理された場合はできるだけ早く対応しますが、実装やリリースの時期は約束できません。もちろん、プルリクエストでのご協力も歓迎です！

- **重複する機能リクエストは作成しないでください。** 既存のリクエストを検索し、類似のものがあればその問題にコメントしてください。
- **問題テンプレートを完全に記入してください。** テンプレートには生産的な議論を始めるために必要な情報が含まれています。
- 提案する機能の成果や既存機能との関係を明確にし、可能であれば実装の詳細も記載してください。

---

## :mag:問題のトリアージ

バグ報告の再現や、バージョン番号や再現手順など追加情報の依頼など、問題のトリアージにもご協力いただけます。迅速な問題解決のため、どんなサポートも大変ありがたいです！

---

## :repeat: プルリクエストの提出

私たちは **プルリクエストが大歓迎です！**  
本質的な変更のために[リポジトリをフォーク](https://help.github.com/en/github/getting-started-with-github/fork-a-repo)し、[プルリクエストを作成](https://help.github.com/en/github/collaborating-with-問題s-and-pull-requests/proposing-changes-to-your-work-with-pull-requests)する前に、まず問題を立てて変更内容を議論するか、既存問題のコメントでアプローチを相談するのがベストです。

ほとんどの貢献では、最初のプルリクエストが受理・マージされた後、**プロジェクトへの招待**と**プッシュ権限**が与えられます。:tada:

*注意: すべての貢献はプロジェクトのライセンスの下でライセンスされます。*

- **小さく分けてください。** バグ修正や機能ごとに**1つのプルリクエスト**を提出してください。1つのプルリクエストには、単一のバグ修正や機能実装に関する変更のみを含めてください。**関係のないリファクタやフォーマット変更は含めないでください。** 多くの小さなプルリクエストの方が、巨大なものよりも歓迎されます。大きすぎるプルリクエストはレビューに時間がかかるか、却下される場合があります。
- **大きな変更は事前に調整を。** 大規模・複雑な変更の場合は、まず問題を立ててメンテナと戦略を相談してください。そうしないと、無駄な作業になるリスクがあります。
- **分かりやすさを優先。** コードは明確かつ簡潔に書いてください。ソースコードは一度書かれ、何度も読まれます。目的やロジックが明確でない場合はコメントを追加してください。
- **既存のコーディングスタイル・規約に従う。** コードベースのスタイルやフォーマット、命名規則に合わせてください。可能な場合はリンターで強制されます。統一性は将来の保守性を高めます。
- **テストを追加。** 可能な限りユニットテストを追加してください。既存のテストパターンに従ってください。
- **サンプルプロジェクトの更新。** 新機能を追加した場合は、サンプルプロジェクトも更新してください。
- **ドキュメントを追加。** コードコメントや既存ガイドに変更内容を記載してください。
- **CHANGELOG の更新。** すべての機能追加やバグ修正について、CHANGELOG を更新してください。問題番号やGitHubユーザー名も記載してください。（例: "- プロフィール画面のクラッシュ修正。#123 @jessesquires"）
- **リポジトリのデフォルトブランチを使う。** デフォルトブランチ（通常は `main` ですが、`dev`、`develop`、`master` の場合もあり）からブランチを切り、プルリクエストを提出してください。
- **マージコンフリクトを解消する。** [マージコンフリクトの解消方法](https://help.github.com/en/github/collaborating-with-問題s-and-pull-requests/resolving-a-merge-conflict-on-github)を参照してください。
- **CIエラーは速やかに修正。** プルリクエストがビルドやテストに失敗した場合は、修正コミットを追加してください。
- コメントを書く際は、正しい文法と句読点を使ってください。
- インデントはスペースを使い、タブは使わないでください。

---

## :memo: コミットメッセージの書き方

[素晴らしいコミットメッセージの書き方](https://chris.beams.io/posts/git-commit/)を参考にしてください。

1. 件名（サブジェクト）と本文は空行で区切る
1. 件名は50文字以内
1. 件名の先頭は大文字で始める
1. 件名の末尾にピリオドを付けない
1. 本文は約72文字で折り返す
1. 本文では**なぜ**その変更をしたかを説明する（何を・どうやってはコードが示す）
1. 必要に応じてタイトルに関連コンポーネント名や絵文字を付ける（例: "[Docs] Fix typo", "[Profile] Fix missing avatar"）

例：
:palm_tree: 素晴らしい機能の概要

必要に応じて、ここに詳細な説明を追加します。修正した問題の背景なども記載できます。コミットメッセージの本文は複数段落に分けても構いません。段落は空行で区切り、適切に折り返してください。

この変更が解決する問題や理由を説明してください。なぜこの変更が必要なのか、どんな副作用や注意点があるのかもここで説明します。

箇条書きも便利です
ハイフンの前にスペースを入れ、項目間は空行を挟みます
関連するGitHub 問題を最後に記載： Resolves: #123 See also: #456, #789


---

## :heart: 絵文字の活用

コミットコメント、問題、機能リクエストなど、絵文字でちょっとした彩りを加えましょう！以下の絵文字を機能や目的に応じて使ってみてください。

- アクション
    - :seedling: `:seedling:` 新機能の追加
    - :art: `:art:` コードのフォーマットや構造の改善
    - :racehorse: `:racehorse:` パフォーマンス改善
    - :non-potable_water: `:non-potable_water:` メモリリーク修正
    - :memo: `:memo:` ドキュメント作成
    - :bug: `:bug:` バグ修正（:beetle: :ant: :honeybee: なども可）
    - :fire: `:fire:` コードやファイルの削除
    - :green_heart: `:green_heart:` CIビルド修正
    - :white_check_mark: `:white_check_mark:` テスト追加
    - :lock: `:lock:` セキュリティ対応
    - :arrow_up: `:arrow_up:` 依存関係のアップグレード
    - :arrow_down: `:arrow_down:` 依存関係のダウングレード
    - :shirt: `:shirt:` リンター警告の修正
- プラットフォーム
    - :penguin: `:penguin:` Linux対応
    - :apple: `:apple:` macOS対応
    - :checkered_flag: `:checkered_flag:` Windows対応

---

## :white_check_mark: コードレビュー

- **コードをレビューし、作者を批判しない。** 改善点を提案し、理由を説明してください。
- **あなたはコードそのものではありません。** コードが批評されたときは個人攻撃と受け取らず、建設的に受け止めてください。
- **常に最善を尽くす。** 誰も故意にバグを書きません。最善を尽くし、失敗から学びましょう。
- このドキュメントのガイドライン違反があれば、やんわりと指摘してください。

---

## :violin: コーディングスタイル

一貫性が最も重要です。修正するファイルやプロジェクト全体の既存スタイル、フォーマット、命名規則に従ってください。これを守らないと、機能や性能の改善よりも表面的な修正にレビュー時間がかかってしまいます。

例えば、すべてのプライベートプロパティがアンダースコア `_` で始まっていれば、新しく追加するものも同様にしてください。メソッド名がキャメルケース（`thisIsMyNewMethod`）なら、`this_is_my_new_method` のように書かないでください。疑問があれば、質問するかコードベースを検索してください。

可能な場合はリンターでスタイルやフォーマットを強制します。

### C スタイルガイド

C コードは [AStyle](https://astyle.sourceforge.net/) でリントされます。

### Ruby スタイルガイド

Ruby コードは [Rubocop](https://github.com/rubocop/rubocop) でリントされます。

---

## :medal_sports: オリジン証明書（Certificate of Origin）

*Developer's Certificate of Origin 1.1*

このプロジェクトに貢献することで、私は以下を証明します：

> 1. この貢献は全体または一部を私自身が作成し、ファイルに記載されたオープンソースライセンスの下で提出する権利がある。
> 2. この貢献は、私の知る限り適切なオープンソースライセンスの下でカバーされている既存の作業に基づいており、そのライセンスの下で（全体または一部を私が作成したかどうかに関わらず）修正を加えて提出する権利がある（別のライセンスでの提出が許可されていない限り）、ファイルに記載されたオープンソースライセンスの下で提出する。
> 3. この貢献は、(1)、(2)、または(3)を証明した他の人物から直接提供され、私はそれを変更していない。
> 4. このプロジェクトおよび貢献が公開され、貢献の記録（私が提出したすべての個人情報を含む）が無期限に保持され、このプロジェクトまたは関係するオープンソースライセンスに従って再配布されることを理解し、同意する。

---

## [No Brown M&M's](https://ja.wikipedia.org/wiki/Van_Halen#契約上の要求事項)

ここまで読んでくださった皆さん、素晴らしいです！あなたは最高です。:100:

このガイドを読んで遵守していることを確認するために、**問題 やプルリクエストの冒頭にこの絵文字を含めてください**：  
:pineapple: `:pineapple:`

---

## :pray: クレジット

執筆: [@jessesquires](https://github.com/jessesquires)  
ThrowTheSwitch.org 向けアダプト: [@mvandervoord](https://github.com/mvandervoord)

**このガイドはご自身のプロジェクトでも自由にご利用ください。丸ごとフォークしたり、必要に応じてリミックスして構いません。**

*このドキュメントの多くのアイデアや文章は、以下のコミュニティの貢献に基づき、またはインスパイアされています:*

- [Alamofire](https://github.com/Alamofire/Alamofire/blob/master/CONTRIBUTING.md)
- [CocoaPods](https://github.com/CocoaPods/CocoaPods/blob/master/CONTRIBUTING.md)
- [Docker](https://github.com/moby/moby/blob/master/CONTRIBUTING.md)
- [Linux](https://elinux.org/Developer_Certificate_Of_Origin)

*これらのプロジェクトが協働を促進するために尽力していることに敬意を表します。*

---

■補足

- Markdown記法やGitHubの機能（問題、Pull Request、リアクション、コードブロック等）を活用することで、より円滑なコラボレーションが可能です。
- コミットメッセージやコードスタイルの統一は、将来的な保守性や他の貢献者との協働を大きく助けます。
- オリジン証明書（DCO）は、オープンソースプロジェクトでの貢献の法的な明確化に役立ちます。

---

■まとめ

- ThrowTheSwitch.org への貢献は、ガイドラインに従い、コミュニティの一員として協力的かつ建設的に行いましょう。
- 質問やバグ報告、機能リクエスト、プルリクエストの提出には、既存の情報確認やテンプレートの活用、Markdown記法の徹底が推奨されます。
- コードレビューやコーディングスタイルの遵守、コミットメッセージの工夫は、プロジェクトの品質向上と円滑な運営に不可欠です。
- このガイドを読んだ証として、:pineapple: を問題やPRの冒頭に入れてください。


# Contributing to a ThrowTheSwitch.org Project

👍🎉 _First off, thanks for taking the time to contribute!_ 🎉👍

The following is a set of guidelines for contributing to any of ThrowTheSwitch.org's projects or the website itself, hosted at throwtheswitch.org or ThrowTheSwitch's organization on GitHub. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

### Table Of Contents

- [Code of Conduct](#book-code-of-conduct)
- [Asking Questions](#bulb-asking-questions)
- [Opening an Issue](#inbox_tray-opening-an-issue)
- [Feature Requests](#love_letter-feature-requests)
- [Triaging Issues](#mag-triaging-issues)
- [Submitting Pull Requests](#repeat-submitting-pull-requests)
- [Writing Commit Messages](#memo-writing-commit-messages)
- [Code Review](#white_check_mark-code-review)
- [Coding Style](#nail_care-coding-style)
- [Certificate of Origin](#medal_sports-certificate-of-origin)
- [Credits](#pray-credits)

## :book: Code of Conduct

Please review our [Code of Conduct](CODE_OF_CONDUCT.md). It is in effect at all times. We expect it to be honored by everyone who contributes to this project. Be a Good Human!

## :bulb: Asking Questions

> **Note:** Please don't file an issue to ask a question. We have an official forum where the community chimes in with helpful advice if you have questions.

* [ThrowTheSwitch Forums](https://throwtheswitch.org/forums)

### What should I know before I get started?

ThrowTheSwitch hosts a number of open source projects &mdash; Ceedling is the entrypoint for many users. Ceedling is actually built upon the foundation of Unity Test (a flexible C testing framework) and CMock (a mocking tool for C) and it coordinates many other open source and proprietary tools. Please do your best to focus your ideas and questions at the correct tool. We'll do our best to help you find your way, but there will be times where we'll have to direct your attention to another subtool.

Here are some of the main projects hosted by ThrowTheSwitch.org:

 - [Ceedling](https://www.github.com/throwtheswitch/ceedling) -- Build coordinator for testing C applications, especially embedded C (and optionally your release build too!)
 - [CMock](https://www.github.com/throwtheswitch/cmock) -- Mocking tool for automatically creating stubs, mocks, and skeletons in C
 - [Unity](https://www.github.com/throwtheswitch/unity) -- Unit Testing framework for C, specially embedded C.
 - [MadScienceLabDocker](https://www.github.com/throwtheswitch/madsciencelabdocker) -- Docker image giving you a shortcut to getting running with Ceedling
 - [CException](https://www.github.com/throwtheswitch/cexception) -- An exception framework for using simple exceptions in C.

There are many more, but this list should be a good starting point.

## :inbox_tray: Opening an Issue

Before [creating an issue](https://help.github.com/en/github/managing-your-work-on-github/creating-an-issue), check if you are using the latest version of the project. If you are not up-to-date, see if updating fixes your issue first.

### :beetle: Bug Reports and Other Issues

A great way to contribute to the project is to send a detailed issue when you encounter a problem. We always appreciate a well-written, thorough bug report. :v:

In short, since you are most likely a developer, **provide a ticket that you would like to receive**.

- **Review the documentation** before opening a new issue.

- **Do not open a duplicate issue!** Search through existing issues to see if your issue has previously been reported. If your issue exists, comment with any additional information you have. You may simply note "I have this problem too", which helps prioritize the most common problems and requests. 

- **Prefer using [reactions](https://github.blog/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/)**, not comments, if you simply want to "+1" an existing issue.

- **Fully complete the provided issue template.** The bug report template requests all the information we need to quickly and efficiently address your issue. Be clear, concise, and descriptive. Provide as much information as you can, including steps to reproduce, stack traces, compiler errors, library versions, OS versions, and screenshots (if applicable).

- **Use [GitHub-flavored Markdown](https://help.github.com/en/github/writing-on-github/basic-writing-and-formatting-syntax).** Especially put code blocks and console outputs in backticks (```). This improves readability.

## :seedling: Feature Requests

Feature requests are welcome! We don't have all the answers and we truly love the collaborative experience of building software together! That being said, we cannot guarantee your request will be accepted. We want to avoid [feature creep](https://en.wikipedia.org/wiki/Feature_creep). Your idea may be great, but also out-of-scope for the project. If accepted, we'll do our best to tackle it in a timely manner, but cannot make any commitments regarding the timeline for implementation and release. However, you are welcome to submit a pull request to help!

- **Please don't open a duplicate feature request.** Search for existing feature requests first. If you find your feature (or one very similar) previously requested, comment on that issue.

- **Fully complete the provided issue template.** The feature request template asks for all necessary information for us to begin a productive conversation. 

- Be precise about the proposed outcome of the feature and how it relates to existing features. Include implementation details if possible.

## :mag: Triaging Issues

You can triage issues which may include reproducing bug reports or asking for additional information, such as version numbers or reproduction instructions. Any help you can provide to quickly resolve an issue is very much appreciated!

## :repeat: Submitting Pull Requests

We **love** pull requests! Before [forking the repo](https://help.github.com/en/github/getting-started-with-github/fork-a-repo) and [creating a pull request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/proposing-changes-to-your-work-with-pull-requests) for non-trivial changes, it is usually best to first open an issue to discuss the changes, or discuss your intended approach for solving the problem in the comments for an existing issue.

For most contributions, after your first pull request is accepted and merged, you will be [invited to the project](https://help.github.com/en/github/setting-up-and-managing-your-github-user-account/inviting-collaborators-to-a-personal-repository) and given **push access**. :tada:

*Note: All contributions will be licensed under the project's license.*

- **Smaller is better.** Submit **one** pull request per bug fix or feature. A pull request should contain isolated changes pertaining to a single bug fix or feature implementation. **Do not** refactor or reformat code that is unrelated to your change. It is better to **submit many small pull requests** rather than a single large one. Enormous pull requests will take enormous amounts of time to review, or may be rejected altogether. 

- **Coordinate bigger changes.** For large and non-trivial changes, open an issue to discuss a strategy with the maintainers. Otherwise, you risk doing a lot of work for nothing!

- **Prioritize understanding over cleverness.** Write code clearly and concisely. Remember that source code usually gets written once and read often. Ensure the code is clear to the reader. The purpose and logic should be obvious to a reasonably skilled developer, otherwise you should add a comment that explains it.

- **Follow existing coding style and conventions.** Keep your code consistent with the style, formatting, and conventions in the rest of the code base. When possible, these will be enforced with a linter. Consistency makes it easier to review and modify in the future.

- **Include test coverage.** Add unit tests when possible. Follow existing patterns for implementing tests.

- **Update the example project** if one exists to exercise any new functionality you have added.

- **Add documentation.** Document your changes with code doc comments or in existing guides.

- **Update the CHANGELOG** for all enhancements and bug fixes. Include the corresponding issue number if one exists, and your GitHub username. (example: "- Fixed crash in profile view. #123 @jessesquires")

- **Use the repo's default branch.** Branch from and [submit your pull request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request-from-a-fork) to the repo's default branch. Usually this is `main`, but it could be `dev`, `develop`, or `master`.

- **[Resolve any merge conflicts](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/resolving-a-merge-conflict-on-github)** that occur.

- **Promptly address any CI failures**. If your pull request fails to build or pass tests, please push another commit to fix it. 

- When writing comments, use properly constructed sentences, including punctuation.

- Use spaces, not tabs.

## :memo: Writing Commit Messages

Please [write a great commit message](https://chris.beams.io/posts/git-commit/).

1. Separate subject from body with a blank line
1. Limit the subject line to 50 characters
1. Capitalize the subject line
1. Do not end the subject line with a period
1. Wrap the body at _about_ 72 characters
1. Use the body to explain **why**, *not what and how* (the code shows that!)
1. If applicable, prefix the title with the relevant component name or emoji (see below. examples: "[Docs] Fix typo", "[Profile] Fix missing avatar")

```
:palm_tree: Summary of Amazing Feature Here

Add a more detailed explanation here, if necessary. Possibly give 
some background about the issue being fixed, etc. The body of the 
commit message can be several paragraphs. Further paragraphs come 
after blank lines and please do proper word-wrap.

Wrap it to about 72 characters or so. In some contexts, 
the first line is treated as the subject of the commit and the 
rest of the text as the body. The blank line separating the summary 
from the body is critical (unless you omit the body entirely); 
various tools like `log`, `shortlog` and `rebase` can get confused 
if you run the two together.

Explain the problem that this commit is solving. Focus on why you
are making this change as opposed to how or what. The code explains 
how or what. Reviewers and your future self can read the patch, 
but might not understand why a particular solution was implemented.
Are there side effects or other unintuitive consequences of this
change? Here's the place to explain them.

 - Bullet points are awesome, too

 - A hyphen should be used for the bullet, preceded
   by a single space, with blank lines in between

Note the fixed or relevant GitHub issues at the end:

Resolves: #123
See also: #456, #789
```

## :heart: Who Loves Emoji?

Commit comments, Issues, Feature Requests... they can all use a little sprucing up, right? Consider using the following emoji for a mix of function and :sparkles: dazzle!

  - actions
    - :seedling: `:seedling:` (or other plants) when growing new features. Choose your fav! :cactus: :herb: :evergreen_tree: :palm_tree: :deciduous_tree: :blossom: 
    - :art: `:art:` when improving the format/structure of the code
    - :racehorse: `:racehorse:` when improving performance
    - :non-potable_water: `:non-potable_water:` when plugging memory leaks
    - :memo: `:memo:` when writing docs
    - :bug: `:bug:` (or other insects) when fixing a bug. Maybe :beetle: :ant: or :honeybee: ?
    - :fire: `:fire:` when removing code or files
    - :green_heart: `:green_heart:` when fixing the CI build
    - :white_check_mark: `:white_check_mark:` when adding tests
    - :lock: `:lock:` when dealing with security
    - :arrow_up: `:arrow_up:` when upgrading dependencies
    - :arrow_down: `:arrow_down:` when downgrading dependencies
    - :shirt: `:shirt:` when removing linter warnings

  - platforms
    - :penguin: `:penguin:` when fixing something on Linux
    - :apple: `:apple:` when fixing something on macOS
    - :checkered_flag: `:checkered_flag:` when fixing something on Windows

## :white_check_mark: Code Review

- **Review the code, not the author.** Look for and suggest improvements without disparaging or insulting the author. Provide actionable feedback and explain your reasoning.

- **You are not your code.** When your code is critiqued, questioned, or constructively criticized, remember that you are not your code. Do not take code review personally.

- **Always do your best.** No one writes bugs on purpose. Do your best, and learn from your mistakes.

- Kindly note any violations to the guidelines specified in this document. 

## :violin: Coding Style

Consistency is the most important. Following the existing style, formatting, and naming conventions of the file you are modifying and of the overall project. Failure to do so will result in a prolonged review process that has to focus on updating the superficial aspects of your code, rather than improving its functionality and performance.

For example, if all private properties are prefixed with an underscore `_`, then new ones you add should be prefixed in the same way. Or, if methods are named using camelcase, like `thisIsMyNewMethod`, then do not diverge from that by writing `this_is_my_new_method`. You get the idea. If in doubt, please ask or search the codebase for something similar.

When possible, style and format will be enforced with a linter.

### C Styleguide

C code is linted with [AStyle](https://astyle.sourceforge.net/).

### Ruby Styleguide

Ruby code is linted with [Rubocop](https://github.com/rubocop/rubocop)

## :medal_sports: Certificate of Origin

*Developer's Certificate of Origin 1.1*

By making a contribution to this project, I certify that:

> 1. The contribution was created in whole or in part by me and I have the right to submit it under the open source license indicated in the file; or
> 1. The contribution is based upon previous work that, to the best of my knowledge, is covered under an appropriate open source license and I have the right under that license to submit that work with modifications, whether created in whole or in part by me, under the same open source license (unless I am permitted to submit under a different license), as indicated in the file; or
> 1. The contribution was provided directly to me by some other person who certified (1), (2) or (3) and I have not modified it.
> 1. I understand and agree that this project and the contribution are public and that a record of the contribution (including all personal information I submit with it, including my sign-off) is maintained indefinitely and may be redistributed consistent with this project or the open source license(s) involved.

## [No Brown M&M's](https://en.wikipedia.org/wiki/Van_Halen#Contract_riders)

If you are reading this, bravo dear user and (hopefully) contributor for making it this far! You are awesome. :100: 

To confirm that you have read this guide and are following it as best as possible, **include this emoji at the top** of your issue or pull request: :pineapple: `:pineapple:`

## :pray: Credits

Written by [@jessesquires](https://github.com/jessesquires). Lovingly adapted to ThrowTheSwitch.org by [@mvandervoord](https://github.com/mvandervoord).

**Please feel free to adopt this guide in your own projects. Fork it wholesale or remix it for your needs.**

*Many of the ideas and prose for the statements in this document were based on or inspired by work from the following communities:*

- [Alamofire](https://github.com/Alamofire/Alamofire/blob/master/CONTRIBUTING.md)
- [CocoaPods](https://github.com/CocoaPods/CocoaPods/blob/master/CONTRIBUTING.md)
- [Docker](https://github.com/moby/moby/blob/master/CONTRIBUTING.md)
- [Linux](https://elinux.org/Developer_Certificate_Of_Origin)

*We commend them for their efforts to facilitate collaboration in their projects.*
