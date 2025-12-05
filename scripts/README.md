# group_repo_metadata.py

Usage:

python "D:\package\venv310\Scripts\python.exe" scripts\group_repo_metadata.py repo_metadata.jsonl output

This script reads a JSONL file where each line is a JSON object containing a `repo` field and writes separate JSONL files into `output/`, grouped by `repo`. Filenames replace `/` with `__`.
