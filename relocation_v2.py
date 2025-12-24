import os, json
import win32com.client

TARGET = "D:/RESTORED"
shell = win32com.client.Dispatch("WScript.Shell")

def fix_lnk(path):
    lnk = shell.CreateShortcut(path)
    target = lnk.Targetpath
    if os.path.exists(target):
        return

    exe = os.path.basename(target)
    for root, _, files in os.walk(TARGET):
        if exe in files:
            lnk.Targetpath = os.path.join(root, exe)
            lnk.save()
            print(f"Fixed: {path}")
            return

for root, _, files in os.walk(os.path.expanduser("~/Desktop")):
    for f in files:
        if f.endswith(".lnk"):
            fix_lnk(os.path.join(root, f))
