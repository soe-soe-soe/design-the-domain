from domain.permits.models import Permit


class PermitRepository:
    def get(self, permit_id: int) -> Permit: ...

    def save(self, permit: Permit) -> None: ...
