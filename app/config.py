from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: str = 'sqlite+aiosqlite:///sql.db'

settings = Settings()