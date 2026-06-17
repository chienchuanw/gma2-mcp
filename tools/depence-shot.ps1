# depence-shot.ps1
# In-session screenshot HTTP server for the visualizer (Depence) machine.
#
# Runs IN your interactive Windows desktop session (so it captures the real
# screen, avoiding the SSH "Session 0" black-frame problem). Each GET /shot.png
# captures the current virtual desktop (all monitors) and returns a PNG.
#
# Pair with `tailscale serve` so nothing is exposed to the LAN and no Windows
# Firewall rule is needed (the listener binds to loopback; tailscaled proxies it
# onto the tailnet). See tools/README-screenshot-bridge.md.
#
# Usage (run an ELEVATED PowerShell — admin is needed to bind the HttpListener):
#   powershell -ExecutionPolicy Bypass -File .\depence-shot.ps1
#   # then, once, on the same machine:
#   tailscale serve --bg http://localhost:8099
#   tailscale serve status   # prints the https://<node>.<tailnet>.ts.net URL

Add-Type -AssemblyName System.Windows.Forms, System.Drawing

$port = 8099
$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add("http://localhost:$port/")   # loopback only; tailscale serve exposes it
$listener.Start()
Write-Host "Screenshot server on http://localhost:$port  (GET /shot.png). Ctrl+C to stop."

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
    $ctx.Response.Close()
}
