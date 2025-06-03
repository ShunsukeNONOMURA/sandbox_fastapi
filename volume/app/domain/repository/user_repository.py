from sqlmodel import Session, select

from migrations.models import TUser

class UserRepository:
    def __init__(self, session: Session) -> None:
        self.__session: Session = session

    def _fetch_by_id(self, _id: str) -> TUser | None:
        statement = select(TUser).where(TUser.user_id == _id)
        return self.__session.exec(statement).first()

    def find_by_id(self, _id: str):
        model: TUser | None = self._fetch_by_id(_id)
        return model
        # if model is None:
        #     raise UserNotFoundError(user_id=_id.root)
        # return User.model_validate(model)