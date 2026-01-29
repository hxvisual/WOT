import subprocess
import sys

cmd = [
    sys.executable, 
    "-m",
    "PyInstaller",
    "--onefile",
    "--name", "wot",
    "--add-data", "TWEAKS;TWEAKS",
    "--hidden-import", "config",
    "--hidden-import", "version_checker",
    "--icon", "icon.ico",
    "main.py"
]

try:
    subprocess.check_call(cmd) 
except subprocess.CalledProcessError as e:
    print(f"Код ошибки: {e.returncode}")
    sys.exit(1)
