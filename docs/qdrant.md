# Qdrant

## 概要

Qdrant は、ベクトル検索のためのデータベースです。
文章、画像、音声などを埋め込みベクトルに変換して保存し、似ているデータを高速に探せます。

このリポジトリでは、Qdrant を `docker-compose.yml` で起動し、設定やコレクション定義を `.docker/qdrant` 配下で管理します。

## この構成でやっていること

- Qdrant 本体を `vdb` サービスとして起動する
- 起動時に `vdb-init` がコレクション定義を読み込む
- 設定は [`.docker/qdrant/config/production.yaml`](/Users/kubo/Desktop/furumi_work/llm/.docker/qdrant/config/production.yaml) で管理する
- コレクションの定義は [`.docker/qdrant/collections/`](/Users/kubo/Desktop/furumi_work/llm/.docker/qdrant/collections) に JSON で置く
- BGE-M3 用のコレクション定義は [`.docker/qdrant/collections/documents_bge_m3.json`](/Users/kubo/Desktop/furumi_work/llm/.docker/qdrant/collections/documents_bge_m3.json) に置く

## ポートの用途

この Compose では、Qdrant の次のポートを公開しています。

- `6333`: HTTP API 用
- `6334`: gRPC 用

通常の確認や、コレクションの作成・検索などの REST API 呼び出しは `6333` を使います。
`6334` は gRPC クライアントから接続したい場合に使います。

`vdb-init` は初期化用のコンテナなので、ポートは公開しません。

## 起動方法

1. Docker を起動する
2. 次のコマンドを実行する

```bash
docker compose up -d vdb vdb-init
```

3. 起動確認をする

```bash
curl http://localhost:6333/readyz
```

`healthz check passed` のような応答が返れば、Qdrant は利用可能です。

## 使い方

Qdrant はコレクション単位でデータを管理します。
今回の構成では、`documents` というコレクションを初期値として作成しています。
もし BGE-M3 を使うなら、`documents_bge_m3.json` を使って hybrid 構成のコレクションを作るのが基本です。

コレクション一覧は次の API で確認できます。

```bash
curl http://localhost:6333/collections
```

詳細を見たい場合は、コレクション名を指定します。

```bash
curl http://localhost:6333/collections/documents
```

データを入れるときは、まずコレクションに合う次元数と距離関数を決めます。
`documents.json` は他モデル向けの例で、`documents_bge_m3.json` では `size: 1024` の dense ベクトルに加えて sparse ベクトルも有効にしています。

## コレクション追加時の操作

コレクションを増やすときは、次の流れで進めると分かりやすいです。

1. [`.docker/qdrant/collections/`](/Users/kubo/Desktop/furumi_work/llm/.docker/qdrant/collections) に新しい JSON ファイルを追加する
2. ファイル名をコレクション名にする
3. ベクトル次元数と距離関数を定義する
4. `vdb-init` を再実行して作成する

たとえば `articles` コレクションを追加する場合は、`articles.json` を作ります。

```json
{
  "vectors": {
    "size": 1536,
    "distance": "Cosine"
  },
  "metadata": {
    "description": "Articles for semantic search"
  }
}
```

その後、初期化コンテナを再実行します。

```bash
docker compose run --rm vdb-init
```

すでにコレクションが存在する場合は、スクリプトが作成をスキップします。
新規追加したときだけ作成されるので、開発中の繰り返し実行にも使いやすいです。

## 追加時の注意

- `size` は埋め込みモデルの出力次元と一致させる必要があります
- `distance` は検索の比較方法です
- 既存コレクションの `size` は後から簡単には変えられないので、最初に合わせるのが安全です
- hybrid 構成では dense ベクトルと sparse ベクトルの両方を upsert します
- sparse ベクトルは名前付きで管理し、検索側でも同じ名前を使います

## 管理ファイル

- 設定: [`.docker/qdrant/config/production.yaml`](/Users/kubo/Desktop/furumi_work/llm/.docker/qdrant/config/production.yaml)
- コレクション定義: [`.docker/qdrant/collections/documents.json`](/Users/kubo/Desktop/furumi_work/llm/.docker/qdrant/collections/documents.json)
- BGE-M3 向けコレクション定義: [`.docker/qdrant/collections/documents_bge_m3.json`](/Users/kubo/Desktop/furumi_work/llm/.docker/qdrant/collections/documents_bge_m3.json)
- 初期化スクリプト: [`.docker/qdrant/scripts/apply-collections.sh`](/Users/kubo/Desktop/furumi_work/llm/.docker/qdrant/scripts/apply-collections.sh)
