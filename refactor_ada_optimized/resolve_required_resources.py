#!/usr/bin/env python3
"""Resolve required workspace resource IDs for a function/source call.

Usage:
  python refactor_ada_optimized/resolve_required_resources.py fn_src_mlp_ws_plans
  python refactor_ada_optimized/resolve_required_resources.py fn_prd_mlp_ada_dom_dispatch_status
"""
from __future__ import annotations
from pathlib import Path
import re
import sys
from collections import defaultdict, deque

ROOT = Path(__file__).resolve().parent
LAW = ROOT / "law_functions"

DEF_RE = re.compile(r"\blet\s+(fn_[A-Za-z0-9_]+)\s*=\s*\(")
CALL_RE = re.compile(r"\b(fn_[A-Za-z0-9_]+)\s*\(")
WS_RE = re.compile(r'workspace\("([^"]+)"\)')


def build_index():
    defs = {}
    calls = defaultdict(set)
    refs = defaultdict(set)
    for p in LAW.rglob("*.kql"):
        txt = p.read_text(encoding="utf-8")
        m = DEF_RE.search(txt)
        if not m:
            continue
        fn = m.group(1)
        defs[fn] = p
        for c in set(CALL_RE.findall(txt)):
            if c != fn:
                calls[fn].add(c)
        for w in set(WS_RE.findall(txt)):
            refs[fn].add(w)
    return defs, calls, refs


def resolve(target: str, defs, calls, refs):
    if target not in defs:
        raise SystemExit(f"Function not found: {target}")
    q = deque([target])
    seen = set()
    out = set()
    while q:
        fn = q.popleft()
        if fn in seen:
            continue
        seen.add(fn)
        out |= refs.get(fn, set())
        for nxt in calls.get(fn, set()):
            if nxt in defs:
                q.append(nxt)
    return sorted(out), sorted(seen)


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python resolve_required_resources.py <function_name>")
    target = sys.argv[1].strip()
    defs, calls, refs = build_index()
    resources, closure = resolve(target, defs, calls, refs)
    print(f"Target: {target}")
    print(f"Functions in dependency closure: {len(closure)}")
    for fn in closure:
        print(f"  - {fn}")
    print("\nRequired workspace resource IDs:")
    if not resources:
        print("  (none)")
    else:
        for r in resources:
            print(f"  - {r}")


if __name__ == "__main__":
    main()
