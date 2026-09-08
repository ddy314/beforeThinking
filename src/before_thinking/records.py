"""Artifact schemas. Every generated row carries lineage and decoding state."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class GenerationSettings(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    temperature: float = Field(gt=0)
    top_p: float = Field(gt=0, le=1)
    top_k: int = Field(ge=0)
    max_new_tokens: int = Field(gt=0)
    seed: int = Field(ge=0)


class TrajectoryRecord(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: int = 1
    item_id: str
    task: str
    rollout_id: str
    parent_rollout_id: str | None = None
    prefix_token_count: int | None = None
    model_id: str
    model_revision: str
    tokenizer_hash: str
    prompt_token_ids: list[int]
    generated_token_ids: list[int]
    thinking_token_count: int
    final_answer_raw: str | None
    final_answer_canonical: str | None
    parse_ok: bool
    correct: bool | None
    settings: GenerationSettings

