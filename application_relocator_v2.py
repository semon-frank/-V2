import os
import json
import subprocess

BLUEPRINT = "blueprint_v2.json"

def find_exe(path):
    for root, _, files in os.walk(path):
        for f in files:
            if f.lower().endswith(".exe"):
                return os.path.join(root, f)
    return None

with open(BLUEPRINT, encoding="utf-8") as f:
    bp = json.load(f)

apps = [i for i in bp["items"] if i["category"] == "application"]

for app in apps:
    base = app["path"]
    exe = find_exe(os.path.dirname(base))
    if exe:
        print(f"Executable detected: {exe}")
    else:
        print(f"Reinstall required for: {base}")
