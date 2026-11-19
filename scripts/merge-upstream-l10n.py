"""Reconcile localization tables after merging upstream into the Arabic branch.

The local tables are authoritative where a key already exists. New upstream rows are
added only when the merged Java sources still reference that key. This preserves local
translations while retaining upstream additions and dropping obsolete catalog entries.
"""
from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
L10N = ROOT / "extensions/shared/library/src/main/l10n"
GENERATOR_PATH = ROOT / "scripts/gen-l10n.py"

spec = importlib.util.spec_from_file_location("hushgram_gen_l10n", GENERATOR_PATH)
if spec is None or spec.loader is None:
    raise SystemExit("Could not load scripts/gen-l10n.py")
generator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generator)


def git_text(revision: str, path: str) -> str | None:
    result = subprocess.run(
        ["git", "show", f"{revision}:{path}"],
        cwd=ROOT,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        return None
    return result.stdout.decode("utf-8")


def parse_blocks(content: str, path: str):
    blocks = []
    pending = []
    seen = set()
    for number, line in enumerate(content.splitlines(), 1):
        if not line or (line.startswith("#") and "\t" not in line):
            pending.append(line)
            continue
        if "\t" not in line:
            raise SystemExit(f"{path}:{number}: expected a tab-separated translation row")
        key = generator.decode_field(line.split("\t", 1)[0])
        if key in seen:
            raise SystemExit(f"{path}:{number}: duplicate key while reconciling: {key}")
        seen.add(key)
        blocks.append((key, pending + [line]))
        pending = []
    return blocks, pending


def reconcile_tables() -> None:
    source_keys, quantity_others = generator.source_catalog(str(ROOT))
    allowed = generator.allowed_keys(source_keys, quantity_others)
    if not L10N.is_dir():
        raise SystemExit(f"Missing localization directory: {L10N}")

    for table in sorted(L10N.glob("*.tsv")):
        relative = table.relative_to(ROOT).as_posix()
        local = git_text("HEAD^1", relative)
        upstream = git_text("HEAD^2", relative)
        if local is None and upstream is None:
            continue
        local_blocks, local_tail = parse_blocks(local or "", relative)
        upstream_blocks, upstream_tail = parse_blocks(upstream or "", relative)

        chosen = {}
        ordered = []
        for key, block in local_blocks:
            if key in allowed and key not in chosen:
                chosen[key] = block
                ordered.append(key)
        for key, block in upstream_blocks:
            if key in allowed and key not in chosen:
                chosen[key] = block
                ordered.append(key)

        missing = sorted(source_keys - chosen.keys())
        if missing:
            preview = "\n".join(f"  - {key}" for key in missing[:40])
            raise SystemExit(
                f"{relative}: {len(missing)} source strings still need a translation.\n{preview}"
            )

        output = []
        for key in ordered:
            output.extend(chosen[key])
        tail = []
        for line in local_tail + upstream_tail:
            if line not in tail:
                tail.append(line)
        output.extend(tail)
        table.write_text("\n".join(output).rstrip("\n") + "\n", encoding="utf-8", newline="\n")


def unreleased_bounds(lines):
    start = next((i for i, line in enumerate(lines) if line.strip() == "## Unreleased"), None)
    if start is None:
        return None
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    return start, end


def merge_changelog() -> None:
    local = git_text("HEAD^1", "CHANGELOG.md")
    upstream = git_text("HEAD^2", "CHANGELOG.md")
    if local is None or upstream is None:
        return
    lines = local.splitlines()
    upstream_lines = upstream.splitlines()
    bounds = unreleased_bounds(lines)
    upstream_bounds = unreleased_bounds(upstream_lines)
    if bounds is None or upstream_bounds is None:
        return
    start, end = bounds
    up_start, up_end = upstream_bounds
    headings = [
        (i, line) for i, line in enumerate(upstream_lines[up_start + 1:up_end], up_start + 1)
        if line.startswith("### ")
    ]
    for heading_index, heading in headings:
        next_heading = next(
            (i for i, line in headings if i > heading_index),
            up_end,
        )
        bullets = [
            line for line in upstream_lines[heading_index + 1:next_heading]
            if line.startswith("* ")
        ]
        local_heading = next(
            (i for i in range(start + 1, end) if lines[i] == heading),
            None,
        )
        if local_heading is None:
            insert_at = end
            lines[insert_at:insert_at] = ["", heading, ""]
            start, end = unreleased_bounds(lines)
            local_heading = next(i for i in range(start + 1, end) if lines[i] == heading)
        local_group_end = next(
            (i for i in range(local_heading + 1, end) if lines[i].startswith("### ")),
            end,
        )
        existing = set(lines[local_heading + 1:local_group_end])
        additions = [bullet for bullet in bullets if bullet not in existing]
        if additions:
            insert_at = local_group_end
            while insert_at > local_heading + 1 and not lines[insert_at - 1].strip():
                insert_at -= 1
            lines[insert_at:insert_at] = additions + [""]
            start, end = unreleased_bounds(lines)
    (ROOT / "CHANGELOG.md").write_text("\n".join(lines).rstrip("\n") + "\n", encoding="utf-8", newline="\n")


def main() -> None:
    reconcile_tables()
    merge_changelog()
    print("Upstream localization tables reconciled; local translations preserved.")


if __name__ == "__main__":
    main()
