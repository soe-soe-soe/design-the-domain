"""Aggregate root of an Antrag."""

from dataclasses import dataclass
from enum import StrEnum


class ProcedureStatus(StrEnum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    REWORK = "rework"


@dataclass
class Procedure:
    id: str
    project_id: str
    status: ProcedureStatus = ProcedureStatus.DRAFT
