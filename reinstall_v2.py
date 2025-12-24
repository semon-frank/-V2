import subprocess

apps = [
    "Google.Chrome",
    "Microsoft.VisualStudioCode",
    "Python.Python.3"
]

with open("reinstall.ps1", "w") as f:
    for app in apps:
        f.write(f"winget install {app} -e\n")

print("Generated reinstall.ps1")
