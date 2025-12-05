#!/usr/bin/env python3
"""
Group JSONL records by the `repo` field and write each group to its own JSONL file.

Usage:
  python scripts/group_repo_metadata.py <input_jsonl> <output_dir>

If output_dir does not exist it will be created. Filenames are the `repo` value with
`/` replaced by `__` and `.jsonl` appended.
"""
import json
import os
import sys
from collections import defaultdict


def group_by_repo(input_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    groups = defaultdict(list)

    with open(input_path, "r", encoding="utf-8") as fh:
        for line_no, line in enumerate(fh, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON on line {line_no}: {exc}")

            repo = obj.get("repo")
            if not repo:
                raise ValueError(f"Missing 'repo' field on line {line_no}")

            groups[repo].append(obj)

    for repo, entries in groups.items():
        filename = repo.replace("/", "__") + ".jsonl"
        out_path = os.path.join(output_dir, filename)
        with open(out_path, "w", encoding="utf-8") as out_fh:
            for item in entries:
                out_fh.write(json.dumps(item, ensure_ascii=False) + "\n")

    return sorted([repo.replace("/", "__") + ".jsonl" for repo in groups.keys()])


def main(argv):
    if len(argv) != 3:
        print("Usage: group_repo_metadata.py <input_jsonl> <output_dir>", file=sys.stderr)
        return 2

    input_path, output_dir = argv[1], argv[2]
    files = group_by_repo(input_path, output_dir)
    print(f"Wrote {len(files)} files to {output_dir}")
    for f in files:
        print(f)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
