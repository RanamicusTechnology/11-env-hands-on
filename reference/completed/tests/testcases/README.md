<!--
Copyright 2026 Ranamicus Technology LLC. All rights reserved.
-->

# 正式テスト観点

5.5で接続する正式テストは、次の責務を分けて確認する。

| 種別 | 主な確認対象 |
| --- | --- |
| インフラテスト | container/network label、Nginx設定、Goアプリbinary、process、port、Nginx経由health |
| APIテスト | `/health`のstatusとbody、Build Artifact version、未対応method、未定義path |

Goアプリ単体テスト、UT環境上の最小起動・疎通確認、正式インフラテスト、正式APIテストを同じテストとして扱わない。
