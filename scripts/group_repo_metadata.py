"""Group lines in a JSONL file by the value of the `repo` field.

Usage:
    python -m scripts.group_repo_metadata <input_jsonl> <output_dir>

Exports:
    group_by_repo(input_path: str, output_dir: str) -> None
"""
from __future__ import annotations
import json
import os
from pathlib import Path
from typing import Dict, TextIO


def _repo_to_filename(repo: str) -> str:
    return repo.replace("/", "__") + ".jsonl"


def group_by_repo(input_path: str, output_dir: str) -> None:
    """Read input_path (JSONL) and write grouped files into output_dir.

    Lines that are not valid JSON or do not have a `repo` key are skipped.
    """
    input_path = Path(input_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    open_files: Dict[str, TextIO] = {}
    try:
        with input_path.open("r", encoding="utf-8") as fh:
            for line in fh:
                if not line.strip():
                    continue
                try:
                    obj = json.loads(line)
                except Exception:
                    # Skip invalid JSON lines
                    continue
                repo = obj.get("repo")
                if not repo:
                    continue
                filename = _repo_to_filename(repo)
                out_path = output_dir / filename
                if filename not in open_files:
                    open_files[filename] = out_path.open("a", encoding="utf-8")
                # Write original line as-is
                open_files[filename].write(line.rstrip("\n") + "\n")
    finally:
        for f in open_files.values():
            try:
                f.close()
            except Exception:
                pass


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Group JSONL records by repo field")
    parser.add_argument("input", help="Path to repo_metadata.jsonl")
    parser.add_argument("output", help="Directory to write grouped files")
    args = parser.parse_args()
    group_by_repo(args.input, args.output)
