import pytest

from before_thinking.metrics import (
    persistent_branch_commitment,
    summarize_answers,
    switch_probability,
    wilson_interval,
)


def test_answer_summary() -> None:
    summary = summarize_answers(["A", "A", "A", "B"])
    assert summary.mode == "A"
    assert summary.modal_mass == 0.75
    assert 0 < summary.normalized_entropy < 1


def test_wilson_interval_contains_observed_rate() -> None:
    lower, upper = wilson_interval(8, 10)
    assert lower < 0.8 < upper


def test_commitment_requires_persistence_and_precision() -> None:
    checkpoints = [0.0, 0.25, 0.5, 0.75]
    samples = [
        ["A"] * 8 + ["B"] * 8,
        ["B"] * 16,
        ["B"] * 16,
        ["B"] * 16,
    ]
    assert persistent_branch_commitment(checkpoints, samples, threshold=0.75) == 0.25


def test_commitment_is_undefined_when_mode_changes() -> None:
    checkpoints = [0.0, 0.5, 1.0]
    samples = [["A"] * 20, ["A"] * 20, ["B"] * 20]
    assert persistent_branch_commitment(checkpoints, samples, threshold=0.8) is None


def test_switch_probability() -> None:
    assert switch_probability("A", ["A", "B", "A", "C"]) == 0.5


@pytest.mark.parametrize("successes,trials", [(-1, 2), (3, 2), (1, 0)])
def test_invalid_wilson_inputs(successes: int, trials: int) -> None:
    with pytest.raises(ValueError):
        wilson_interval(successes, trials)
