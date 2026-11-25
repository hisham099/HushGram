"""Filter Arabic translations to keys present in the exact v0.0.22 source."""
import importlib.util
from pathlib import Path
import sys
root = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("gen_l10n", root / "scripts" / "gen-l10n.py")
gen = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gen)
table_path = root / "extensions/shared/library/src/main/l10n/ar.tsv"
entries = gen.read(str(table_path))
keys, others = gen.source_catalog()
allowed = gen.allowed_keys(keys, others)
missing = set(keys) - entries.keys()
unknown = entries.keys() - allowed
if missing:
    print("Missing Arabic translations:", len(missing))
    for key in sorted(missing): print("MISSING:", key)
    sys.exit(1)
def esc(s): return s.replace("\\", "\\\\").replace("\n", "\\n").replace("\t", "\\t")
lines = ["# Arabic translations filtered against the exact v0.0.22 source catalog."]
for key in sorted(entries):
    if key in allowed: lines.append(esc(key) + "\t" + esc(entries[key]))
table_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Kept {sum(1 for key in entries if key in allowed)} translations; dropped {len(unknown)} unreachable newer keys.")