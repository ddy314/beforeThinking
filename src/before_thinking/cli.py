"""Small operational commands for the local research environment."""

from __future__ import annotations

import json
import os
import platform
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from importlib import metadata
from pathlib import Path
from typing import Any, cast

import typer

app = typer.Typer(no_args_is_help=True)


@app.callback()
def main() -> None:
    """Inspect and operate the Before Thinking research harness."""


def _package_version(name: str) -> str | None:
    try:
        return metadata.version(name)
    except metadata.PackageNotFoundError:
        return None


def collect_doctor_report() -> dict[str, Any]:
    report: dict[str, Any] = {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "executables": {name: shutil.which(name) for name in ("uv", "git", "nvidia-smi", "nvcc")},
        "packages": {
            name: _package_version(name)
            for name in ("torch", "transformers", "datasets", "numpy", "scikit-learn")
        },
    }
    try:
        import torch

        report["torch"] = {
            "cuda_available": torch.cuda.is_available(),
            "compiled_cuda": torch.version.cuda,
            "device_count": torch.cuda.device_count(),
            "device_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
            "bf16_supported": (
                torch.cuda.is_bf16_supported() if torch.cuda.is_available() else False
            ),
        }
    except ImportError:
        report["torch"] = {"cuda_available": False, "error": "torch is not installed"}
    return report


def _model_snapshot_dir(model_id: str, revision: str) -> Path:
    hf_home = Path(os.environ.get("HF_HOME", Path.home() / ".cache" / "huggingface"))
    safe_model_id = model_id.replace("/", "--")
    return hf_home / "aria2" / safe_model_id / revision


def _download_model_file(
    *,
    aria2c: str,
    model_id: str,
    revision: str,
    snapshot_dir: Path,
    sibling: Any,
    connections: int,
    splits: int,
) -> str:
    filename = str(sibling.rfilename)
    relative_path = Path(filename)
    target = snapshot_dir / relative_path
    target.parent.mkdir(parents=True, exist_ok=True)

    if target.is_file() and sibling.size is not None and target.stat().st_size == sibling.size:
        return filename

    from huggingface_hub import hf_hub_url

    command = [
        aria2c,
        "--allow-overwrite=false",
        "--auto-file-renaming=false",
        "--check-integrity=true",
        "--continue=true",
        "--file-allocation=none",
        f"--max-connection-per-server={connections}",
        "--max-tries=5",
        "--min-split-size=1M",
        "--retry-wait=5",
        f"--split={splits}",
        "--timeout=60",
        "--connect-timeout=30",
        f"--dir={target.parent}",
        f"--out={target.name}",
    ]
    if sibling.lfs is not None:
        command.append(f"--checksum=sha-256={sibling.lfs.sha256}")
    command.append(hf_hub_url(model_id, filename, revision=revision))
    subprocess.run(command, check=True)
    if not target.is_file() or (
        sibling.size is not None and target.stat().st_size != sibling.size
    ):
        raise RuntimeError(f"aria2c finished but downloaded file is incomplete: {target}")
    return filename


def download_model_with_aria2(
    model_id: str,
    revision: str,
    *,
    connections: int = 16,
    splits: int = 16,
    parallel_files: int = 2,
) -> Path:
    """Download a pinned Hub snapshot with aria2c and return its local path."""
    aria2c = shutil.which("aria2c")
    if aria2c is None:
        raise RuntimeError(
            "aria2c is required for model downloads; install the aria2 package and retry"
        )
    if min(connections, splits, parallel_files) < 1:
        raise ValueError("aria2 connection, split, and parallel-file counts must be positive")

    from huggingface_hub import HfApi

    info = HfApi().model_info(model_id, revision=revision, files_metadata=True)
    siblings = list(info.siblings or [])
    if not siblings:
        raise RuntimeError(f"Hugging Face repository has no files: {model_id}@{revision}")

    snapshot_dir = _model_snapshot_dir(model_id, revision)
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=parallel_files) as pool:
        futures = [
            pool.submit(
                _download_model_file,
                aria2c=aria2c,
                model_id=model_id,
                revision=revision,
                snapshot_dir=snapshot_dir,
                sibling=sibling,
                connections=connections,
                splits=splits,
            )
            for sibling in siblings
        ]
        for future in futures:
            future.result()

    manifest = {
        "model_id": model_id,
        "revision": revision,
        "files": [sibling.rfilename for sibling in siblings],
        "downloader": "aria2c",
    }
    (snapshot_dir / "download-manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return snapshot_dir


@app.command("download-model")
def download_model(
    model_id: str = "Qwen/Qwen3-1.7B",
    revision: str = "70d244cc86ccca08cf5af4e1e306ecf908b1ad5e",
    connections: int = typer.Option(16, min=1, help="Connections per file."),
    splits: int = typer.Option(16, min=1, help="Segments per file."),
    parallel_files: int = typer.Option(2, min=1, help="Files downloaded concurrently."),
) -> None:
    """Download a pinned model snapshot with aria2c."""
    snapshot_dir = download_model_with_aria2(
        model_id,
        revision,
        connections=connections,
        splits=splits,
        parallel_files=parallel_files,
    )
    typer.echo(json.dumps({"model_id": model_id, "revision": revision, "path": str(snapshot_dir)}))


@app.command()
def doctor() -> None:
    """Print a machine-readable environment and CUDA readiness report."""
    typer.echo(json.dumps(collect_doctor_report(), indent=2, sort_keys=True))


@app.command("model-smoke")
def model_smoke(
    model_id: str = "Qwen/Qwen3-1.7B",
    revision: str = "70d244cc86ccca08cf5af4e1e306ecf908b1ad5e",
    max_new_tokens: int = typer.Option(32, min=1, max=128),
    connections: int = typer.Option(16, min=1, help="aria2 connections per file."),
    splits: int = typer.Option(16, min=1, help="aria2 segments per file."),
    parallel_files: int = typer.Option(2, min=1, help="aria2 files downloaded concurrently."),
) -> None:
    """Download a pinned model with aria2c, generate briefly, and capture hidden states."""
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer, set_seed

    if not torch.cuda.is_available():
        raise typer.BadParameter("CUDA is required for the registered local smoke")

    snapshot_dir = download_model_with_aria2(
        model_id,
        revision,
        connections=connections,
        splits=splits,
        parallel_files=parallel_files,
    )
    tokenizer = AutoTokenizer.from_pretrained(  # type: ignore[no-untyped-call]
        snapshot_dir, local_files_only=True
    )
    model = AutoModelForCausalLM.from_pretrained(
        snapshot_dir,
        local_files_only=True,
        dtype=torch.bfloat16,
        device_map="cuda",
        attn_implementation="eager",
    )
    messages = [{"role": "user", "content": "What is 17 + 28? Give the final integer."}]
    encoded = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        enable_thinking=True,
        tokenize=True,
        return_dict=True,
        return_tensors="pt",
    ).to(model.device)
    set_seed(1729)
    with torch.inference_mode():
        generated = cast(
            torch.Tensor,
            model.generate(
                **encoded,
                do_sample=True,
                temperature=0.6,
                top_p=0.95,
                top_k=20,
                max_new_tokens=max_new_tokens,
            ),
        )
        prefix = generated[:, : encoded["input_ids"].shape[1] + 1]
        hidden_output = model(
            input_ids=prefix,
            attention_mask=torch.ones_like(prefix),
            output_hidden_states=True,
            use_cache=False,
        )

    hidden_states = hidden_output.hidden_states
    if hidden_states is None:
        raise RuntimeError("model did not return hidden states")
    report = {
        "model_id": model_id,
        "revision": revision,
        "model_path": str(snapshot_dir),
        "hf_home": os.environ.get("HF_HOME"),
        "prompt_tokens": encoded["input_ids"].shape[1],
        "generated_tokens": generated.shape[1] - encoded["input_ids"].shape[1],
        "hidden_state_tensors": len(hidden_states),
        "hidden_size": hidden_states[-1].shape[-1],
        "hidden_finite": bool(torch.isfinite(hidden_states[-1]).all().item()),
        "peak_cuda_memory_mib": round(torch.cuda.max_memory_allocated() / 2**20, 1),
        "decoded_suffix": tokenizer.decode(
            generated[0, encoded["input_ids"].shape[1] :], skip_special_tokens=False
        ),
    }
    typer.echo(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    app()
