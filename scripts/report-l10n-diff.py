"""Report which Arabic keys differ from this release's source catalog."""

import importlib.util
from pathlib import Path

root = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("hushgram_l10n", root / "scripts" / "gen-l10n.py")
generator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generator)

keys, others = generator.source_catalog(root)
entries = generator.read(Path(generator.L10N) / "ar.tsv")
allowed = generator.allowed_keys(keys, others)

missing = sorted(keys - entries.keys())
unknown = sorted(entries.keys() - allowed)
print(f"Missing Arabic translations: {len(missing)}")
for key in missing:
    print("MISSING\t" + key)
print(f"Unused or unreachable Arabic entries: {len(unknown)}")
for key in unknown:
    print("UNUSED\t" + key)
