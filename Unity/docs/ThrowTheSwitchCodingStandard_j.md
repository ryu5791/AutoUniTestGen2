[和訳]

# ThrowTheSwitch.org コーディング規約

こんにちは。ThrowTheSwitch.org のコーディング規約へようこそ。
私たちは、貢献者のコードを統一感のあるものにするため、基本的にこれらの規約に従うよう努めています（ダジャレも含めて）。
規約が守られていない箇所を見つけることもあるかもしれませんが、私たちも完璧ではありません。
もしそうした点に気付いたら丁寧にご指摘ください。私たちもあなたの指摘に丁寧に対応するよう努めます。 

---

## なぜコーディング規約が必要なのか？

一貫性を持たせることで、コードが理解しやすくなります。
私たちは規約をシンプルに保つよう心がけています。なぜなら、理解できるものしか守ってもらえないと考えているからです。
どうか最善を尽くしてください。

---

## 私たちの哲学

構文の詳細に入る前に、これらのツールに対する私たちのビジョンについて少しお話しします。
私たちはC開発者であり、組み込みソフトウェア開発者です。
これらのツールはあらゆるCコードのテストに最適ですが、組み込みソフトウェア向けに作られているため、コンパイラの癖にも寛容です。
世の中には本当に多くの「癖のある」コンパイラが存在します。
ここで言う「癖」とは、「標準に従わず、好き勝手に実装されている」ことを指します。

私たちの哲学は「可能な限りすべてのコンパイラをサポートする」ことです。
多くの場合、これは標準（主にC89…これがほぼ常に互換性のある良い落とし所です）に準拠したCコードを書くことを意味します。
しかし同時に、一般的でないものや標準に準拠していないものにも寛容であることも意味します。
標準型のサイズを上書きする設定や、Unityが特定の標準ライブラリ関数を使わないようにする設定も用意しています。
Unityは多くの部分が設定可能であり、その過程であまりにも醜くならないよう努力しています。

同様に、Cコードをパースする私たちのツールも最善を尽くしています。
完全なCパーサーではありません（まだ）し、仮にそうであっても、gcc拡張や `@0x1000` のような非標準の記法も受け入れる必要があります。
なぜなら「すべてが Just Work™（とにかく動く）」ことを目指しているからです。

Just Work™ について言えば、これが私たちのもう一つの哲学です。
つまり、すべての設定オプションに論理的なデフォルト値を持たせるよう最善を尽くしています。
シンプルなコンパイラやターゲットで作業している場合、ほとんど設定しなくても済むようにしています。
ツールができるだけ自動で推測し、必要な場合のみユーザーが上書きできるようにしています。

---

## 名前付けについて

名前付けについてお話しましょう。
プログラミングは「名前付け」がすべてです。
ファイル、関数、変数など、あらゆるものに名前を付けます。
常に最良の名前が見つかるわけではありませんが、*そのものが呼ばれたがっている名前* を見つける努力をしています。

名前付けの際は、以下の優先順位で考えます（上ほど重要ですが、可能な限りすべて満たします）：

1. 読みやすいこと
2. 説明的であること
3. 一貫性があること
4. 記憶に残ること

### 読みやすさ

私たちはコードを「読む」ことを重視します。
そのため、自然に読める名前や流れを好みます。
二重否定や、分かりにくい略語（一般的なものを除く）は避けるようにしています。

### 説明的であること

特に関数や変数には説明的な名前を付けるのが好きです。
適切な名前を見つけることは重要な作業です。
そのため、私たちのコードでは平均より少し長めの名前が多いかもしれませんが、理解しやすさのためなら多少のタイピング量は気にしません。

このルールには2つの例外があり、私たちは可能な限り厳格に守っています：

1つ目は、ハンガリアン記法（型情報を名前に埋め込む方式）などは、説明的ではありますが、一般的な開発者にとっては可読性を損なうため、避けるべきだと考えています。

2つ目は、ループカウンタや一時的なローカル変数など、用途が明白な場合です。
この場合、複雑な名前にする必要はなく、`i`, `j`, `k` などの方が適しています。
ただし、より説明的な名前がアルゴリズムの理解を助ける場合は例外です。

### 一貫性

一貫性は大切ですが、過度にこだわるわけではありません。
設定用マクロの命名には一貫性を持たせるよう努めています（例：`UNITY_EXCLUDE_BLAH` や `UNITY_USES_BLAH` など）。
これにより、ユーザーが各マクロの詳細を覚える手間が減ります。

### 記憶に残ること

上記の原則に反しない範囲で、記憶に残る名前を付けるようにしています。
単に説明的なだけでなく、ユニークで印象的な名前を目指します。
例えば、`preprocess` よりも `preprocessinator`、リリース時のタスクを実行するモジュールなら `release_invoker` など。
ただし、やりすぎには注意し、あくまで説明的であることを優先します。

---

## C および C++ の詳細

スタイル論争（タブかスペースか、何スペースか、波括弧の位置など）には深入りしたくありません。
これらは永遠に決着しない問題です。

私たちは自分たちの好みでスタイルを決めています。
もしプロジェクトに貢献したい場合（ぜひお願いします！）、できるだけ同じスタイルに従ってください。
少しだけ我慢していただければ幸いです。

### C/C++ の空白（インデント）

Cスタイルではスペースを使い、インデントは4スペースです。
2のべき乗で、ワイドスクリーンでも見やすいからです。
ただし、マクロや関数引数などで折り返す場合は、さらにインデントして整列させます。

```c
if (stuff_happened)
{
    do_something();
}

```

### C/C++ における大文字・小文字の規則（Case in C/C++）

- **ファイル名**：すべて小文字＋アンダースコア（例: `my_file.c`）
- **変数名**：すべて小文字＋アンダースコア（例: `my_variable`）
- **マクロ名**：すべて大文字＋アンダースコア（例: `MY_MACRO`）
- **typedef名**：すべて大文字＋アンダースコア、かつ末尾に `_T` を付ける（例: `MY_TYPE_T`）
- **関数名**：キャメルケース。通常は `ModuleName_FuncName` の形式（例: `Timer_Start`）
- **定数・グローバル変数**：キャメルケース（例: `MaxValue`、`GlobalCounter`）

---

### C/C++ における波括弧（ブレース）の使い方（Braces in C/C++）

- **左波括弧（{）は宣言の次の行に置く。**
- **右波括弧（}）は左波括弧の真下に置く。**
- **波括弧で囲まれた中身は1段階インデントする。**
- **たとえ1行だけの処理でも、必ず波括弧を使う。**

#### コード例

```c
while (blah)
{
    // このように。たとえ1行でも波括弧を使います。
}

```

### C/C++ のコメントについて

私たちが嫌いなものは何かご存知ですか？  
それは「昔ながらのCのブロックコメント（`/* ... */`）」です。  
ですが、私たちはそれを使っています。  
なぜなら、私たちの目標はあらゆるコンパイラ、特に組み込み用コンパイラをサポートすることだからです。  
今でも、古いブロックコメントしかサポートしないCコンパイラが存在します。  
そのため、私たちはこの形式を使っています。  
申し訳ありません。私たちも見た目が良くないと思っています。

---

### Ruby の詳細

Rubyにコーディング標準なんて本当にあるのでしょうか？  
Rubyは非常に自由な形式の言語なので、1つの方法に従うべきだと提案するのは、ほとんど冒涜的にさえ感じます！  
ここでは本当に簡潔にまとめます。

#### Ruby の空白（インデント）

私たちのRubyスタイルはスペースを使い、インデントは1レベルにつき2スペースです。  
これは2のべき乗であり、Rubyのコンパクトなスタイルによく合います。  
それ以上の理由はありません。  
折り返しが発生した場合はこのルールを破り、きれいに列を揃えるためにさらにインデントします。

#### Ruby の大文字・小文字規則

- ファイル名：すべて小文字＋アンダースコア
- 変数名：すべて小文字＋アンダースコア
- クラス、モジュールなど：キャメルケース
- 関数名：すべて小文字＋アンダースコア
- 定数：すべて大文字＋アンダースコア

---

## ドキュメント

本当に？と思うかもしれませんが、私たちはMarkdownを使い、PDFファイルも好んで使います。  
PDFは見た目が良く、持ち運びもしやすいからです。  
これで十分でしょう？

*この内容やその他の最新情報は [ThrowTheSwitch.org](https://throwtheswitch.org) でご確認ください。*

---



# ThrowTheSwitch.org Coding Standard

Hi.
Welcome to the coding standard for ThrowTheSwitch.org.
For the most part, we try to follow these standards to unify our contributors' code into a cohesive unit (puns intended).
You might find places where these standards aren't followed.
We're not perfect. Please be polite where you notice these discrepancies and we'll try to be polite when we notice yours.

;)

## Why Have A Coding Standard?

Being consistent makes code easier to understand.
We've tried to keep our standard simple because we also believe that we can only expect someone to follow something that is understandable.
Please do your best.

## Our Philosophy

Before we get into details on syntax, let's take a moment to talk about our vision for these tools.
We're C developers and embedded software developers.
These tools are great to test any C code, but catering to embedded software made us more tolerant of compiler quirks.
There are a LOT of quirky compilers out there.
By quirky I mean "doesn't follow standards because they feel like they have a license to do as they wish."

Our philosophy is "support every compiler we can".
Most often, this means that we aim for writing C code that is standards compliant (often C89... that seems to be a sweet spot that is almost always compatible).
But it also means these tools are tolerant of things that aren't common.
Some that aren't even compliant.
There are configuration options to override the size of standard types.
There are configuration options to force Unity to not use certain standard library functions.
A lot of Unity is configurable and we have worked hard to make it not TOO ugly in the process.

Similarly, our tools that parse C do their best.
They aren't full C parsers (yet) and, even if they were, they would still have to accept non-standard additions like gcc extensions or specifying `@0x1000` to force a variable to compile to a particular location.
It's just what we do, because we like everything to Just Work™.

Speaking of having things Just Work™, that's our second philosophy.
By that, we mean that we do our best to have EVERY configuration option have a logical default.
We believe that if you're working with a simple compiler and target, you shouldn't need to configure very much... we try to make the tools guess as much as they can, but give the user the power to override it when it's wrong.

## Naming Things

Let's talk about naming things.
Programming is all about naming things.
We name files, functions, variables, and so much more.
While we're not always going to find the best name for something, we actually put a bit of effort into finding *What Something WANTS to be Called*™.

When naming things, we follow this hierarchy, the first being the most important to us (but we do all four when possible):

1. Readable
2. Descriptive
3. Consistent
4. Memorable

### Readable

We want to read our code.
This means we like names and flow that are more naturally read.
We try to avoid double negatives.
We try to avoid cryptic abbreviations (sticking to ones we feel are common).

### Descriptive

We like descriptive names for things, especially functions and variables.
Finding the right name for something is an important endeavour.
You might notice from poking around our code that this often results in names that are a little longer than the average.
Guilty.
We're okay with a bit more typing if it means our code is easier to understand.

There are two exceptions to this rule that we also stick to as religiously as possible:

First, while we realize hungarian notation (and similar systems for encoding type information into variable names) is providing a more descriptive name, we feel that (for the average developer) it takes away from readability and is to be avoided.

Second, loop counters and other local throw-away variables often have a purpose which is obvious.
There's no need, therefore, to get carried away with complex naming.
We find i, j, and k are better loop counters than loopCounterVar or whatnot.
We only break this rule when we see that more description could improve understanding of an algorithm.

### Consistent

We like consistency, but we're not really obsessed with it.
We try to name our configuration macros in a consistent fashion... you'll notice a repeated use of UNITY_EXCLUDE_BLAH or UNITY_USES_BLAH macros.
This helps users avoid having to remember each macro's details.

### Memorable

Where ever it doesn't violate the above principles, we try to apply memorable names.
Sometimes this means using something that is simply descriptive, but often we strive for descriptive AND unique... we like quirky names that stand out in our memory and are easier to search for.
Take a look through the file names in Ceedling and you'll get a good idea of what we are talking about here.
Why use preprocess when you can use preprocessinator?
Or what better describes a module in charge of invoking tasks during releases than release_invoker?
Don't get carried away.
The names are still descriptive and fulfill the above requirements, but they don't feel stale.

## C and C++ Details

We don't really want to add to the style battles out there.
Tabs or spaces?
How many spaces?
Where do the braces go?
These are age-old questions that will never be answered... or at least not answered in a way that will make everyone happy.

We've decided on our own style preferences.
If you'd like to contribute to these projects (and we hope that you do), then we ask if you do your best to follow the same.
It will only hurt a little. We promise.

### Whitespace in C/C++

Our C-style is to use spaces and to use 4 of them per indent level.
It's a nice power-of-2 number that looks decent on a wide-screen.
We have no more reason than that.
We break that rule when we have lines that wrap (macros or function arguments or whatnot).
When that happens, we like to indent further to line things up in nice tidy columns.

```C
    if (stuff_happened)
    {
        do_something();
    }
```

### Case in C/C++

- Files - all lower case with underscores.
- Variables - all lower case with underscores
- Macros - all caps with underscores.
- Typedefs - all caps with underscores. (also ends with _T).
- Functions - camel cased. Usually named ModuleName_FuncName
- Constants and Globals - camel cased.

### Braces in C/C++

The left brace is on the next line after the declaration.
The right brace is directly below that.
Everything in between in indented one level.
If you're catching an error and you have a one-line, go ahead and to it on the same line.

```C
    while (blah)
    {
        //Like so. Even if only one line, we use braces.
    }
```

### Comments in C/C++

Do you know what we hate?
Old-school C block comments.
BUT, we're using them anyway.
As we mentioned, our goal is to support every compiler we can, especially embedded compilers.
There are STILL C compilers out there that only support old-school block comments.
So that is what we're using.
We apologize.
We think they are ugly too.

## Ruby Details

Is there really such thing as a Ruby coding standard?
Ruby is such a free form language, it seems almost sacrilegious to suggest that people should comply to one method!
We'll keep it really brief!

### Whitespace in Ruby

Our Ruby style is to use spaces and to use 2 of them per indent level.
It's a nice power-of-2 number that really grooves with Ruby's compact style.
We have no more reason than that.
We break that rule when we have lines that wrap.
When that happens, we like to indent further to line things up in nice tidy columns.

### Case in Ruby

- Files - all lower case with underscores.
- Variables - all lower case with underscores
- Classes, Modules, etc - Camel cased.
- Functions - all lower case with underscores
- Constants - all upper case with underscores

## Documentation

Egad.
Really?
We use markdown and we like PDF files because they can be made to look nice while still being portable.
Good enough?

*Find The Latest of This And More at [ThrowTheSwitch.org][]*

[ThrowTheSwitch.org]: https://throwtheswitch.org
