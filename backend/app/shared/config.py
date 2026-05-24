from pydantic_settings import BaseSettings,SettingsConfigDict

# 設定モデルを定義
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )
    APP_PORT: int = 9000