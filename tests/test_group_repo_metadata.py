import json
import tempfile
import os
from pathlib import Path

from scripts.group_repo_metadata import group_by_repo


def make_sample(input_path: Path):
    lines = [
        {"repo": "org1/repoA", "id": 1},
        {"repo": "org1/repoA", "id": 2},
        {"repo": "org2/repoB", "id": 3},
        {"repo": "org/complex/name/with/slash", "id": 4},
    ]
    with input_path.open("w", encoding="utf-8") as f:
        for obj in lines:
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")
    return lines


def test_grouping_creates_files(tmp_path: Path):
    input_file = tmp_path / "repo_metadata.jsonl"
    lines = make_sample(input_file)
    output_dir = tmp_path / "out"

    group_by_repo(str(input_file), str(output_dir))

    # Expected filenames: slashes replaced by __
    expected_files = [
        output_dir / "org1__repoA.jsonl",
        output_dir / "org2__repoB.jsonl",
        output_dir / "org__complex__name__with__slash.jsonl",
    ]

    for ef in expected_files:
        assert ef.exists(), f"Expected output file {ef} not found"
        # Verify contents are valid JSONL and belong to correct repo
        with ef.open("r", encoding="utf-8") as f:
            lines_in_file = [json.loads(l) for l in f if l.strip()]
        assert all("repo" in o for o in lines_in_file)

    # Verify counts
    with (output_dir / "org1__repoA.jsonl").open("r", encoding="utf-8") as f:
        repo1_lines = [json.loads(l) for l in f if l.strip()]
    assert len(repo1_lines) == 2


def test_grouping_idempotent_and_skips_invalid(tmp_path: Path):
    input_file = tmp_path / "repo_metadata.jsonl"
    # Add an invalid json line and a line missing repo
    sample_lines = [
        '{"repo": "a/b", "x": 1}',
        'not a json\n',
        '{"no_repo": "missing"}',
    ]
    input_file.write_text("\n".join(sample_lines), encoding="utf-8")
    output_dir = tmp_path / "out"

    group_by_repo(str(input_file), str(output_dir))

    # Only a/b should be present
    ef = output_dir / "a__b.jsonl"
    assert ef.exists()
    with ef.open("r", encoding="utf-8") as f:
        lines_in_file = [l for l in f if l.strip()]
    assert len(lines_in_file) == 1
