from sayr.command import AutonomyLevel


def test_advisory_levels_never_act():
    assert not AutonomyLevel.OBSERVE.can_act
    assert not AutonomyLevel.ADVISE.can_act


def test_approval_level_acts_only_with_approval():
    assert AutonomyLevel.APPROVE.can_act
    assert AutonomyLevel.APPROVE.needs_approval
    assert not AutonomyLevel.SUPERVISED.needs_approval
