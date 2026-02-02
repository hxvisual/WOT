import msvcrt
import os
import sys
import subprocess
from colorama import init, Fore, Back


init(autoreset=True)

PATH = os.path.dirname(os.path.abspath(__file__))

ELEMENT_MENU = 4
ACTIVE = False

ELEMENTS = [
	[Fore.RED + "Разрешить скрипты (при первом запуске!)\n", 	f"{PATH}/PROGRAMS/Allow Scripts.cmd"],
	[Fore.BLUE + "Установить Windows 10", 						f"{PATH}/PROGRAMS/Reinstall 1.ps1"],
	[Fore.BLUE + "Установить Windows 11", 						f"{PATH}/PROGRAMS/Reinstall 2.ps1"],
	[Fore.GREEN + "zapret + 7z\n", 								f"{PATH}/PROGRAMS/zapret.ps1"],
	["1. Google Chrome", 										f"{PATH}/PROGRAMS/Google Chrome.ps1"],
	["2. Discord", 												f"{PATH}/PROGRAMS/Discord.ps1"],
	["3. Telegram", 											f"{PATH}/PROGRAMS/Telegram.ps1"],
	["4. Spotify", 												f"{PATH}/PROGRAMS/Spotify.ps1"],
	["5. Happ", 												f"{PATH}/PROGRAMS/Happ.ps1"],
	["6. VLC", 													f"{PATH}/PROGRAMS/VLC.ps1"],
	["7. qBittorrent", 											f"{PATH}/PROGRAMS/qBittorrent.ps1"],
	["8. StartAllBack (win 11)", 								f"{PATH}/PROGRAMS/StartAllBack.ps1"],
	["9. Revo Uninstaller", 									f"{PATH}/PROGRAMS/Revo Uninstaller.ps1"],
]

def clear_console():
	os.system("cls")

def clear_input_buffer():
	while msvcrt.kbhit():
		msvcrt.getch()

def logo():
	print(Back.GREEN + Fore.BLACK + "⚡ WINDOWS PROGRAMS INSTALLER ⚡")
	print(" "*8 + "by t.me/heksaw")
	print()
	print(" "*2 + Fore.RED + "ДОЛЖНА БЫТЬ АНГЛ. РАСКЛАДКА!")
	print()
	print(" "*9 + Fore.CYAN + "Управление:")
	print(" "*10 + "W - вверх")
	print(" "*10 + "S - вниз")
	print(" "*6 + "Enter - запустить")
	print(" "*9 + "Esc - выход")
	print("-"*30)
	print()

def menu(element):
	global ACTIVE

	logo()

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