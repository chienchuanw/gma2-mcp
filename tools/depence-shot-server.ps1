# depence-shot-server.ps1
# One-launch screenshot bridge for the Depence / grandMA2 onPC machine.
#
# Serves the current interactive desktop as a PNG over HTTP so another machine
# on the show network (e.g. the assistant's Mac at 2.0.0.x) can pull frames for
# closed-loop visual verification:  set values (MCP/telnet) -> render -> GET
# /shot.png -> look -> adjust.
#
# Why this exists: a screenshot taken over SSH/Session-0 is a black frame. The
# capture must run inside YOUR logged-in desktop session, so this is a plain
# in-session HTTP server. It binds to all interfaces (http://+:PORT/) so a
# direct-cable / LAN peer can reach it without Tailscale.
#
# Just launch it (double-click tools\Start-DepenceShot.cmd, or run this file).
# It will:
#   1. self-elevate to Administrator (HttpListener on http://+ needs admin),
#   2. ensure an inbound firewall rule for the port exists,
#   3. start serving GET /shot.png and print the URLs to pull from.
#
# Pull a frame from another machine:
#   curl -s -m 10 http://<this-machine-ip>:8099/shot.png -o shot.png
#
# Limitation: a single still judges STATIC looks only (position, beam, color,
# gobo, iris/frost/prism). Temporal looks (strobe rate, rotation/movement speed)
# need a short frame sequence, not one shot.

param([int]$Port = 8099)

# --- 1. self-elevate ---------------------------------------------------------
$id = [Security.Principal.WindowsIdentity]::GetCurrent()
$isAdmin = (New-Object Security.Principal.WindowsPrincipal($id)).IsInRole(
    [Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "Elevating (HttpListener needs admin)..."
    Start-Process powershell -Verb RunAs -ArgumentList @(
        "-ExecutionPolicy", "Bypass", "-NoExit",
        "-File", "`"$PSCommandPath`"", "-Port", "$Port")
    return
}

# --- 2. ensure firewall rule -------------------------------------------------
$ruleName = "DepenceShot-$Port"
if (-not (Get-NetFirewallRule -DisplayName $ruleName -ErrorAction SilentlyContinue)) {
    New-NetFirewallRule -DisplayName $ruleName -Direction Inbound -Protocol TCP `
        -LocalPort $Port -Action Allow -Profile Any | Out-Null
    Write-Host "Firewall rule added: $ruleName (TCP $Port inbound)"
}

# --- 3. serve ----------------------------------------------------------------
Add-Type -AssemblyName System.Windows.Forms, System.Drawing
$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add("http://+:$Port/")   # all interfaces; firewall gates access
$listener.Start()

$ips = (Get-NetIPAddress -AddressFamily IPv4 |
        Where-Object { $_.IPAddress -ne "127.0.0.1" -and $_.IPAddress -notlike "169.254.*" }
       ).IPAddress
Write-Host ""
Write-Host "Depence screenshot server is running on port $Port  (GET /shot.png)." -ForegroundColor Green
foreach ($ip in $ips) { Write-Host "  pull:  http://${ip}:$Port/shot.png" }
Write-Host "Leave this window open. Press Ctrl+C to stop." -ForegroundColor Yellow
Write-Host ""

function Get-ScreenPng {
    # Whole virtual desktop (all monitors) so the visualizer is always included.
    $vs = [System.Windows.Forms.SystemInformation]::VirtualScreen
    $bmp = New-Object System.Drawing.Bitmap $vs.Width, $vs.Height
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.CopyFromScreen($vs.Location, [System.Drawing.Point]::Empty, $vs.Size)
    $ms = New-Object System.IO.MemoryStream
    $bmp.Save($ms, [System.Drawing.Imaging.ImageFormat]::Png)
    $g.Dispose(); $bmp.Dispose()
    return $ms.ToArray()
}

while ($listener.IsListening) {
    $ctx = $listener.GetContext()
    try {
        if ($ctx.Request.Url.AbsolutePath -eq "/shot.png") {
            $bytes = Get-ScreenPng
            $ctx.Response.ContentType = "image/png"
            $ctx.Response.OutputStream.Write($bytes, 0, $bytes.Length)
        }
        else {
            $msg = [Text.Encoding]::UTF8.GetBytes("ok - GET /shot.png")
            $ctx.Response.ContentType = "text/plain"
            $ctx.Response.OutputStream.Write($msg, 0, $msg.Length)
        }
    }
    catch { Write-Host "err: $_" }
    finally { $ctx.Response.Close() }
}
