from sqlmodel import SQLModel, Field

class VUser(SQLModel, table=True):
    __tablename__ = "v_user"

    user_id: str = Field(
        max_length=36,
        primary_key=True,
        nullable=False,
        sa_column_kwargs={"comment": "グループID"}
    )
    
    group_id: str
    is_member: bool


    @classmethod
    def create_view_sql(cls) -> str:
        return f"""
        CREATE VIEW {cls.__tablename__} AS
        SELECT
            u.user_id,
            u.group_id,
            CASE
                WHEN u.group_id IS NOT NULL THEN TRUE
                ELSE FALSE
            END AS is_member
        FROM
            t_user u;
        """
    
    @classmethod
    def drop_view_sql(cls) -> str:
        return f"DROP VIEW IF EXISTS {cls.__tablename__} CASCADE"