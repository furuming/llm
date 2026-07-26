import os

# Settingsを生成するモジュールがテスト収集時にimportされるため、
# 本番用の設定へフォールバックしないテスト専用の署名鍵を先に設定する。
os.environ["APP_KEY"] = "test-only-app-key-at-least-32-chars"
