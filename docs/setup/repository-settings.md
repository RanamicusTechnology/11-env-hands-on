<!--
Copyright 2026 Ranamicus Technology LLC. All rights reserved.
-->

# リポジトリ設定手順

## 目的

GitHub Actionsの権限、merge方式、main branch用Rulesetを設定し、5.2の初回PR CI成功後に`pr-ci-gate`をRequired status checkへ接続する。

## 前提

- [GitHubアカウントとテンプレートリポジトリの準備](github-account-and-template.md)が完了している。
- 演習用リポジトリのOwnerは受講者本人の個人GitHubアカウントである。
- 受講者は演習用リポジトリの`Settings`を変更できる。

## GitHubプラン、Owner、Visibilityの制約

| Owner | プラン | Public | Private |
| --- | --- | ---: | ---: |
| 個人アカウント | GitHub Free | 本線対応 | 本線非対応 |
| 個人アカウント | GitHub Pro | 対応 | 対応 |
| Organization | Team／Enterprise等 | 補足扱い | 補足扱い |

GitHub FreeではPublicリポジトリを使用する。GitHub ProではPublicまたはPrivateを選択できる。Organization所有を利用する場合は、Organizationのプラン、権限、上位ポリシーに従うため、本線手順とは分けて扱う。

## Phase A: レクチャー5.1で行う設定

Phase Aでは、Required status check以外を設定したRulesetを`Disabled`で保存する。`pr-ci-gate`はまだ実行されていないため、この段階ではRequired status checkへ追加しない。

### 1. GitHub Actionsの利用可否を確認する

1. 演習用リポジトリで`Settings`を開く。
2. 左サイドバーの`Actions`を開き、`General`を選択する。
3. `Actions permissions`でGitHub Actionsが無効になっていないことを確認する。
4. 利用を制限している場合は、教材workflowが参照するGitHub公式Actionと許可済みの第三者Actionを実行できることを確認する。

### 2. Workflow permissionsを確認する

1. 同じ`Settings` → `Actions` → `General`画面の`Workflow permissions`を確認する。
2. `Read repository contents and packages permissions`を選択する。
3. `Allow GitHub Actions to create and approve pull requests`は有効にしない。
4. 設定を変更した場合は`Save`を選択する。

PR CIはworkflow内の`permissions`で必要なread権限だけを宣言する。GitHub Release、Draft Release、GHCRへのwrite権限は与えず、`pull_request_target`も使用しない。

### 3. merge方式を設定する

1. `Settings`の`General`を開く。
2. `Pull Requests`までスクロールする。
3. `Allow squash merging`を有効にする。
4. `Allow merge commits`を有効にする。
5. `Allow rebase merging`を無効にする。

### 4. main branch用Rulesetの基本設定を保存する

1. `Settings`を開く。
2. 左サイドバーの`Rules`を開き、`Rulesets`を選択する。
3. `New ruleset` → `New branch ruleset`を選択する。
4. `Ruleset name`へ`main-protection`と入力する。
5. `Enforcement status`は`Disabled`を選択する。
6. `Bypass list`は空のままにする。管理者や自分自身を追加しない。
7. `Target branches`でdefault branch、またはbranch名`main`を対象にする。
8. `Restrict deletions`を有効にする。
9. `Require a pull request before merging`を有効にする。
10. Required approvalsは`0`のままにする。個人演習のため、承認者を必須にしない。
11. `Block force pushes`を有効にする。
12. `Require status checks to pass before merging`は有効にしない。
13. `Create`を選択して保存する。

受講者自身はリポジトリ管理者であるため、Rulesetそのものを編集、無効化、削除できる。演習中は品質ゲートを迂回するための変更を行わない。

## Phase A完了チェック

- [ ] GitHub Actionsが利用可能である。
- [ ] Workflow permissionsはreadを基本とし、Pull Requestの作成・承認権限を与えていない。
- [ ] Squash mergeとMerge commitが有効、Rebase mergeが無効である。
- [ ] main branch用Rulesetが作成されている。
- [ ] RulesetのBypass listが空である。
- [ ] main branchの削除とforce pushを許可しない設定になっている。
- [ ] `Require a pull request before merging`が有効である。
- [ ] Required approvalsは`0`である。
- [ ] Required status checkはまだ設定していない。
- [ ] Enforcement statusは`Disabled`である。

## Phase B: レクチャー5.2の初回PR CI成功後に行う設定

5.2でIssue、branch、Draft Pull Requestを作成し、最小PR CIを実行する。Actionsのworkflow runで`pr-ci-gate`が初めてsuccessになったことを確認してから、次を行う。

1. `Actions`タブで対象workflow runを開き、`pr-ci-gate` jobがsuccessであることを確認する。
2. `Settings` → `Rules` → `Rulesets`を開く。
3. Phase Aで作成した`main-protection`を選択する。
4. `Require status checks to pass before merging`を有効にする。
5. Required status checkとして`pr-ci-gate`を検索して追加する。
6. `Require branches to be up to date before merging`を有効にする。
7. `Enforcement status`を`Active`へ変更する。
8. Bypass listが空で、`Restrict deletions`、`Require a pull request before merging`、`Block force pushes`が有効であることを再確認する。
9. `Save changes`を選択する。
10. Draft Pull Requestのmerge欄で、`pr-ci-gate`とbranch更新条件がmerge条件として表示されることを確認する。

Required status checkは`pr-ci-gate`の1本だけにする。`pr-ci-gate`は解析やテストを再実行せず、PR CI内の品質関連job、必須output、Artifact upload、cleanup、残存確認を集約する。

## Phase B完了チェック

- [ ] `pr-ci-gate`がsuccessになったworkflow runを確認した。
- [ ] Required status checkは`pr-ci-gate`の1本だけである。
- [ ] `Require branches to be up to date before merging`が有効である。
- [ ] Enforcement statusは`Active`である。
- [ ] Bypass listは空である。
- [ ] mainへの直接変更はRulesetにより制限される。
- [ ] `pr-ci-gate`が失敗、未完了、または最新mainを取り込む前の結果だけではmergeできない。

## 設定できない場合の確認先

- `Settings`が表示されない場合は、受講者本人の個人アカウントがOwnerか確認する。
- Rulesetを作成できない場合は、GitHubプランとVisibilityを確認する。GitHub Freeの本線はPublicを使用する。
- `pr-ci-gate`が候補に表示されない場合は、5.2のPull Requestで同名jobが一度successになっているか確認する。
- GitHub Actionsを実行できない場合は、`Settings` → `Actions` → `General`の`Actions permissions`を確認する。
- Organization所有の場合は、OrganizationまたはEnterpriseの上位ポリシーで設定が制限されていないか管理者へ確認する。
- CIやArtifactの調査は[トラブルシューティング](../troubleshooting/README.md)を参照する。

## 演習終了後のリポジトリ保持・削除

- 演習履歴が不要なら、リポジトリを削除することを推奨する。
- 復習やポートフォリオとして残す場合は、Publicリポジトリの内容を第三者が閲覧できることを理解したうえで保持する。
- GitHub Pro利用者はPrivateへ変更することも選択できる。
- 必要ならZIPを取得するか、手元へcloneしてから削除する。
- 一度Publicにした情報は第三者が取得済みの可能性があり、削除やPrivate化だけでは完全に回収できない。

削除は必須ではない。学習目的と公開範囲を確認して選択する。
