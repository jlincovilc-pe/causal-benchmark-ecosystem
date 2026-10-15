#!/usr/bin/env python3
"""Run read-only release checks for the complete benchmark repository.

The script never writes inside the repository. Synthetic validation reports are
written to a temporary directory and deleted when the process exits.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_MARKERS = ("RELEASE_README.md", "https://github.com/OWNER/")
IGNORED_DIR_NAMES = {"build", "dist", ".pytest_cache", "__pycache__", ".benchmarks"}


def check_index() -> dict[str, Any]:
    index = ROOT / "causal_benchmark_synthetic" / "release_index" / "dataset_index.csv"
    rows = list(csv.DictReader(index.open(newline="", encoding="utf-8")))
    missing = []
    for row in rows:
        rel = row.get("dataset", "")
        path = ROOT / "causal_benchmark_synthetic" / rel.removeprefix("datasets/")
        # The index stores paths relative to the synthetic component.
        path = ROOT / "causal_benchmark_synthetic" / rel
        if not path.is_dir():
            missing.append(rel)
        if not (path / "metadata.json").exists():
            missing.append(f"{rel}/metadata.json")
        if not any((path / name).exists() for name in ("observed_train.csv", "observed.csv", "data_public.csv", "data.csv", "data_observed.csv")):
            missing.append(f"{rel}/observable-data")
    return {"scenarios": len(rows), "missing": missing}


def check_links_and_markers() -> list[str]:
    issues: list[str] = []
    for path in ROOT.rglob("*.md"):
        if any(part in IGNORED_DIR_NAMES for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for marker in FORBIDDEN_MARKERS:
            if marker in text:
                issues.append(f"{path.relative_to(ROOT)} contains stale marker {marker}")
        for target in re.findall(r"\[[^]]+\]\(([^)#]+)", text):
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            target_path = (path.parent / target).resolve()
            if not target_path.exists():
                issues.append(f"{path.relative_to(ROOT)} -> missing link {target}")
    return issues


def run_synthetic_validator() -> dict[str, Any]:
    script = ROOT / "causal_benchmark_synthetic" / "scripts" / "00_validate_benchmark.py"
    with tempfile.TemporaryDirectory(prefix="causal-benchmark-validation-") as tmp:
        result = subprocess.run(
            [sys.executable, str(script), "--root", str(ROOT / "causal_benchmark_synthetic"), "--output", str(Path(tmp) / "validation")],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        if result.returncode not in (0, 1):
            raise RuntimeError(result.stderr.strip() or result.stdout.strip())
        payload = json.loads((Path(tmp) / "validation" / "validation_report.json").read_text())
        payload["process_returncode"] = result.returncode
        return payload


def check_zoo_registry() -> dict[str, Any]:
    registry = ROOT / "causal_benchmark_zoo" / "benchmarks" / "registry.yaml"
    try:
        import yaml  # type: ignore
    except ImportError as exc:
        raise RuntimeError("PyYAML is required; install requirements.txt") from exc
    data = yaml.safe_load(registry.read_text(encoding="utf-8")) or {}
    ids = [item["id"] for item in data.get("benchmarks", [])]
    missing = [item for item in ids if not (registry.parent / item / "manifest.yaml").exists()]
    return {"registered": ids, "missing_manifests": missing}


def check_release_manifest() -> dict[str, Any]:
    """Verify every recorded hash without hashing the manifest itself."""
    manifest_path = ROOT / "RELEASE_MANIFEST.json"
    if not manifest_path.exists():
        return {"present": False, "issues": ["RELEASE_MANIFEST.json is missing"]}
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    issues: list[str] = []
    recorded = {item["path"]: item for item in payload.get("files", [])}
    for rel, item in recorded.items():
        path = ROOT / rel
        if not path.is_file():
            issues.append(f"manifest file missing: {rel}")
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != item.get("sha256"):
            issues.append(f"manifest hash mismatch: {rel}")
    # Files omitted from the manifest are usually an accidental untracked
    # release artifact. Apply the same exclusions as the generator.
    excluded = {".git", ".pytest_cache", "__pycache__", ".ipynb_checkpoints", "build", "dist", ".benchmarks"}
    actual = {
        path.relative_to(ROOT).as_posix()
        for path in ROOT.rglob("*")
        if path.is_file()
        and path.name != manifest_path.name
        and not path.suffix in {".pyc", ".pyo"}
        and not any(part in excluded for part in path.relative_to(ROOT).parts)
        and not any(part.endswith(".egg-info") for part in path.relative_to(ROOT).parts)
    }
    omitted = sorted(actual - set(recorded))
    issues.extend(f"manifest omitted file: {rel}" for rel in omitted)
    return {"present": True, "file_count": len(recorded), "issues": issues}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", dest="json_path", help="write the summary to this path")
    args = parser.parse_args()

    index = check_index()
    link_issues = check_links_and_markers()
    synthetic = run_synthetic_validator()
    zoo = check_zoo_registry()
    manifest = check_release_manifest()
    failures = []
    if index["scenarios"] != 43:
        failures.append(f"expected 43 scenarios, found {index['scenarios']}")
    failures.extend(index["missing"])
    failures.extend(link_issues)
    failures.extend(f"missing manifest: {x}" for x in zoo["missing_manifests"])
    failures.extend(manifest["issues"])
    if synthetic["total_errors"]:
        failures.append(f"synthetic validator reported {synthetic['total_errors']} errors")

    summary = {
        "repository": str(ROOT),
        "index": index,
        "synthetic_validation": {k: synthetic[k] for k in ("n_datasets", "status_counts", "total_errors", "total_warnings", "process_returncode")},
        "zoo_registry": zoo,
        "release_manifest": manifest,
        "link_or_marker_issues": link_issues,
        "failures": failures,
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    if args.json_path:
        Path(args.json_path).write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
