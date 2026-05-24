from pydantic_settings import BaseSettings,SettingsConfigDict
from urllib.parse import quote_plus

# 設定モデルを定義
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )
    APP_PORT: int = 9000

    DB_HOST:str = "db"
    DB_USER: str = "root"
    DB_PASSWORD: str = ""
    DB_PORT: int = 3306
    DB_NAME: str = "llm"

    @property
    def db_url(self) -> str:
        user = quote_plus(self.DB_USER)
        pwd = quote_plus(self.DB_PASSWORD)
        return f"mysql+pymysql://{user}:{pwd}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"