# Проверка прав администратора
If (!([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]"Administrator"))
{
    Start-Process PowerShell.exe -ArgumentList ("-NoProfile -ExecutionPolicy Bypass -File `"{0}`"" -f $PSCommandPath) -Verb RunAs
    Exit
}

$Host.UI.RawUI.WindowTitle = $myInvocation.MyCommand.Definition + " (Administrator)"
$Host.UI.RawUI.BackgroundColor = "Black"
$Host.PrivateData.ProgressBackgroundColor = "Black"
$Host.PrivateData.ProgressForegroundColor = "White"
Clear-Host



$apiUrl = "https://api.github.com/repos/Flowseal/zapret-discord-youtube/releases/latest"
$releaseInfo = Invoke-RestMethod -Uri $apiUrl -UseBasicParsing

# Находим RAR архив в assets
$asset = $releaseInfo.assets | Where-Object { $_.name -like "*.rar" } | Select-Object -First 1

$downloadUrl = $asset.browser_download_url
$fileName = $asset.name
$version = $releaseInfo.tag_name

$tempFile = "$env:TEMP\zapret.rar"
$destinationPath = "C:\zapret"

# Удаление старой версии
if (Test-Path $destinationPath) {
    Remove-Item -Path $destinationPath -Recurse -Force
}

# Удаление старого временного файла
if (Test-Path $tempFile) {
    Remove-Item -Path $tempFile -Force
}

# Скачивание
Write-Host "Installing: Zapret . . ."
$ProgressPreference = 'Continue'
Invoke-WebRequest -Uri $downloadUrl -OutFile $tempFile -UseBasicParsing


$fileSize = (Get-Item $tempFile).Length

# Проверка наличия 7-Zip
$7zipPaths = @(
    "$env:ProgramFiles\7-Zip\7z.exe",
    "${env:ProgramFiles(x86)}\7-Zip\7z.exe",
    "$env:ProgramW6432\7-Zip\7z.exe"
)

$7zipExe = $null
foreach ($path in $7zipPaths) {
    if (Test-Path $path) {
        $7zipExe = $path
        break
    }
}

if (!$7zipExe) {
	$7zipUrl = "https://www.7-zip.org/a/7z2408-x64.exe"
	$7zipInstaller = "$env:TEMP\7zip-installer.exe"
	
	Invoke-WebRequest -Uri $7zipUrl -OutFile $7zipInstaller -UseBasicParsing
	
	# Тихая установка 7-Zip
	Start-Process -FilePath $7zipInstaller -ArgumentList "/S" -Wait
	Remove-Item -Path $7zipInstaller -Force
	
	# Повторная проверка
	Start-Sleep -Seconds 2
	foreach ($path in $7zipPaths) {
		if (Test-Path $path) {
			$7zipExe = $path
			break
		}
	}
}

$tempExtractPath = "$env:TEMP\zapret_extract"
if (Test-Path $tempExtractPath) {
	Remove-Item -Path $tempExtractPath -Recurse -Force
}
New-Item -ItemType Directory -Path $tempExtractPath -Force | Out-Null

# Распаковываем в временную папку
$extractArgs = "x `"$tempFile`" -o`"$tempExtractPath`" -y"
Start-Process -FilePath $7zipExe -ArgumentList $extractArgs -Wait -NoNewWindow

# Проверяем содержимое
$extractedItems = Get-ChildItem -Path $tempExtractPath

if ($extractedItems.Count -eq 1 -and $extractedItems[0].PSIsContainer) {
	# Если внутри одна папка, перемещаем её содержимое
	$innerFolder = $extractedItems[0].FullName
	Move-Item -Path $innerFolder -Destination $destinationPath -Force
} else {
	# Иначе перемещаем всё содержимое
	Move-Item -Path $tempExtractPath -Destination $destinationPath -Force
}

# Очистка временной папки
if (Test-Path $tempExtractPath) {
	Remove-Item -Path $tempExtractPath -Recurse -Force
}
    

# Очистка
Remove-Item -Path $tempFile -Force -ErrorAction SilentlyContinue

# Открытие папки
Start-Process explorer.exe -ArgumentList $destinationPath