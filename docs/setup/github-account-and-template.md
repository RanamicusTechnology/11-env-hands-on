<!--
Copyright 2026 Ranamicus Technology LLC. All rights reserved.
-->

# GitHubアカウント、テンプレート、ローカルGitの準備

## 目的

GitHubアカウントとローカルのGit／Bash環境を準備し、公開テンプレートから受講者本人が所有する演習用リポジトリを作成してcloneする。

## 前提とローカル必須条件

- ハンズオン本線では、受講者本人の個人GitHubアカウントをOwnerにする。
- 公開テンプレートは[`RanamicusTechnology/11-env-hands-on`](https://github.com/RanamicusTechnology/11-env-hands-on)を使用する。
- forkではなく、テンプレートから独立した新しいリポジトリを作成する。
- ローカルPCで必要なのはGitとBashである。
- Docker、Terraform、AnsibleはローカルPCへ導入しなくてよい。CIと使い捨てUT環境面はGitHub-hosted runner上で実行する。

| OS | 標準の準備 |
| --- | --- |
| Windows | [Git for Windows](https://git-scm.com/install/windows.html)をインストールし、Git Bashを使用する。 |
| macOS／Linux | 利用可能なterminalとGitを使用する。Bashまたは同等のBash環境でコマンドを実行する。 |

以降の`bash`、`git`コマンドは、WindowsではGit Bash、macOS／Linuxでは利用可能なBash環境で実行する。PowerShell専用の手順ではない。

## GitHubプラン、Owner、Visibility

| Owner | プラン | Public | Private |
| --- | --- | ---: | ---: |
| 個人アカウント | GitHub Free | 本線対応 | 本線非対応 |
| 個人アカウント | GitHub Pro | 対応 | 対応 |
| Organization | Team／Enterprise等 | 補足扱い | 補足扱い |

GitHub FreeではPublicリポジトリを使用する。GitHub ProではPublicまたはPrivateを選択できる。Organization所有はハンズオン本線の対象外であり、利用する場合はOrganizationのプラン、権限、ポリシーに従う。

## Publicリポジトリを作成する前の注意

Publicリポジトリを選ぶ場合は、作成前に次を確認する。

- secret、token、パスワード、秘密鍵を登録しない。
- 個人情報、顧客情報、業務情報を登録しない。
- 実在システムの設定値や認証情報を流用しない。
- 教材用ダミー情報だけを使用する。
- Publicリポジトリは第三者から閲覧、clone、forkできる。
- 一度公開した情報は、後から削除しても完全には回収できない。

Publicであることは、この教材がオープンソースとして自由に再利用・再配布できることを意味しない。

## 1. GitHubアカウントを準備する

1. GitHubアカウントを持っていない場合は、GitHubの[Sign up](https://github.com/signup)を開く。
2. 画面の案内に従って個人アカウントを作成し、登録メールアドレスの確認を完了する。
3. [GitHub](https://github.com/)へ、受講に使う個人アカウントでサインインする。
4. 既にアカウントを持っている場合は、サインインしているアカウントだけを確認して次へ進む。

## 2. LICENSEを確認する

公開テンプレートから演習用リポジトリを作成する前に、Repositoryルートの日本語正文
[`LICENSE`](../../LICENSE)を読み、条件へ同意する。参考英訳は
[`LICENSE.en.md`](../../LICENSE.en.md)で確認できる。

Eligible LearnerがTemplateからExercise Repositoryを作成すること、教材を演習用にclone
すること、または演習のために教材を変更することは、`LICENSE`への同意を示す行為である。
これらの追加的な教育利用権を使う前に、`LICENSE`への同意が必要となる。適用法令上、
単独で有効に同意できない場合は、法定代理人その他適用法令上権限を有する者の同意を
得た場合に限り、追加的な教育利用権を行使できる。

GitHubの利用規約その他のPlatform Termsまたは法令から直接与えられる権利に基づく
単なる閲覧またはGitHubの標準機能によるforkだけでは、`LICENSE`への同意を示すものでは
ない。Eligible Learnerでない者には、本LICENSEによる追加的な許諾は付与されず、Platform
Termsまたは法令により直接認められる範囲を超えて教材を利用することはできない。

## 3. テンプレートから演習用リポジトリを作成する

ここまではGitHub Web UIで操作する。

1. 公開テンプレート[`RanamicusTechnology/11-env-hands-on`](https://github.com/RanamicusTechnology/11-env-hands-on)を開く。
2. ファイル一覧の上にある`Use this template`を選択する。
3. `Create a new repository`を選択する。
4. `Owner`に、受講者本人の個人GitHubアカウントを指定する。
5. `Repository name`へ演習用リポジトリ名を入力する。
6. `Description`は任意である。必要なら、このコースの演習用リポジトリであることを記載する。
7. `Visibility`を選択する。
   - GitHub Free: `Public`
   - GitHub Pro: `Public`または`Private`
8. `Include all branches`は選択しない。
9. `Create repository from template`を選択する。
10. 作成されたリポジトリのURLとOwnerを確認する。

作成後は、次を確認する。

- URLのOwner部分が受講者本人の個人GitHubアカウント名である。
- テンプレート元とは異なる独立したリポジトリで、fork元の表示がない。
- [README](../../README.md)、`docs/`、[Issue Form](../../.github/ISSUE_TEMPLATE/change-request.yml)、[Pull Requestテンプレート](../../.github/pull_request_template.md)が存在する。
- `Actions`タブへアクセスできる。
- 完成版PR CIが最初から有効になっていない。

## 4. Repository設定Phase Aを行う

作成した演習用リポジトリのWeb UIで、[リポジトリ設定手順](repository-settings.md)のPhase Aを行う。GitHub Actions、workflow permissions、merge方式、`main-protection` Rulesetの基本設定を保存する。

5.1では`pr-ci-gate`をまだRequired checkへ登録せず、Rulesetを`Disabled`で保存する。Phase Bは5.2の初回`pr-ci-gate`成功後に行う。

## 5. GitとBashを確認する

ここからローカルPCのGit Bashまたは同等のBashへ移る。

```bash
git --version
bash --version
```

Windowsでコマンドが見つからない場合はGit for WindowsのインストールとGit Bashの起動を確認する。macOS／Linuxでは、利用中OSの標準手順でGitを準備する。

## 6. 自分の演習用リポジトリをcloneする

公開テンプレートではなく、手順3で自分のアカウントに作成した演習用リポジトリを、ローカルにcloneする。`<account>`と`<repository>`は、自分のOwner名とリポジトリ名へ置き換える。

```bash
git clone https://github.com/<account>/<repository>.git
cd <repository>
git status
```

`cd <repository>`後のディレクトリがRepositoryルートである。以降の教材コマンドは、特に記載がない限りこのRepositoryルートで実行する。

`git status`で、現在のbranchが`main`であり、working treeがcleanであることを確認する。初回clone直後に自分で作成していない変更や未追跡ファイルが表示された場合は、5.2へ進む前に原因を確認する。

## 操作の導線

| 順序 | 操作場所 | 操作 |
| --- | --- | --- |
| 1 | GitHub Web UI | `LICENSE`を確認して同意する。 |
| 2 | GitHub Web UI | Templateから自分の演習用リポジトリを作成する。 |
| 3 | GitHub Web UI | Repository設定Phase Aを行う。 |
| 4 | ローカルGit／Bash | 自分の演習用リポジトリをcloneし、Repositoryルートへ移動する。 |
| 5 | GitHub Web UIとローカルGit／Bash | [Lesson 5.2](../lessons/5.2-change-and-pipeline-setup.md)でIssue、branch、段階patch、Draft Pull Requestをつなぐ。 |

## 完了チェック

- [ ] 受講に使う個人GitHubアカウントへサインインできる。
- [ ] 追加的な教育利用権を使う前に`LICENSE`を読み、同意した。
- [ ] 単独で有効に同意できない場合は、必要な法定代理人等の同意を得た。
- [ ] Public利用時の注意を確認した。
- [ ] 公開テンプレートから、受講者本人がOwnerの独立した演習用リポジトリを作成した。
- [ ] `Include all branches`を選択していない。
- [ ] GitHub ActionsとRepository設定Phase Aを確認した。
- [ ] WindowsではGit for WindowsとGit Bash、macOS／LinuxではterminalとGitを準備した。
- [ ] 自分の演習用リポジトリをHTTPSでcloneした。
- [ ] Repositoryルートへ移動し、`git status`がcleanである。
- [ ] Docker、Terraform、Ansibleのローカル導入は必須でないことを確認した。

完了したら、[Lesson 5.1](../lessons/5.1-overview-and-setup.md)の完了チェックを確認し、Lesson 5.2へ進む。
