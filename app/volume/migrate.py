from app.infrastructure.database.db import db_engine, get_session_context, settings

from sqlalchemy import text
from sqlmodel import SQLModel
from migrations.models import *  # すべて連れてくる
from migrations.models import (
    TUser,
)

# RDBの初期化
def drop_all() -> None:
    SQLModel.metadata.drop_all(db_engine)
    # with get_session_context() as session:
    #     session.execute(text("DROP SCHEMA public CASCADE;"))
    #     session.execute(text("CREATE SCHEMA public;"))
    #     session.commit() # 手動コミット

def init_ddl() -> None:
    SQLModel.metadata.drop_all(db_engine)
    SQLModel.metadata.create_all(bind=db_engine)

def init_dummy_records() -> None:
    with get_session_context() as session:
        t_user = TUser(
            user_id = "00",
        )
        session.add(t_user)
        session.flush()

        session.commit() # 手動コミット

# テーブル作成
if __name__ == "__main__":
    print("on reset")
    drop_all()
    init_ddl()
    init_dummy_records()