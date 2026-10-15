#!/usr/bin/env python3
"""Generate the file-level SHA-256 manifest for this benchmark release."""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import platform
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_DIRS = {".git", ".pytest_cache", "__pycache__", ".ipynb_checkpoints", "build", "dist", ".benchmarks"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}
DEFAULT_OUTPUT = ROOT / "RELEASE_MANIFEST.json"


def release_version() -> str:
    citation = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    match = re.search(r"^version:\s*([^\s]+)", citation, flags=re.MULTILINE)
    if not match:
        raise RuntimeError("CITATION.cff does not declare a release version")
    return match.group(1)


def include(path: Path, output: Path) -> bool:
    if path.resolve() == output.resolve():
        return False
    if any(part in EXCLUDED_DIRS for part in path.relative_to(ROOT).parts):
        return False
    if path.suffix in EXCLUDED_SUFFIXES or any(part.endswith(".egg-info") for part in path.relative_to(ROOT).parts):
        return False
    return path.is_file()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def version(name: str) -> str | None:
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args()
    output = Path(args.output)
    if not output.is_absolute():
        output = (ROOT / output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    files = []
    for path in sorted(ROOT.rglob("*")):
        if include(path, output):
            files.append({
                "path": path.relative_to(ROOT).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            })

    payload = {
        "manifest_schema": "1.0",
        "release": release_version(),
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "generator": "scripts/generate_release_manifest.py",
        "scope": "All source, documentation, manifests and benchmark artifacts under this repository, excluding RELEASE_MANIFEST.json and generated/cache directories.",
        "excluded_directories": sorted(EXCLUDED_DIRS),
        "environment": {
            "python": platform.python_version(),
            "implementation": platform.python_implementation(),
            "platform": platform.platform(),
            "packages": {name: version(name) for name in ("numpy", "pandas", "scipy", "scikit-learn", "networkx", "PyYAML", "jsonschema", "pytest")},
        },
        "file_count": len(files),
        "total_bytes": sum(item["bytes"] for item in files),
        "files": files,
    }
    output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "file_count": len(files), "total_bytes": payload["total_bytes"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
