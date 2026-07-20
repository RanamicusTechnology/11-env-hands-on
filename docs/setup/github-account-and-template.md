<!--
Copyright 2026 Ranamicus Technology LLC. All rights reserved.
-->

# GitHubアカウントとテンプレートリポジトリの準備

## 目的

GitHubアカウントを準備し、公開テンプレートから受講者本人が所有する演習用リポジトリを作成する。

## 前提

- ハンズオン本線では、受講者本人の個人GitHubアカウントをOwnerにする。
- 公開テンプレートは[`RanamicusTechnology/11-env-hands-on`](https://github.com/RanamicusTechnology/11-env-hands-on)を使用する。
- forkではなく、テンプレートから独立した新しいリポジトリを作成する。
- ローカルDocker環境は必須ではない。CIと使い捨てUT環境面はGitHub-hosted runner上で実行する。

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
- リポジトリ名を知らない人からも、検索結果、ユーザーやOrganizationのページ、リンク共有などを通じて発見される可能性がある。
- 一度公開した情報は第三者が取得済みの可能性があり、後から削除しても完全には回収できない。

Publicであることは、この教材がオープンソースとして自由に再利用・再配布できることを意味しない。

## 1. GitHubアカウントを準備する

1. GitHubアカウントを持っているか確認する。
2. 持っていない場合は、GitHubの[Sign up](https://github.com/signup)を開き、画面の案内に従って個人アカウントを作成する。
3. GitHubから届く案内に従い、登録メールアドレスの確認を完了する。
4. [GitHub](https://github.com/)へサインインする。
5. 既にアカウントを持っている場合は、受講に使う個人アカウントでサインインしていることを確認し、次へ進む。

## 2. テンプレートから演習用リポジトリを作成する

1. 公開テンプレート[`RanamicusTechnology/11-env-hands-on`](https://github.com/RanamicusTechnology/11-env-hands-on)を開く。
2. ファイル一覧の上にある`Use this template`を選択する。
3. `Create a new repository`を選択する。
4. `Owner`に、受講者本人の個人GitHubアカウントを指定する。
5. `Repository name`へ演習用リポジトリ名を入力する。
6. `Description`は任意である。必要なら、このコースの演習用リポジトリであることを記載する。
7. `Visibility`を選択する。
   - GitHub Free: `Public`
   - GitHub Pro: `Public`または`Private`
8. `Include all branches`は選択しない。テンプレートのdefault branchにある受講開始時点の資源だけを使用する。
9. `Create repository from template`を選択する。
10. 作成されたリポジトリのURLとOwnerを確認する。

## 3. 作成後の状態を確認する

作成した演習用リポジトリで、次を確認する。

- URLのOwner部分が受講者本人の個人アカウント名になっている。
- テンプレート元とは異なる、独立したリポジトリである。
- リポジトリ名の近くにfork元を示す表示がない。
- [README](../../README.md)と`docs/`が存在する。
- [Issue Form](../../.github/ISSUE_TEMPLATE/change-request.yml)と[Pull Requestテンプレート](../../.github/pull_request_template.md)が存在する。
- レクチャーで使うアプリ、IaC、テスト、演習用scriptなどのスターター資源が存在する。
- `Actions`タブへアクセスできる。
- 受講開始時点の資源だけが存在し、完成後のPR CIが最初から有効になっていない。

## 完了チェック

- [ ] 受講に使う個人GitHubアカウントへサインインできる。
- [ ] 登録メールアドレスの確認が完了している。
- [ ] Public利用時の注意を確認した。
- [ ] 公開テンプレートから演習用リポジトリを作成した。
- [ ] Ownerは受講者本人の個人GitHubアカウントである。
- [ ] GitHub FreeではPublic、GitHub Proでは選択したVisibilityになっている。
- [ ] `Include all branches`を選択していない。
- [ ] forkではなく、テンプレート元から独立したリポジトリである。
- [ ] README、docs、Issue Form、Pull Requestテンプレート、スターター資源を確認した。
- [ ] `Actions`タブへアクセスできる。

完了したら、[リポジトリ設定手順](repository-settings.md)のPhase Aへ進む。
