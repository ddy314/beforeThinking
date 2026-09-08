"""Registered behavioral metrics for prefix-branch experiments."""

from __future__ import annotations

from collections import Counter
from collections.abc import Hashable, Sequence
from dataclasses import dataclass
from math import log, sqrt
from statistics import NormalDist


@dataclass(frozen=True)
class AnswerDistribution:
    """Summary of answers sampled from one fixed reasoning prefix."""

    counts: dict[Hashable, int]
    total: int
    mode: Hashable
    modal_mass: float
    normalized_entropy: float


def summarize_answers(answers: Sequence[Hashable]) -> AnswerDistribution:
    """Summarize a non-empty collection of categorical final answers."""
    if not answers:
        raise ValueError("answers must be non-empty")
    counts = Counter(answers)
    mode, mode_count = counts.most_common(1)[0]
    total = len(answers)
    probabilities = [count / total for count in counts.values()]
    entropy = -sum(p * log(p) for p in probabilities)
    max_entropy = log(len(counts)) if len(counts) > 1 else 1.0
    return AnswerDistribution(
        counts=dict(counts),
        total=total,
        mode=mode,
        modal_mass=mode_count / total,
        normalized_entropy=entropy / max_entropy if len(counts) > 1 else 0.0,
    )


def wilson_interval(successes: int, trials: int, confidence: float = 0.95) -> tuple[float, float]:
    """Wilson score interval for a binomial proportion."""
    if trials <= 0:
        raise ValueError("trials must be positive")
    if not 0 <= successes <= trials:
        raise ValueError("successes must be between zero and trials")
    if not 0 < confidence < 1:
        raise ValueError("confidence must be between zero and one")
    z = NormalDist().inv_cdf(0.5 + confidence / 2)
    p = successes / trials
    denominator = 1 + z * z / trials
    center = (p + z * z / (2 * trials)) / denominator
    radius = z * sqrt((p * (1 - p) + z * z / (4 * trials)) / trials) / denominator
    return max(0.0, center - radius), min(1.0, center + radius)


def persistent_branch_commitment(
    checkpoints: Sequence[float],
    answer_samples: Sequence[Sequence[Hashable]],
    *,
    threshold: float = 0.8,
    confidence: float = 0.95,
    minimum_persistent_checkpoints: int = 2,
) -> float | None:
    """Return the first checkpoint with a persistent modal answer and Wilson bound.

    Persistence means that the modal answer is identical at every remaining
    checkpoint and each modal-mass Wilson lower bound exceeds ``threshold``.
    """
    if len(checkpoints) != len(answer_samples):
        raise ValueError("checkpoints and answer_samples must have equal length")
    if minimum_persistent_checkpoints < 1:
        raise ValueError("minimum_persistent_checkpoints must be positive")

    summaries = [summarize_answers(samples) for samples in answer_samples]
    for index, (checkpoint, summary) in enumerate(zip(checkpoints, summaries, strict=True)):
        remaining = summaries[index:]
        if len(remaining) < minimum_persistent_checkpoints:
            continue
        if any(candidate.mode != summary.mode for candidate in remaining):
            continue
        lower_bounds = [
            wilson_interval(candidate.counts[candidate.mode], candidate.total, confidence)[0]
            for candidate in remaining
        ]
        if all(bound >= threshold for bound in lower_bounds):
            return checkpoint
    return None


def switch_probability(reference: Hashable, branches: Sequence[Hashable]) -> float:
    """Fraction of branch continuations whose answer differs from a reference."""
    if not branches:
        raise ValueError("branches must be non-empty")
    return sum(answer != reference for answer in branches) / len(branches)

