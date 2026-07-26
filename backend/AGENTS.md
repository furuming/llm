# Project instructions

## Logging

ログに関する実装・変更・レビューを行う場合は、必ず [`docs/log.md`](docs/log.md) を確認し、そのルールに従うこと。

重要ルール:

- 共通 logger は `app.infrastructure.logger.logger` から直接 import する。
- logger を DI（コンストラクターや関数の引数として受け渡し）しない。
- ログ出力の代わりに `print()` を使用しない。
- パスワード、JWT、アクセストークン、Cookie、秘密鍵などの機密情報をログに含めない。
- API を受け付ける Controller、および Infrastructure の副作用を伴う処理では、開始・正常終了時に `info` を出力する。
- 例外を送出または再送出する箇所では、`error` または `exception` を出力する。
