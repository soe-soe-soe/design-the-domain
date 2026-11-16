from datetime import date

evidence_history: list[dict] = []


def on_deadline_done(permit_id: str, title: str, done_on: date) -> None:
    """A done deadline appears in the evidence history of its permit."""
    evidence_history.append({"permit_id": permit_id, "text": f"Deadline done: {title}", "on": done_on})
