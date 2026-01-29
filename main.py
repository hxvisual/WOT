import msvcrt
import os
import sys
import subprocess
from colorama import init, Fore, Back

from config import VERSION
from version_checker import check_version


init(autoreset=True)

PATH = os.path.dirname(os.path.abspath(__file__))

ELEMENT_MENU = 1
ACTIVE = False
LATEST_VERSION = True

ELEMENTS = [
	[Fore.RED + "Разрешить скрипты (при первом запуске!)\n", 				[f"{PATH}/TWEAKS/Allow Scripts.cmd", f"{PATH}/TWEAKS/ps/UAC.ps1"]],

	["1. Проверить активацию", 												[f"{PATH}/TWEAKS/sc/Activation.url"]],
	["2. Синхронизация", 													[f"{PATH}/TWEAKS/sc/Remember Sync.url"]],
	["3. Информация для входа", 											[f"{PATH}/TWEAKS/sc/Sign In Info.url"]],
	["4. Обновление карт", 													[f"{PATH}/TWEAKS/sc/Map Updates.url"]],
	["5. Автозапуск приложений", 											[f"{PATH}/TWEAKS/sc/Startup Apps.url"]],
	["6. Обновление Windows", 												[f"{PATH}/TWEAKS/sc/Windows Updates.url"]],

	["7. Удаление драйверов видеокарты", 									[f"{PATH}/TWEAKS/ps/Clean Driver.ps1"], True],
	["8. Установка драйвера для видеокарты " + Fore.RED + "AMD", 			[f"{PATH}/TWEAKS/ps/Amd Driver.ps1"], True],
	["9. Настройки для видеокарты " + Fore.RED + "AMD", 					[f"{PATH}/TWEAKS/Amd Settings.txt"]],
	["10. Установка драйвера для видеокарты " + Fore.GREEN + "NVIDIA", 		[f"{PATH}/TWEAKS/ps/Nvidia Driver.ps1"], True],
	["11. Настройки для видеокарты " + Fore.GREEN + "NVIDIA", 				[f"{PATH}/TWEAKS/ps/Nvidia Settings.ps1"], True],

	["12. Direct X", 														[f"{PATH}/TWEAKS/ps/Direct X.ps1"], True],
	["13. VC++", 															[f"{PATH}/TWEAKS/ps/VC++.ps1"], True],
	["14. Отключить изоляцию ядра", 										[f"{PATH}/TWEAKS/sc/Core Isolation.url"]],
	["15. Удалить Edge", 													[f"{PATH}/TWEAKS/ps/Edge.ps1"]],
	["16. Удалить мусор из Windows", 										[f"{PATH}/TWEAKS/ps/Bloatware.ps1"]],
	["17. Настройки реестра", 												[f"{PATH}/TWEAKS/ps/Background Apps.ps1", f"{PATH}/TWEAKS/ps/Gamebar.ps1", f"{PATH}/TWEAKS/ps/Msi Mode.ps1", f"{PATH}/TWEAKS/ps/Start Menu Taskbar Clean.ps1", f"{PATH}/TWEAKS/ps/Copilot.ps1", f"{PATH}/TWEAKS/ps/Widgets.ps1", f"{PATH}/TWEAKS/ps/Power Plan.ps1", f"{PATH}/TWEAKS/ps/Timer Resolution.ps", f"{PATH}/TWEAKS/ps/Signout Lockscreen.ps1", f"{PATH}/TWEAKS/ps/Mpo.ps1", f"{PATH}/TWEAKS/ps/Fso.ps1", f"{PATH}/TWEAKS/ps/Registry.ps1"]],
	["18. Отключить точку восстановления", 									[f"{PATH}/TWEAKS/sc/Restore Point.lnk"]],
	["19. " + Fore.GREEN + "NVIDIA HDCP", 									[f"{PATH}/TWEAKS/ps/Hdcp.ps1"]],
	["20. " + Fore.GREEN + "NVIDIA P0 State", 								[f"{PATH}/TWEAKS/ps/P0 State Nvidia.ps1"]],
	["21. " + Fore.RED + "AMD ULPS", 										[f"{PATH}/TWEAKS/ps/ULPS AMD.ps1"]],
	["22. Отключить защиту Windows (Шаг 1)", 								[f"{PATH}/TWEAKS/ps/Security 1.ps1"]],
	["23. Отключить защиту Windows (Шаг 2 В безопасном режиме)", 			[f"{PATH}/TWEAKS/ps/Security 2.ps1"]],
	["24. Очистить диск", 													[f"{PATH}/TWEAKS/ps/Cleanup.ps1"]],
]

def clear_console():
	os.system("cls")

def clear_input_buffer():
	while msvcrt.kbhit():
		msvcrt.getch()

def logo():
	status = ""

	if LATEST_VERSION:
		status = Fore.GREEN + "LATEST"
	elif LATEST_VERSION == None:
		status = Fore.YELLOW + "ERROR!"
	else:
		status = Fore.RED + "UPDATE"

	print(Back.GREEN + Fore.BLACK + "⚡ WINDOWS OPTIMIZATION TOOL ⚡")
	print(" "*7 + "by t.me/heksaw")
	print(" "*7 + f"{VERSION} · {status}")
	print()
	print(" "*9 + Fore.CYAN + "Управление:")
	print(" "*10 + "W - вверх")
	print(" "*10 + "S - вниз")
	print(" "*6 + "Enter - запустить")
	print(" "*9 + "Esc - выход")
	print("-"*29)
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


def start_script(path, show_console=False):
	global ACTIVE
	ACTIVE = True

	clear_console()
	menu(ELEMENT_MENU)

	show_console = subprocess.CREATE_NEW_CONSOLE if show_console else subprocess.CREATE_NO_WINDOW

	for p in path:
		if p[-3:] == "ps1":
			process = subprocess.Popen(["powershell", "-File", p], creationflags=show_console)
			process.wait()
		elif p[-3:] == "cmd":
			process = subprocess.Popen([p],creationflags=show_console)
			process.wait()
		else:
			os.startfile(p)

	ACTIVE = False
	clear_input_buffer()

def run():
	global LATEST_VERSION
	global ELEMENT_MENU

	if check_version():
		LATEST_VERSION = False
	elif check_version() == None:
		LATEST_VERSION = None
	
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
					try:
						start_script(ELEMENTS[ELEMENT_MENU][1], ELEMENTS[ELEMENT_MENU][2])
					except IndexError:
						start_script(ELEMENTS[ELEMENT_MENU][1])
				elif key == b"\x1b":
					sys.exit(0)
				else:
					continue
				break


run()