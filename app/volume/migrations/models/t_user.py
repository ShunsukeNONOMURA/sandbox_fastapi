from sqlmodel import Field, SQLModel, Relationship

from typing import Optional, TYPE_CHECKING
from migrations.base import BaseTable

# if TYPE_CHECKING:
#     from migrations.models.t_group import TGroup  # 循環参照を避けるため TYPE_CHECKING を使う
from migrations.models.t_group import TGroup  # 循環参照を避けるため TYPE_CHECKING を使う

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

    group_id: Optional[str] = Field(
        default=None,
        foreign_key="t_group.group_id",
        sa_column_kwargs={
            "comment": "FK：所属するグループのID（t_group.group_id）"
        },
    )

    # 外部キーとしての関係（ユーザーが所属するグループ）
    group: Optional["TGroup"] = Relationship(back_populates="users")