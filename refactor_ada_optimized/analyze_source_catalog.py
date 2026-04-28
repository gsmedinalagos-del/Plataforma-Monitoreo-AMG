#!/usr/bin/env python3
"""Static analyzer for KQL source catalog/dependency map.

Scans refactor_ada_optimized/law_functions and reports:
- fn_src_mlp_* definitions
- consumers per source
- domains/helpers using sources
- cross-product usage and top shared sources
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
LAW = ROOT / "law_functions"
SOURCES_DIR = LAW / "sources"

DEF_RE = re.compile(r"\blet\s+(fn_src_mlp_[A-Za-z0-9_]+)\s*=\s*\(")
SRC_CALL_RE = re.compile(r"\b(fn_src_mlp_[A-Za-z0-9_]+)\s*\(")
TABLE_LITERAL_RE = re.compile(r'\.table\("([A-Za-z0-9_]+)"\)')
WS_NAME_RE = re.compile(r"workspaces/([a-z0-9-]+)")


@dataclass
class SourceInfo:
    name: str
    path: Path
    source_type: str
    workspace_logical: str
    tables: list[str]


def classify_source(name: str) -> str:
    return "workspace genérico" if name.startswith("fn_src_mlp_ws_") else "agregador product-level"


def infer_workspace_logical(name: str, text: str) -> str:
    if name.startswith("fn_src_mlp_ws_"):
        return name.removeprefix("fn_src_mlp_ws_")
    if "pipeline_runs" in name:
        return "multi-ws: dispatch/drillit/blkgrde"
    if "ssag_systemlogs" in name:
        return "multi-ws: ssag/plans/pdmsagi/pisystem"
    if "systemlogs_all" in name:
        return "multi-ws: ada/meteo/pisystem/plans"
    ws_names = sorted(set(WS_NAME_RE.findall(text)))
    return ", ".join(ws_names) if ws_names else "n/a"


def infer_tables(name: str, text: str) -> list[str]:
    tables = sorted(set(TABLE_LITERAL_RE.findall(text)))
    if tables:
        return tables
    if name.startswith("fn_src_mlp_ws_"):
        return ["tableName (parámetro)"]
    return ["derivadas de workspace sources"]


def product_from_path(path: Path) -> str:
    parts = path.parts
    if "ada" in parts:
        return "ADA"
    if "notpii" in parts:
        return "NOTPII"
    if "sirosag" in parts:
        return "SIROSAG"
    if "sources" in parts:
        return "Capa Source"
    return "Otro"


def role_from_path(path: Path) -> str:
    if "domains" in path.parts:
        return "domain"
    if "helpers" in path.parts:
        return "helper"
    if "sources" in path.parts:
        return "source"
    return "otro"


def main() -> None:
    source_infos: dict[str, SourceInfo] = {}
    all_kql = sorted(LAW.rglob("*.kql"))

    for path in sorted(SOURCES_DIR.glob("fn_src_mlp_*.kql")):
        text = path.read_text(encoding="utf-8")
        m = DEF_RE.search(text)
        if not m:
            continue
        name = m.group(1)
        source_infos[name] = SourceInfo(
            name=name,
            path=path,
            source_type=classify_source(name),
            workspace_logical=infer_workspace_logical(name, text),
            tables=infer_tables(name, text),
        )

    source_consumers: dict[str, list[Path]] = defaultdict(list)
    consumer_sources: dict[Path, set[str]] = defaultdict(set)

    for path in all_kql:
        text = path.read_text(encoding="utf-8")
        calls = set(SRC_CALL_RE.findall(text))
        for call in calls:
            if call in source_infos and not ("sources" in path.parts and path.name == source_infos[call].path.name):
                source_consumers[call].append(path)
                consumer_sources[path].add(call)

    product_sources: dict[str, set[str]] = defaultdict(set)
    domains_helpers_using_sources = []
    for path, srcs in sorted(consumer_sources.items()):
        role = role_from_path(path)
        if role in {"domain", "helper"}:
            domains_helpers_using_sources.append(path)
        product_sources[product_from_path(path)].update(srcs)

    consumer_count = {s: len(set(ps)) for s, ps in source_consumers.items()}
    top_shared = sorted(consumer_count.items(), key=lambda x: (-x[1], x[0]))

    print("# Source catalog summary")
    print(f"Total sources: {len(source_infos)}")
    print("Workspace sources:", sum(1 for s in source_infos.values() if s.source_type == "workspace genérico"))
    print("Aggregators:", sum(1 for s in source_infos.values() if s.source_type == "agregador product-level"))
    print(f"Domains/helpers using sources: {len(domains_helpers_using_sources)}")
    print("\nTop shared sources:")
    for name, count in top_shared[:5]:
        print(f"- {name}: {count}")

    print("\nSource -> consumers")
    for name in sorted(source_infos):
        consumers = sorted({str(p.relative_to(ROOT)) for p in source_consumers.get(name, [])})
        print(f"- {name}: {len(consumers)}")
        for c in consumers:
            print(f"  - {c}")

    print("\nProduct -> sources")
    for product in sorted(product_sources):
        srcs = sorted(product_sources[product])
        print(f"- {product}: {len(srcs)}")
        for s in srcs:
            print(f"  - {s}")


if __name__ == "__main__":
    main()
