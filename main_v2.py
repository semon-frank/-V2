import sys
import subprocess

def help():
    print("""
SmartMigrator v2
================
scan        扫描系统
blueprint   生成迁移蓝图
restore     分批恢复（支持 test-clean）
relocate    修复快捷方式 / 应用重定位
reinstall   生成缺失应用重装脚本
transfer    大体量传输（占位）
""")

if len(sys.argv) < 2:
    help()
    sys.exit(0)

cmd = sys.argv[1]

mapping = {
    "scan": "scan_system_v2.py",
    "blueprint": "generate_blueprint_v2.py",
    "restore": "restore_execute_v2.py",
    "relocate": "relocation_v2.py",
    "reinstall": "reinstall_v2.py",
    "transfer": "transfer_v2.py",
}

if cmd not in mapping:
    help()
    sys.exit(1)

subprocess.run([sys.executable, mapping[cmd]] + sys.argv[2:])
