from typing import TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship

from migrations.base import BaseTable

if TYPE_CHECKING:
    from migrations.models.t_user import TUser  # 循環参照を避けるため TYPE_CHECKING を使う

class TGroup(BaseTable, table=True):
    __tablename__ = "t_group"

    group_id: str = Field(
        max_length=36,
        nullable=False,
        unique=True,
        sa_column_kwargs={
            "comment": "UK：グループを一意に識別するID（openid connect sub）"
        },
    )

    # 逆参照（グループが持つユーザー一覧）
    users: list["TUser"] = Relationship(back_populates="group")