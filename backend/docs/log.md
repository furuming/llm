# Logging guidelines

## 目的

アプリケーション全体で一貫したログを出力し、障害調査に必要な情報を残しながら、認証情報や個人情報の漏えいを防ぐ。

## 共通 logger

共通 logger を各モジュールから直接 import して使用する。

```python
from app.infrastructure.logger.logger import logger

logger.info("Application started")
```

logger は DI しない。クラスのコンストラクターや関数の引数として受け渡さない。

ログレベルは `app.shared.config.Settings.LOG_LEVEL` から取得する。ログは次のファイルへ出力する。

```text
/storage/logs/YYYY_MM_DD_app.log
```

## ログレベル

### INFO

正常な処理の流れを追跡するために使用する。

以下のタイミングで出力する。

- Controller が API リクエストを受け付けたとき
- Controller の処理が正常終了したとき
- Infrastructure で副作用を伴う処理を開始するとき
- Infrastructure で副作用を伴う処理が正常終了したとき
- 認証など、運用上追跡が必要な処理が正常終了したとき

```python
logger.info("Register request received email=%s", request.email)
logger.info("Register request completed user_id=%s", user.id)
```

### ERROR

処理を継続できない失敗や、例外を送出する箇所で使用する。

- 新たに例外を送出するときは、送出前に `logger.error()` を使用する。
- 捕捉した例外を再送出するときは、原則として `logger.exception()` を使用する。
- `logger.exception()` は `except` ブロック内で使用し、スタックトレースを記録する。

```python
if token is None:
    logger.error("Authentication failed: access token is missing")
    raise HTTPException(status_code=401, detail="authentication error")
```

```python
try:
    session.commit()
except Exception:
    logger.exception("Failed to save user email=%s", user.email)
    raise
```

同一の例外を複数の層で無条件に記録するとログが重複するため、各層では必要な文脈が追加できる場合に記録する。

## ログメッセージ

- 何の処理が、どの状態になったかが分かる文言にする。
- 文字列結合や f-string ではなく、logging のプレースホルダーを使用する。
- 調査に必要な識別子は `key=value` 形式で付与する。
- パスワードやトークンなどの値は、マスクした場合でも原則として出力しない。

```python
# Good
logger.info("Found user user_id=%s", user_id)

# Avoid
logger.info(f"Found user: {user_id}")
```

## 機密情報と個人情報

以下の情報をログに含めない。

- 平文・ハッシュ済みを問わずパスワード
- JWT、アクセストークン、リフレッシュトークン
- API キー、秘密鍵、署名キー
- Cookie や `Authorization` ヘッダーの内容
- DB 接続文字列や認証情報
- リクエストまたはレスポンスの機密情報を含む本文全体

メールアドレスなどの個人情報は、障害調査に必要な場合だけ使用し、不要な箇所では `user_id` などの内部識別子を優先する。

## 禁止事項

- ログ出力を目的とした `print()`
- logger の DI
- 例外を握りつぶしてログだけを出力すること
- 同一内容のログを複数の層で重複して出力すること
- 機密情報を含むオブジェクト全体の出力
