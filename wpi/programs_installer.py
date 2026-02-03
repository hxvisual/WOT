import msvcrt
import os
import sys
import subprocess
from colorama import init, Fore, Back


init(autoreset=True)

PATH = os.path.dirname(os.path.abspath(__file__))

ELEMENT_MENU = 5
ACTIVE = False

ELEMENTS = [
	[Fore.BLUE + "Установить Windows 10", 						f"{PATH}/PROGRAMS/Reinstall 1.ps1"],
	[Fore.BLUE + "Установить Windows 11", 						f"{PATH}/PROGRAMS/Reinstall 2.ps1"],
	[Fore.RED + "Драйвер Ethernet", 							f"{PATH}/PROGRAMS/ethernet.ps1"],
	[Fore.RED + "Драйвер Wi-Fi", 								f"{PATH}/PROGRAMS/wifi.ps1"],
	[Fore.GREEN + "Установить zapret\n", 						f"{PATH}/PROGRAMS/zapret.ps1"],
	["1. Google Chrome", 										f"{PATH}/PROGRAMS/Google Chrome.ps1"],
	["2. Discord", 												f"{PATH}/PROGRAMS/Discord.ps1"],
	["3. Telegram", 											f"{PATH}/PROGRAMS/Telegram.ps1"],
	["4. Spotify", 												f"{PATH}/PROGRAMS/Spotify.ps1"],
	["5. Happ", 												f"{PATH}/PROGRAMS/Happ.ps1"],
	["6. VLC", 													f"{PATH}/PROGRAMS/VLC.ps1"],
	["7. qBittorrent", 											f"{PATH}/PROGRAMS/qBittorrent.ps1"],
	["8. Python", 												f"{PATH}/PROGRAMS/Python.ps1"],
	["9. Git", 													f"{PATH}/PROGRAMS/Git.ps1"],
	["10. VS Code", 											f"{PATH}/PROGRAMS/VSCode.ps1"],
	["11. StartAllBack (win 11)", 								f"{PATH}/PROGRAMS/StartAllBack.ps1"],
	["12. Revo Uninstaller", 									f"{PATH}/PROGRAMS/Revo Uninstaller.ps1"],
]

def clear_console():
	os.system("cls")

def clear_input_buffer():
	while msvcrt.kbhit():
		msvcrt.getch()


def menu(element):
	global ACTIVE

	for i in range(len(ELEMENTS)):
		if i == element and ACTIVE:
			print(Fore.YELLOW + "🗘 " + Fore.RESET + ELEMENTS[i][0])
			continue

		if i == element:
			print(Fore.GREEN + "➜ " + Fore.RESET + ELEMENTS[i][0])
			continue

		print(ELEMENTS[i][0])


def start_script(path):
	global ACTIVE
	ACTIVE = True

	clear_console()
	menu(ELEMENT_MENU)

	if path[-3:] == "ps1":
		process = subprocess.Popen(["powershell", "-File", path], creationflags=subprocess.CREATE_NEW_CONSOLE)
		process.wait()
	else:
		process = subprocess.Popen([path], creationflags=subprocess.CREATE_NO_WINDOW)
		process.wait()

	ACTIVE = False
	clear_input_buffer()

def run():
	global ELEMENT_MENU
	
	while True:
		clear_console()
		menu(ELEMENT_MENU)

		while True:
			if msvcrt.kbhit():
				key = msvcrt.getch()

				if key == b"w" or key == b"W":
					if ELEMENT_MENU > 0:
						ELEMENT_MENU -= 1
				elif key == b"s" or key == b"S":
					if ELEMENT_MENU < len(ELEMENTS) - 1:
						ELEMENT_MENU += 1
				elif key == b"\r":
					start_script(ELEMENTS[ELEMENT_MENU][1])
				elif key == b"\x1b":
					sys.exit(0)
				else:
					continue
				break


run()