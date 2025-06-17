from typing import Any

from dictknife import (
    deepmerge,  # MEMO(nonomura): 外部依存なので導入不可の場合手組すること
)
from sqlmodel import Field

from pydantic import BaseModel

class SearchParams(BaseModel):
    limit: int = 10
    offset: int = 0
    query: dict[str, Any] = Field({})

    include: list[str] | None = None  # どの項目を取得するかの指定
    exclude: list[str] | None = None  # どの項目を排除するかの指定

    sort: list[dict[str, Any]] = Field(
        default=[]
    )  # 例: [{"age": "desc"}, {"name": "asc"}]

    def query_update(self, query: dict[str, Any]) -> None:
        self.query = deepmerge(self.query, query)

class SearchResult(BaseModel):
    total: int
    items: list[Any]

class SearchService:
    def __init__(self):
        pass

    def search(self, index: str, params: SearchParams):
        return []
    



import contextlib
from datetime import UTC, datetime
from typing import Any, cast

from sqlalchemy.engine.row import Row
from sqlalchemy.sql.expression import and_, not_, or_
from sqlmodel import Session, SQLModel, func, select
from sqlmodel.sql.expression import SelectOfScalar

# from app.ddd.domain.model.search import SearchParams, SearchResult
# from app.ddd.domain.service import SearchService
from migrations.models import (
    TGroup,
    TUser,
)
from migrations.views import (
    VGroup
)

class RDBSearchService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.index_models = {
            "group": VGroup,
        }

    def search(self, index: str, params: SearchParams) -> SearchResult:
        """
        検索メソッド (インターフェース).

        Args:
            index: 検索対象
            params: 検索パラメータ

        Returns:
            SearchResult: (合計件数, 検索結果)

        """
        # セッション
        session = self.session

        # モデル選択
        # index = 'knowledge'
        if self.index_models.get(index) is None:
            return SearchResult(total=0, items=[])
        model = cast(type[SQLModel], self.index_models[index])
        # model: TDigitalBuddy = type[TDigitalBuddy]

        # レコード数を計算
        total_statement = select(func.count()).select_from(model)  # レコード数を計算
        total_statement = self.__apply_query(model, total_statement, params.query)
        total = session.exec(total_statement).one()  # クエリ後の総数を計算

        # **対象のフィールドのみ取得するか、除外するかを決定**
        if params.include:
            # `include` が指定された場合は、そのフィールドのみ取得
            selected_fields = [
                getattr(model, field)
                for field in params.include
                if hasattr(model, field)
            ]
        else:
            # `include` がない場合、全カラム取得し `exclude` の指定があれば除外
            table = getattr(model, "__table__", None)
            all_fields = list(table.columns.keys()) if table is not None else []
            if params.exclude:
                all_fields = [
                    field for field in all_fields if field not in params.exclude
                ]
            if "id" in all_fields:
                all_fields.remove("id")  # RDB管理用のidの削除
            selected_fields = [getattr(model, field) for field in all_fields]

        # ベースステートメント(フィールド条件の適用)
        # statement = select(model) # モデル全体を選択
        statement = select(
            *selected_fields
        )  # TODO(nonomura): リレーション表現できていない問題。リードモデルで対処するなどの想定
        # **リレーションを取得するために `joinedload()` を適用**
        # statement = statement.options(*[joinedload(getattr(model, rel)) for rel in model.__mapper__.relationships.keys()])

        # クエリ条件の適用
        statement = self.__apply_query(model, statement, params.query)

        # ソート条件を適用
        statement = self.__apply_sorting(model, statement, params.sort)

        # リミットとオフセットを適用
        if params.limit > 0:  # -1の時はすべて取得
            statement = statement.limit(params.limit)
        statement = statement.offset(params.offset)

        # 実行して結果を取得
        records = session.exec(
            statement
        ).all()  # TODO(nonomura): スカラ、ROW、モデルのどれかになってしまう。

        # **データを統一的に List[Dict[str, Any]] に変換**
        items = self.__convert_to_dict(records, selected_fields)

        return SearchResult(total=total, items=items)

    def __apply_query(
        self,
        model: type[SQLModel],
        statement: SelectOfScalar[Any],
        query: dict[str, Any],
    ) -> SelectOfScalar[Any]:
        """OpenSearchライク の `query` 構造を SQLAlchemy の where 条件に変換する."""
        conditions = self.__parse_query(model, query)

        if conditions:
            statement = statement.where(and_(*conditions))  # AND 条件で適用

        return statement

    def __parse_query(self, model: type[SQLModel], query: dict[str, Any]) -> list[Any]:
        """OpenSearchライククエリを SQLAlchemy のフィルタに変換."""
        # if "query" in query:
        #     query = query["query"]

        conditions = []

        # クエリがリストで渡された場合、各要素を処理
        if isinstance(query, list):
            for sub_query in query:
                conditions.extend(self.__parse_query(model, sub_query))
            return conditions

        # ブール値の場合、再帰処理の条件整理
        if "bool" in query:
            conditions.extend(self.__parse_bool(model, query["bool"]))

        # 指定条件の場合、特定の条件を追加
        if "term" in query:
            conditions.extend(self.__parse_term(model, query["term"]))

        if "wildcard" in query:
            conditions.extend(self.__parse_wildcard(model, query["wildcard"]))

        if "range" in query:
            conditions.extend(self.__parse_range(model, query["range"]))

        return conditions

    def __parse_bool(
        self, model: type[SQLModel], bool_query: dict[str, Any]
    ) -> list[Any]:
        """Bool クエリの解析 (AND, OR, NOT)."""
        conditions = []

        if "filter" in bool_query:
            filter_conditions = self.__parse_query(model, bool_query["filter"])
            if filter_conditions:
                conditions.append(and_(*filter_conditions))

        if "should" in bool_query:
            should_conditions = self.__parse_query(model, bool_query["should"])
            if should_conditions:
                conditions.append(or_(*should_conditions))

        if "not" in bool_query:
            not_conditions = self.__parse_query(model, bool_query["not"])
            if not_conditions:
                conditions.append(not_(and_(*not_conditions)))

        return conditions

    def __parse_term(
        self, model: type[SQLModel], term_query: dict[str, Any]
    ) -> list[Any]:
        """Term クエリの解析 (完全一致)."""
        conditions = []
        for field, value in term_query.items():
            if not hasattr(model, field):
                # logger.warning(f"無効なカラム名が指定されました: {field}")
                continue
            conditions.append(getattr(model, field) == value.get("value", value))
        return conditions

    def __parse_wildcard(
        self, model: type[SQLModel], wildcard_query: dict[str, Any]
    ) -> list[Any]:
        """Wildcard クエリの解析 (部分一致)."""
        conditions = []
        for field, value in wildcard_query.items():
            if not hasattr(model, field):
                # logger.warning(f"無効なカラム名が指定されました: {field}")
                continue
            wildcard_value = value.get("value", value).replace("*", "%")
            conditions.append(getattr(model, field).like(wildcard_value))
        return conditions

    def __parse_range(
        self, model: type[SQLModel], range_query: dict[str, Any]
    ) -> list[Any]:
        """Range クエリの解析 (範囲検索)."""
        conditions = []
        for field, value in range_query.items():
            if not hasattr(model, field):
                # logger.warning(f"無効なカラム名が指定されました: {field}")
                continue
            field_attr = getattr(model, field)
            for op, v in value.items():
                converted_value = v
                if isinstance(v, str):
                    with contextlib.suppress(ValueError):
                        converted_value = datetime.strptime(v, "%Y-%m-%d").replace(
                            tzinfo=UTC
                        )
                if op == "gte":
                    conditions.append(field_attr >= converted_value)
                elif op == "lte":
                    conditions.append(field_attr <= converted_value)
                elif op == "gt":
                    conditions.append(field_attr > converted_value)
                elif op == "lt":
                    conditions.append(field_attr < converted_value)
        return conditions

    def __apply_sorting(
        self,
        model: type[SQLModel],
        statement: SelectOfScalar[Any],
        sort: list[dict[str, Any]],
    ) -> SelectOfScalar[Any]:
        """
        ソート条件を適用する.

        Args:
            model: SQLModelクラス.
            statement: SQLAlchemyのクエリステートメント.
            sort: ソート条件のリスト（[{ "line_id": { "order": "desc" } }, ...]）

        Returns:
            select: ソート適用後のステートメント.

        """
        for sort_rule in sort:
            if not isinstance(sort_rule, dict):
                continue

            for field, options in sort_rule.items():
                order = options.get("order")

                if order in {"asc", "desc"}:
                    field_attr = getattr(model, field, None)
                    if field_attr:
                        if order == "asc":
                            statement = statement.order_by(field_attr.asc())
                        elif order == "desc":
                            statement = statement.order_by(field_attr.desc())
        return statement

    def __convert_to_dict(
        self, records: list[Any], fields: list[Any]
    ) -> list[dict[str, Any]]:
        """
        SQLAlchemy の結果を List[Dict[str, Any]] に変換する。.

        - `Row` 形式のオブジェクトや単一の値でも統一的に辞書へ変換する。.

        Args:
            records: 検索結果（Rowオブジェクト, Modelオブジェクト, 単一値など）
            fields: 取得対象のカラムリスト

        Returns:
            List[Dict[str, Any]]: 辞書形式のリスト

        """
        result = []
        field_names = [
            field.name if hasattr(field, "name") else field for field in fields
        ]

        for record in records:
            if isinstance(record, Row):
                # `Row._mapping` を使用して安全に辞書化
                record_dict = record._asdict()
                result.append({field: record_dict[field] for field in field_names})
            elif isinstance(record, SQLModel):
                # SQLModel の場合、dict に変換
                result.append(record.dict())
            elif isinstance(record, tuple):
                # 単一のカラム取得時のタプルを辞書に変換
                result.append({field_names[i]: record[i] for i in range(len(record))})
            else:
                # 単一値 (例えば COUNT の場合) の場合
                result.append({field_names[0]: record})

        return result
