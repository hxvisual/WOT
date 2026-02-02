import subprocess
import sys

cmd = [
    sys.executable, 
    "-m",
    "PyInstaller",
    "--onefile",
    "--name", "wpi",
    "--add-data", "PROGRAMS;PROGRAMS",
    "--icon", "icon.ico",
    "programs_installer.py"
]

try:
    subprocess.check_call(cmd) 
except subprocess.CalledProcessError as e:
    print(f"Код ошибки: {e.returncode}")
    sys.exit(1)
