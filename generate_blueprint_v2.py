import json
from datetime import datetime, UTC

with open("state/scan_state.json", "r", encoding="utf-8") as f:
    files = json.load(f)

print("""
A = user + app + cache
B = user + app
C = user only
D = discard all
""")

choice = input("Your choice [A/B/C/D]: ").strip().upper()

rules = {
    "A": lambda p: True,
    "B": lambda p: "AppData\\Local\\Temp" not in p,
    "C": lambda p: p.startswith(os.path.expanduser("~")),
    "D": lambda p: False
}

selected = [f for f in files if rules[choice](f["path"])]

blueprint = {
    "generated_at": datetime.now(UTC).isoformat(),
    "policy": choice,
    "files": selected
}

with open("blueprint_v2.json", "w", encoding="utf-8") as f:
    json.dump(blueprint, f, indent=2)

print("Blueprint written: blueprint_v2.json")
