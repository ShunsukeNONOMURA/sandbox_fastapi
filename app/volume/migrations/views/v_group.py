from sqlmodel import SQLModel, Field

class VGroup(SQLModel, table=True):
    __tablename__ = "v_group"

    group_id: str = Field(
        max_length=36,
        primary_key=True,
        nullable=False,
        sa_column_kwargs={"comment": "グループID"}
    )
    user_count: int = Field(
        nullable=False,
        sa_column_kwargs={"comment": "グループに所属するユーザの数"}
    )

    @classmethod
    def create_view_sql(cls) -> str:
        return """
        CREATE VIEW v_group AS
        SELECT
            g.group_id,
            COUNT(u.user_id) AS user_count
        FROM
            t_group g
        LEFT JOIN
            t_user u ON g.group_id = u.group_id
        GROUP BY
            g.group_id;
        """
    
    @classmethod
    def drop_view_sql(cls) -> str:
        return "DROP VIEW IF EXISTS v_group CASCADE"