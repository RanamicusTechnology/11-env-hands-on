<!--
Copyright 2026 Ranamicus Technology LLC. All rights reserved.
-->

# Third-Party Notices

## 1. この文書の位置付け

本文書は、社外弁護士レビュー前の法務レビュー用ドラフトです。

本Repositoryの`LICENSE`は、Ranamicus Technology合同会社が権利を有する教材固有の
Materialsだけに適用されます。第三者ソフトウェア、GitHub Actions、container image、
package、serviceその他のThird-Party Materialsには、それぞれの権利者が定めるlicense、
noticeおよび利用規約が適用されます。本Repositoryの`LICENSE`は、これらを再許諾しません。

この一覧は、2026-08-24時点のRepository内の直接参照を対象にした確認結果です。網羅性を
保証するものではありません。version更新、transitive dependencyの変更、container image
またはBuild Artifactの配布を行う場合は、実際に取得した配布物のlicense metadata、
Copyright noticeおよびattributionを再確認してください。

## 2. 利用形態と再配布の区別

現在のRepositoryには、次の種類の参照があります。

- workflow、requirements、Terraform設定、Dockerfile等に第三者資源の取得先やversionを
  記載し、CIまたは演習実行時に取得するもの
- GitHub、GitHub Actions、GitHub-hosted runner等をserviceとして利用するもの
- Ubuntu base imageやUbuntu packageをcontainer build時に取得するもの

RepositoryのGit treeには、下表の第三者project本体のsource code、Action bundle、Python
wheel、Terraform binary/provider binary、Ubuntu image、Nginx binaryまたはDocker binaryを
複製していません。したがって、現状のPublic Repository生成で配布されるのは主として
参照定義です。ただし、利用者がcontainer image、依存packageを含む環境、またはbinaryを
第三者へ配布する場合は、当該配布物に適用されるlicense義務を別途満たす必要があります。

## 3. GitHub、GitHub Actionsおよびrunner

| 名称 | Repository内での利用形態 | upstream / 確認先 | licenseまたは規約 | notice上の注意 |
| --- | --- | --- | --- | --- |
| GitHub / GitHub Actions service | Issue、Pull Request、workflow、Artifact、GitHub-hosted runnerをserviceとして利用 | [GitHub Terms of Service](https://docs.github.com/en/site-policy/github-terms/github-terms-of-service)、[GitHub Actionsの利用条件案内](https://docs.github.com/en/actions/concepts/billing-and-usage) | GitHubの利用規約およびAdditional Product Terms | service利用であり、GitHub service自体をRepositoryへ複製していない。Public Repositoryの閲覧・fork等にはGitHubの規約が別途適用される。 |
| GitHub-hosted runner `ubuntu-latest` | workflow実行環境 | [GitHub runner images](https://github.com/actions/runner-images) | runner imageに含まれる各softwareの個別licenseおよびGitHubの利用規約 | runner imageの内容は更新され得る。配布物へrunner imageを同梱していない。厳密な監査では対象workflow runのimage versionとsoftware inventoryを確認する。 |
| `actions/checkout` v4.2.2 | immutable commit SHAをworkflowから参照 | [pinned source / LICENSE](https://github.com/actions/checkout/blob/11bd71901bbe5b1630ceea73d27597364c9af683/LICENSE) | MIT License | Action本体はGit treeへ複製せず、workflow実行時に取得する。再配布する場合はCopyright noticeとlicense textを保持する。 |
| `actions/setup-go` v5.5.0 | immutable commit SHAをworkflowから参照 | [pinned source / LICENSE](https://github.com/actions/setup-go/blob/d35c59abb061a4a6fb18e82ac0862c26744d6ab5/LICENSE) | MIT License | 同上。 |
| `actions/setup-python` v5.6.0 | immutable commit SHAをworkflowから参照 | [pinned source / LICENSE](https://github.com/actions/setup-python/blob/a26af69be951a213d495a4c3e4e4022e16d87065/LICENSE) | MIT License | 同上。 |
| `actions/upload-artifact` v4.6.2 | immutable commit SHAをworkflowから参照 | [pinned source / LICENSE](https://github.com/actions/upload-artifact/blob/ea165f8d65b6e75b540449e92b4886f43607fa02/LICENSE) | MIT License | 同上。 |
| `actions/download-artifact` v4.3.0 | immutable commit SHAをworkflowから参照 | [pinned source / LICENSE](https://github.com/actions/download-artifact/blob/d3f86a106a0bac45b974a628896c90dbdf5c8093/LICENSE) | MIT License | 同上。 |
| `hashicorp/setup-terraform` v3.1.2 | immutable commit SHAをworkflowから参照 | [pinned source / LICENSE](https://github.com/hashicorp/setup-terraform/blob/b9cd54a3c349d3f38e8881555d616ced269862dd/LICENSE) | Mozilla Public License 2.0 | Action本体はGit treeへ複製しない。Actionのlicenseと、Actionが取得するTerraform本体のlicenseは別である。 |

## 4. Toolchain、IaCおよびcontainer関連

| 名称 | Repository内での利用形態 | upstream / 確認先 | licenseまたは規約 | notice上の注意 |
| --- | --- | --- | --- | --- |
| Go 1.26.4 | `actions/setup-go`がCI実行時に取得し、Go appのtest/buildに利用 | [Go LICENSE](https://github.com/golang/go/blob/go1.26.4/LICENSE) | BSD 3-Clause License相当のGo project license | Go toolchainをRepositoryへ複製していない。Go appは標準libraryだけをimportし、`go.mod`に外部module dependencyはない。Go binaryを配布する場合は、toolchainおよび標準libraryのnotice要否を成果物単位で再確認する。 |
| `gotestsum` v1.13.0 | `go install`でCI実行時に取得し、JUnit XML生成に利用 | [`gotestsum` LICENSE](https://github.com/gotestyourself/gotestsum/blob/v1.13.0/LICENSE) | Apache License 2.0 | tool本体をGit treeへ複製していない。binaryを再配布する場合はlicenseとnoticeを確認する。 |
| Terraform 1.14.1 | `setup-terraform`がCI実行時に取得し、UT環境面のplan/apply/destroyに利用 | [Terraform v1.14.1 LICENSE](https://github.com/hashicorp/terraform/blob/v1.14.1/LICENSE) | Business Source License 1.1。upstream LICENSEのparameters、Additional Use Grant、Change Date、Change License (MPL 2.0)を含む | Terraform 1.6.0以降のlicenseは、`setup-terraform` ActionのMPL 2.0とは異なる。binaryをGit treeへ複製していない。利用・組込み・再配布時は対象versionのLICENSEを確認する。 |
| Terraform Docker Provider (`kreuzwerker/docker`) 4.5.0 | `terraform init`で実行時に取得するprovider | [v4.5.0 LICENSE](https://github.com/kreuzwerker/terraform-provider-docker/blob/v4.5.0/LICENSE) | Mozilla Public License 2.0 | provider binaryをGit treeへ複製していない。Terraform cacheやprovider binaryはcommitしない。 |
| TFLint v0.63.1 | `scripts/ms1/install-tflint.sh`がrelease binaryとchecksumを実行時に取得 | [v0.63.1 LICENSE](https://github.com/terraform-linters/tflint/blob/v0.63.1/LICENSE) | Mozilla Public License 2.0 | binaryをGit treeへ複製していない。再配布時はupstream LICENSEを添付する。pluginを追加した場合はplugin固有licenseも確認する。 |
| Docker Engine / CLI | GitHub-hosted runner上のDockerをcontainer build、Terraform Provider、test、cleanupで利用 | [Docker CLI LICENSE](https://github.com/docker/cli/blob/master/LICENSE)、[Moby LICENSE](https://github.com/moby/moby/blob/master/LICENSE) | 実際に利用する配布物のlicenseはrunner imageおよびinstall元で要確認 | runner提供toolをservice実行時に利用し、Docker binaryやdaemonをGit treeへ複製していない。対象workflow runのversionと配布元を記録して確認する。 |
| Ubuntu 24.04 base image | digest固定の`ubuntu:24.04`をDockerfileのbase imageとしてbuild時に取得 | [Canonical Intellectual Property Rights Policy](https://ubuntu.com/legal/intellectual-property-policy)、image内の`/usr/share/doc/*/copyright` | Ubuntuは複数のworkの集合であり、単一licenseではない。各package固有licenseとCanonicalのpolicyが適用される | built imageはGit treeへ含めていない。imageを配布する場合、実際のdigest、package一覧、各package notice、Ubuntu trademark/policyを確認する。 |
| Ubuntu packages (`bash`, `ca-certificates`, `curl`, `iproute2`, `net-tools`, `procps`, `python3`, `python3-apt`, `tar`) | DockerfileがUbuntu package repositoryからbuild時にinstall | Ubuntu package metadata、image内の`/usr/share/doc/<package>/copyright` | packageごとに異なるため一括したlicense名は記載しない | package versionはDockerfileで固定していない。built imageを配布する前に、実際にinstallされたversionとnoticeをSBOM等で確定する。 |
| Nginx | AnsibleがUbuntu package repositoryから対象containerへ実行時にinstall | [Nginx LICENSE](https://github.com/nginx/nginx/blob/master/LICENSE)、Ubuntu packageの`/usr/share/doc/nginx/copyright` | upstream Nginxは2-Clause BSD License相当。Ubuntu packageのpatchや同梱物はpackage metadataで別途確認 | Nginx binaryをGit treeへ複製していない。package versionは固定していないため、built imageまたは環境を配布する場合は「要確認」。 |

## 5. Python、Ansibleおよびtest dependency

| 名称 | Repository内での利用形態 | upstream / 確認先 | licenseまたは規約 | notice上の注意 |
| --- | --- | --- | --- | --- |
| Python 3.12.13 | `actions/setup-python`がCI実行時に取得し、script、Ansible、pytestを実行 | [Python 3.12.13 LICENSE](https://github.com/python/cpython/blob/v3.12.13/LICENSE) | Python Software Foundation Licenseほか、同LICENSEに列挙される履歴上の条件 | interpreterをGit treeへ複製していない。再配布時は対象versionのLICENSEを確認する。 |
| pip (workflowで`--upgrade`、version未固定) | CI実行時にPython packageをinstall | [pip LICENSE](https://github.com/pypa/pip/blob/main/LICENSE.txt) | MIT License | workflow実行時の正確なversionはlogで「要確認」。pip本体をGit treeへ複製していない。 |
| Ansible community package 13.8.0 | `requirements/ms1.txt`から実行時install。playbookと`community.docker.docker` connectionを実行 | [Ansible community package](https://pypi.org/project/ansible/)、[build data](https://github.com/ansible-community/ansible-build-data) | `ansible-core`および同梱collectionごとにlicenseが異なる | community packageは複数collectionの集合であり、単一licenseとして扱わない。13.8.0で実際に同梱されるcollection一覧と各licenseは、wheel、build data、`ansible-galaxy collection list`で「要確認」。 |
| `ansible-core` (Ansible 13.8.0のdependency) | Ansible実行engineとして実行時install | [`ansible-core` metadata / COPYING](https://github.com/ansible/ansible/blob/devel/COPYING) | GPL-3.0-or-later | sourceまたはbinaryをGit treeへ複製していない。対象wheelのlicense filesを保持・確認する。 |
| `community.docker` collection (Ansible 13.8.0により取得) | inventoryのDocker connection pluginとして実行 | [`community.docker` metadata](https://github.com/ansible-collections/community.docker/blob/main/galaxy.yml)、[COPYING](https://github.com/ansible-collections/community.docker/blob/main/COPYING) | upstream metadataはGPL-3.0-or-laterおよびApache-2.0を列挙 | Ansible 13.8.0が取得する正確なcollection versionとfile単位のlicenseは「要確認」。collection本体をGit treeへ複製していない。 |
| `ansible-lint` 26.4.0 | `requirements/ms1.txt`から実行時installし、playbook静的解析に利用 | [v26.4.0 metadata](https://github.com/ansible/ansible-lint/blob/v26.4.0/pyproject.toml)、[COPYING](https://github.com/ansible/ansible-lint/blob/v26.4.0/COPYING) | GPL-3.0-or-later | packageとtransitive dependenciesをGit treeへ複製していない。再配布時は対象wheelのlicense filesを確認する。 |
| Docker SDK for Python (`docker`) 7.1.0 | `requirements/ms1.txt`から実行時installし、Testinfra/AnsibleのDocker接続で利用 | [7.1.0 LICENSE](https://github.com/docker/docker-py/blob/7.1.0/LICENSE) | Apache License 2.0 | packageをGit treeへ複製していない。transitive dependenciesは実際のinstall metadataで確認する。 |
| pytest 8.4.2 / 8.4.1 | `requirements/ms1.txt`および`requirements/learning-assets.txt`から実行時installし、testを実行 | [pytest 8.4.2 LICENSE](https://github.com/pytest-dev/pytest/blob/8.4.2/LICENSE) | MIT License | packageをGit treeへ複製していない。複製または再配布時はCopyright noticeとlicense textを保持する。 |
| pytest-testinfra 10.2.2 | `requirements/ms1.txt`から実行時installし、正式インフラテストに利用 | [10.2.2 LICENSE](https://github.com/pytest-dev/pytest-testinfra/blob/10.2.2/LICENSE) | Apache License 2.0 | packageをGit treeへ複製していない。 |
| Requests 2.32.4 | `requirements/ms1.txt`から実行時installし、正式APIテストに利用 | [v2.32.4 LICENSE](https://github.com/psf/requests/blob/v2.32.4/LICENSE) | Apache License 2.0 | packageをGit treeへ複製していない。transitive dependenciesは実際のinstall metadataで確認する。 |
| PyYAML 6.0.2 | `requirements/learning-assets.txt`から実行時installし、教材validatorでYAMLを処理 | [6.0.2 LICENSE](https://github.com/yaml/pyyaml/blob/6.0.2/LICENSE) | MIT License | packageをGit treeへ複製していない。複製または再配布時はCopyright noticeとlicense textを保持する。 |

## 6. 未確認事項と公開前の追加確認

次は、推測で確定せず、社外弁護士レビューまたは実際の配布物生成時に確認します。

- Ansible community package 13.8.0に含まれる全collection、正確なversionおよびfile単位の
  license
- Python package、Ansible collection、Terraform provider等のtransitive dependenciesの
  正確なversion、licenseおよびnotice
- GitHub-hosted runnerの対象workflow runで実際に使用されたDocker Engine / CLIその他の
  preinstalled softwareのversionと配布元
- Ubuntu base image上で実際にinstallされたpackage version、package固有license、patch、
  Copyright noticeおよびattribution
- build済みcontainer image、Terraform/plugin cache、Python environment、Action bundle、
  binary等を将来配布対象へ追加する場合に必要となるlicense text、NOTICE、source offer、
  attributionおよびtrademark上の対応

第三者資源を更新または新規追加した場合は、dependency定義だけでなく、本文書の名称、
利用形態、upstream、license確認先およびnotice上の注意も同じ変更で更新してください。
