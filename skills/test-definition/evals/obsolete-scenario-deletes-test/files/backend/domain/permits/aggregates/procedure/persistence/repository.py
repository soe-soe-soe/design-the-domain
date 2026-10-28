"""SQLAlchemy adapter of ProcedureRepository (bodies omitted in this fixture)."""


class SqlProcedureRepository:
    def __init__(self, session):
        self._session = session

    async def save(self, procedure) -> None: ...
