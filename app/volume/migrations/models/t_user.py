from sqlmodel import Field, SQLModel

from migrations.models.base import BaseTable

class TUser(BaseTable, table=True):
    __tablename__ = "t_user"

    user_id: str = Field(
        max_length=36,
        nullable=False,
        unique=True,
        sa_column_kwargs={
            "comment": "UK：ユーザーを一意に識別するID（openid connect sub）"
        },
    )