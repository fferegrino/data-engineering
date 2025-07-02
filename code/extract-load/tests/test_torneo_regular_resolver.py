import pytest

from mediotiempo_data.torneo_regular_resolver import TorneoRegularResolver


def test_initial_state():
    resolver_initial = TorneoRegularResolver(2024, 199, 1)
    assert resolver_initial.starting() == (2024, 199, 1)
    assert resolver_initial.current() == (2024, 199, 2)


def test_end_of_league_transition():
    resolver_end_of_league = TorneoRegularResolver(2024, 199, 17)
    assert resolver_end_of_league.starting() == (2024, 199, 17)
    assert resolver_end_of_league.current() == (2025, 385, 1)


def test_end_of_clausura_transition():
    resolver_end_of_clausura = TorneoRegularResolver(2024, 385, 17)
    assert resolver_end_of_clausura.starting() == (2024, 385, 17)
    assert resolver_end_of_clausura.current() == (2025, 199, 1)

    # Test next iterations
    assert next(resolver_end_of_clausura) == (2025, 199, 1)
    assert next(resolver_end_of_clausura) == (2025, 199, 2)


def test_penultimate_round_transition():
    resolver_penultimate_round = TorneoRegularResolver(2024, 385, 16)
    assert next(resolver_penultimate_round) == (2024, 385, 17)
    assert next(resolver_penultimate_round) == (2025, 199, 1)


def test_max_season_stop():
    resolver_max_season = TorneoRegularResolver(2025, 199, 17)
    with pytest.raises(StopIteration):
        next(resolver_max_season)
