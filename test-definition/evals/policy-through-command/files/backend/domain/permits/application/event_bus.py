"""In-process event bus of the context permits: commands publish, policies subscribe."""

from collections import defaultdict
from collections.abc import Awaitable, Callable

Handler = Callable[[object], Awaitable[None]]


class EventBus:
    def __init__(self) -> None:
        self._handlers: dict[type, list[Handler]] = defaultdict(list)

    def subscribe(self, event_type: type, handler: Handler) -> None:
        self._handlers[event_type].append(handler)

    async def publish(self, event: object) -> None:
        for handler in self._handlers[type(event)]:
            await handler(event)


def build_event_bus(procedures) -> EventBus:
    """Wires every policy of permits to the events it reacts to."""
    from ..aggregates.evidence.model.events.evidence_rejected import EvidenceRejected
    from ..aggregates.procedure.application.policies.on_evidence_rejected import on_evidence_rejected

    bus = EventBus()
    bus.subscribe(EvidenceRejected, lambda event: on_evidence_rejected(procedures, event))
    return bus
