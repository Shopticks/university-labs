from dataclasses import dataclass, field


@dataclass
class Effect:
    kind: str
    remaining: float
    payload: dict = field(default_factory=dict)


class EffectsStack:

    def __init__(self) -> None:
        self.active: list[Effect] = []

    def add(self, kind: str, seconds: float, **payload) -> None:
        for e in self.active:
            if e.kind == kind:
                e.remaining = max(e.remaining, seconds)
                e.payload.update(payload)
                return
        self.active.append(Effect(kind=kind, remaining=seconds, payload=dict(payload)))

    def step(self, dt: float) -> list[Effect]:
        expired: list[Effect] = []
        for e in self.active:
            e.remaining -= dt
        keep, expired = [], []
        for e in self.active:
            (keep if e.remaining > 0 else expired).append(e)
        self.active = keep
        return expired

    def has(self, kind: str) -> bool:
        return any(e.kind == kind for e in self.active)

    def remaining(self, kind: str) -> float:
        for e in self.active:
            if e.kind == kind:
                return e.remaining
        return 0.0

    def clear(self) -> None:
        self.active.clear()
