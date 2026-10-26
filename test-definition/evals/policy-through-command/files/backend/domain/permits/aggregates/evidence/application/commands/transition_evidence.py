from ....application.event_bus import EventBus
from ...model.invariants.permitted_transitions import check_permitted_transition
from ...model.repository import EvidenceRepository
from ...model.value_objects.evidence_status import EvidenceStatus


async def transition_evidence(
    repo: EvidenceRepository, events: EventBus, evidence_id: str, target: EvidenceStatus
) -> None:
    evidence = await repo.get(evidence_id)
    check_permitted_transition(evidence.status, target)
    evidence.history.append(f"{evidence.status} -> {target}")
    evidence.status = target
    await repo.save(evidence)
