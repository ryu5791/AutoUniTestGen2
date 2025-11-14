[和訳]
# Meson ジェネレーター - テストランナー

Unity を Ceedling と一緒に使う大きな利点の一つは、Ceedling がテストランナーの自動生成をすべて面倒見てくれることです。しかし、Ceedling を使わない場合は、この作業を自分で行う必要があります。

Unity でこの処理を行う方法は、`generate_test_runner.rb` という Ruby スクリプトを使ってテストランナーを生成します。このスクリプトに `test_example.c` のようなテストファイルを渡すと、`test_example_Runner.c` を生成します。このファイルには `main` 関数やその他便利な処理が含まれます。

手動でこのスクリプトを実行しなくても済むように、Meson 用のジェネレーターが用意されており、ランナーを自動的に生成します。Meson では通常、Unity をサブプロジェクトとして利用し、親プロジェクトからこのジェネレーターにアクセスする形になります。

例えば、ジェネレーターを取得するには以下のように記述します：

```python
unity_proj = subproject('unity')
runner_gen = unity_proj.get_variable('gen_test_runner')
ジェネレーターを取得したら、テストファイルの絶対パスを渡す必要があります。これは Meson のサブプロジェクトでのパスの扱いにバグがあるためのようです。絶対パスは meson.source_root() で取得できるので、次のように記述できます：

test_runner = meson.source_root() / 'test/test_example.c'

```

このようにして得られた test_runner を、通常の依存関係としてビルドに含めることができます。Meson は各ビルドターゲットごとにプライベートディレクトリ内にテストランナーを生成します。

このジェネレーターはビルドの一部としてのみ使うことを想定しているため、ビルド後にテストランナーを参照したい場合はジェネレーターを利用できません。



# Meson Generator - Test Runner

One of the really nice things about using Unity with Ceedling is that Ceedling takes care of generating all of the test runners automatically. If you're not using Ceedling though, you'll need to do this yourself.

The way this is done in Unity is via a Ruby script called `generate_test_runner.rb`. When given a test file such as `test_example.c`, the script will generate `test_example_Runner.c`, which provides the `main` method and some other useful plumbing.

So that you don't have to run this by hand, a Meson generator is provided to generate the runner automatically for you. Generally with Meson, you would use Unity as a subproject and you'd want to access the generator from the parent.

For example, to get the generator you can use:

    unity_proj = subproject('unity')
    runner_gen = unity_proj.get_variable('gen_test_runner')

Once you have the generator you need to pass it the absolute path of your test file. This seems to be a bug in how the paths work with subprojects in Meson. You can get the full path with `meson.source_root()`, so you could do:

    test_runner = meson.source_root() / 'test/test_example.c'

You can then include `test_runner` as a normal dependency to your builds. Meson will create the test runner in a private directory for each build target. It's only meant to be used as part of the build, so if you need to refer to the runner after the build, you won't be able to use the generator.