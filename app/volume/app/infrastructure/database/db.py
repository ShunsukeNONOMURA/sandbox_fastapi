from collections.abc import Generator
from contextlib import contextmanager

# 設定モデルを定義
from pydantic_settings import BaseSettings
from sqlmodel import Session, create_engine


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE: str
    SQLALCHEMY_DATABASE_SQLITE_URI: str
    SQLALCHEMY_DATABASE_POSTGRES_URI: str

    @property
    def database_url(self) -> str:
        """SQLALCHEMY_DATABASE に基づいて適切な URI を返す."""
        db_urls = {
            "sqlite": self.SQLALCHEMY_DATABASE_SQLITE_URI,
            "postgresql": self.SQLALCHEMY_DATABASE_POSTGRES_URI,
        }
        try:
            return db_urls[self.SQLALCHEMY_DATABASE]
        except KeyError as e:
            msg = (
                f"Invalid database type: {self.SQLALCHEMY_DATABASE}. "
                f"Supported types: {', '.join(db_urls.keys())}"
            )
            raise ValueError(msg) from e


settings = Settings()

url = settings.database_url

db_engine = create_engine(
    url=url,
    echo=False,  # SQL見る場合に有効化する
)

# 手動実行用途で分離
@contextmanager
def get_session_context() -> Generator[Session]:
    with Session(db_engine) as session:
        yield session


def get_session() -> Generator[Session]:
    with get_session_context() as session:
        yield session
