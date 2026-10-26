from pydantic import BaseModel


class RejectEvidenceRequest(BaseModel):
    reason: str
