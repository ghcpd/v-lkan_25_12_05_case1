import json
import os
import tempfile

from scripts.group_repo_metadata import group_by_repo


def test_group_by_repo(tmp_path):
    data = [
        {"repo": "owner/repo1", "pr": 1},
        {"repo": "owner/repo2", "pr": 2},
        {"repo": "owner/repo1", "pr": 3},
    ]

    input_file = tmp_path / "repo_metadata.jsonl"
    with input_file.open("w", encoding="utf-8") as fh:
        for item in data:
            fh.write(json.dumps(item) + "\n")

    out_dir = tmp_path / "out"
    files = group_by_repo(str(input_file), str(out_dir))

    assert sorted(files) == ["owner__repo1.jsonl", "owner__repo2.jsonl"]

    # read repo1 file
    with (out_dir / "owner__repo1.jsonl").open("r", encoding="utf-8") as fh:
        lines = [json.loads(l) for l in fh]
    assert lines == [data[0], data[2]]


def test_missing_repo_field(tmp_path):
    input_file = tmp_path / "bad.jsonl"
    with input_file.open("w", encoding="utf-8") as fh:
        fh.write(json.dumps({"pr": 1}) + "\n")

    out_dir = tmp_path / "out"
    try:
        group_by_repo(str(input_file), str(out_dir))
        raise AssertionError("Expected ValueError for missing repo field")
    except ValueError as exc:
        assert "Missing 'repo'" in str(exc)
