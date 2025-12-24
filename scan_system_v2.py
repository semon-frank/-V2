import os, json

OUTPUT = "state/scan_state.json"

SCAN_ROOTS = [
    os.path.expanduser("~"),
    "C:/Program Files",
    "C:/Program Files (x86)"
]

os.makedirs("state", exist_ok=True)

files = []

for root in SCAN_ROOTS:
    for dirpath, _, filenames in os.walk(root):
        for f in filenames:
            try:
                full = os.path.join(dirpath, f)
                size = os.path.getsize(full)
                files.append({
                    "path": full,
                    "size": size
                })
            except:
                continue

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(files, f, indent=2)

print(f"Scan complete: {len(files)} files")
