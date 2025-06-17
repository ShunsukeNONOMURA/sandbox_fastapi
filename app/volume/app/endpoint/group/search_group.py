from app.endpoint.group.router import router
from app.infrastructure.database.db import get_session

from fastapi import Depends
from sqlmodel import Session

@router.post(
    "/groups:search"
)
async def search_groups(
    session: Session = Depends(get_session),
):
    from app.domain.service.search_service import SearchService, RDBSearchService, SearchParams
    search_service = RDBSearchService(session)
    return search_service.search(
        index = 'group',
        params = SearchParams(),
    )
