"""SAYR autonomy levels: authority is earned with evidence, never assumed."""

from enum import IntEnum


class AutonomyLevel(IntEnum):
    OBSERVE = 0      # L0: show state and forecasts; humans decide and act
    ADVISE = 1       # L1: recommend twin-tested decisions with explanations
    APPROVE = 2      # L2: act only after an operator approves
    SUPERVISED = 3   # L3: act within limits; operator can override instantly
    FIELD = 4        # L4: command drone/robotic field units under human rules

    @property
    def can_act(self) -> bool:
        return self >= AutonomyLevel.APPROVE

    @property
    def needs_approval(self) -> bool:
        return self == AutonomyLevel.APPROVE
