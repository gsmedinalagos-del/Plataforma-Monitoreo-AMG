#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
MARKER_RE = re.compile(r'^(<<<<<<< .+|=======|>>>>>>> .+)$', re.M)
SKIP_DIRS = {'.git', 'node_modules', '.venv', 'venv', '__pycache__'}
TEXT_EXT = {'.kql', '.md', '.py', '.json', '.yml', '.yaml', '.txt', '.sh'}

errors = []
for path in ROOT.rglob('*'):
    if not path.is_file():
        continue
    if any(part in SKIP_DIRS for part in path.parts):
        continue
    if path.suffix.lower() not in TEXT_EXT:
        continue
    try:
        text = path.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        continue
    if MARKER_RE.search(text):
        errors.append(path.relative_to(ROOT))

if errors:
    print('Conflict markers FOUND')
    for p in errors:
        print(f'- {p}')
    sys.exit(1)

print('Conflict markers NOT FOUND')
