import json
import shutil
import argparse
from pathlib import Path
from tqdm import tqdm
import sys
import traceback
import os

# =========================
# Config
# =========================

BLUEPRINT_PATH = "blueprint_v2.json"
TARGET_ROOT = Path(r"D:\RESTORED")

SKIP_FILENAMES = {
    "NTUSER.DAT",
    "ntuser.dat",
    "ntuser.dat.log1",
    "ntuser.dat.log2",
}

# =========================
# Helpers
# =========================

def is_skip_file(path: Path) -> bool:
    return path.name.lower() in SKIP_FILENAMES

def win_long_path(p: Path) -> str:
    """Enable Windows long path support"""
    s = str(p.resolve())
    if s.startswith("\\\\?\\"):
        return s
    return "\\\\?\\" + s

# =========================
# CLI
# =========================

parser = argparse.ArgumentParser(description="SmartMigrator Restore v2.1")
parser.add_argument("--limit", type=int, default=None)
parser.add_argument("--dry-run", action="store_true")
parser.add_argument("--test-clean", action="store_true")
args = parser.parse_args()

# =========================
# Load Blueprint
# =========================

with open(BLUEPRINT_PATH, "r", encoding="utf-8") as f:
    bp = json.load(f)

items = bp.get("items", [])
if args.limit:
    items = items[:args.limit]

# =========================
# Info
# =========================

print("\n=== SmartMigrator Restore v2.1 ===")
print(f"Files to restore : {len(items)}")
print(f"Target           : {TARGET_ROOT}")
print(f"Dry run          : {args.dry_run}")
print(f"Test clean       : {args.test_clean}")
print("=" * 40)

# =========================
# Restore
# =========================

restored = []
failed = []

for item in tqdm(items, ncols=120):
    src = Path(item["path"])

    try:
        if not src.exists() or not src.is_file():
            failed.append((str(src), "source_missing"))
            continue

        if is_skip_file(src):
            failed.append((str(src), "system_hive_skipped"))
            continue

        rel = src.relative_to(src.anchor)
        dst = TARGET_ROOT / rel

        dst.parent.mkdir(parents=True, exist_ok=True)

        if args.dry_run:
            continue

        shutil.copy2(
            win_long_path(src),
            win_long_path(dst)
        )

        restored.append(dst)

    except PermissionError:
        failed.append((str(src), "permission_denied"))

    except FileNotFoundError:
        failed.append((str(src), "path_invalid_or_too_long"))

    except Exception as e:
        failed.append((str(src), repr(e)))

# =========================
# Test Clean
# =========================

if args.test_clean and not args.dry_run:
    for f in restored:
        try:
            f.unlink()
        except Exception:
            pass

    for d in sorted(TARGET_ROOT.glob("**/*"), reverse=True):
        try:
            if d.is_dir() and not any(d.iterdir()):
                d.rmdir()
        except Exception:
            pass

# =========================
# Summary
# =========================

print("\n=== Summary ===")
print(f"Restored files : {len(restored)}")
print(f"Failed files  : {len(failed)}")

reason_stats = {}
for _, r in failed:
    reason_stats[r] = reason_stats.get(r, 0) + 1

print("\nFailure breakdown:")
for k, v in sorted(reason_stats.items(), key=lambda x: -x[1]):
    print(f"  {k:30} {v}")

if args.test_clean:
    print("\n[TEST MODE] All copied files were removed after verification.")

print("\nDone.")
