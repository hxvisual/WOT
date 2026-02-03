# wifi.ps1
# Automatically finds the Wi-Fi adapter and silently opens Yandex search for its driver.

$ErrorActionPreference = 'SilentlyContinue'

# ─── Get all network adapters from WMI ────────────────────────────
$AllAdapters = Get-WmiObject -Class Win32_NetworkAdapter 2>$null

if (-not $AllAdapters) { exit 1 }

# ─── Filter: keep only Wi-Fi / wireless adapters ─────────────────
$WifiAdapters = $AllAdapters | Where-Object {
    $_.Name -and
    $_.Name -match 'Wi-Fi|Wireless|WLAN|802\.11|WiFi'
}

# Fallback: check MediaSubType
if (-not $WifiAdapters) {
    $WifiAdapters = $AllAdapters | Where-Object {
        $_.Name -and
        $_.MediaSubType -eq 'wireless'
    }
}

if (-not $WifiAdapters) { exit 1 }

# ─── Get PnP names, filter out virtual, pick connected first ─────
$WifiList = [System.Collections.ArrayList]::new()

foreach ($adapter in $WifiAdapters) {
    $pnpName = $adapter.Name

    if ($adapter.PNPDeviceID) {
        $pnpEntity = Get-WmiObject -Class Win32_PnPEntity -Filter "DeviceID='$($adapter.PNPDeviceID)'" 2>$null
        if ($pnpEntity) { $pnpName = $pnpEntity.Name }
    }

    if ($pnpName -match 'Loopback|Hyper-V|Virtual|vEthernet|Tunnel|PPP') { continue }

    $cfg = Get-WmiObject -Class Win32_NetworkAdapterConfiguration -Filter "Index=$($adapter.DeviceID)" 2>$null
    $connected = ($cfg -and $cfg.IPEnabled -and $cfg.IPAddress -and $cfg.IPAddress[0] -ne '0.0.0.0')

    $WifiList.Add([PSCustomObject]@{
        Name      = $pnpName
        Connected = $connected
    }) | Out-Null
}

if ($WifiList.Count -eq 0) { exit 1 }

# ─── Pick: connected adapter first, otherwise just first in list ──
$selected = $WifiList | Where-Object { $_.Connected } | Select-Object -First 1
if (-not $selected) { $selected = $WifiList[0] }

# ─── Open Yandex silently ─────────────────────────────────────────
$SearchQuery  = "download driver $($selected.Name)"
$EncodedQuery = [System.Net.WebUtility]::UrlEncode($SearchQuery)
$SearchURL    = "https://yandex.ru/search/?text=$EncodedQuery"

Start-Process -FilePath $SearchURL -WindowStyle Hidden