from app.infrastructure.database.db import db_engine, get_session_context, settings

from sqlalchemy import text
from sqlmodel import SQLModel
from migrations.models import *  # すべて連れてくる
from migrations.models import (
    TGroup,
    TUser,
)

# RDBの初期化
def drop_all_views(engine) -> None:
    drop_sql = """
    DO $$
    DECLARE
        r RECORD;
    BEGIN
        FOR r IN (
            SELECT table_schema, table_name
            FROM information_schema.views
            WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
        )
        LOOP
            EXECUTE format('DROP VIEW IF EXISTS %I.%I CASCADE', r.table_schema, r.table_name);
        END LOOP;
    END $$;
    """
    # drop_sql = """
    # SELECT name FROM sqlite_master WHERE type='view';
    # """
    with get_session_context() as session:
        session.execute(text(drop_sql))
        session.commit()

def drop_all() -> None:
    drop_all_views(db_engine)             # ← 先にビュー削除
    SQLModel.metadata.drop_all(db_engine)
    # with get_session_context() as session:
    #     session.execute(text("DROP SCHEMA public CASCADE;"))
    #     session.execute(text("CREATE SCHEMA public;"))
    #     session.commit() # 手動コミット

def init_ddl() -> None:
    SQLModel.metadata.drop_all(db_engine)
    # tables_to_create = [
    #     cls.__table__ for cls in SQLModel.__subclasses__()
    #     if hasattr(cls, "__table__") and not getattr(cls, "__is_view__", False)
    # ]
    # print(tables_to_create)
    # SQLModel.metadata.create_all(bind=db_engine, tables=tables_to_create)
    SQLModel.metadata.create_all(bind=db_engine)
    with get_session_context() as session:
        from migrations.views import all_views
        for v in all_views:
            # session.execute(text(VGroup.drop_view_sql()))
            session.execute(text(v.create_view_sql()))
        session.commit()

def init_dummy_records() -> None:
    with get_session_context() as session:
        # user
        t_group = TGroup(
            group_id = "00",
        )
        session.add(t_group)
        session.flush()

        # user
        t_user = TUser(
            user_id = "00",
            group_id = "00",
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