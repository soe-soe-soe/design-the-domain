from enum import StrEnum


class EvidenceStatus(StrEnum):
    OPEN = "open"
    COMMISSIONED = "commissioned"
    DELIVERED = "delivered"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
