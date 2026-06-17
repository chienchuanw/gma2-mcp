# Visualizer screenshot bridge (#75)

A minimal way to let an AI assistant (or any tailnet device) *see* the
visualizer (Depence) running on the grandMA2 onPC Windows machine, for
closed-loop verification of position / beam / color looks.

Why this design: SSH-triggered screenshots on Windows often capture a black
frame (the SSH process runs in non-interactive Session 0, with no access to the
logged-in desktop). So the capture must run **inside the interactive desktop
session**. `tools/depence-shot.ps1` is an in-session HTTP server that screenshots
on demand; `tailscale serve` publishes it to the tailnet without opening any
Windows Firewall port.

## One-time setup (on the Windows / Depence machine)

1. Copy `depence-shot.ps1` to the machine (e.g. the Desktop).
2. Start it in an **elevated** PowerShell (admin is needed to bind the
   HttpListener), while logged in to the desktop:

   ```powershell
   powershell -ExecutionPolicy Bypass -File .\depence-shot.ps1
   ```

   Leave that window open and stay logged in (so it can capture the real screen).
   Verify locally: open `http://localhost:8099/shot.png` in a browser.

3. Publish it to the tailnet via Tailscale (no firewall change needed — the
   listener is loopback-only and tailscaled proxies it):

   ```powershell
   tailscale serve --bg http://localhost:8099
   tailscale serve status
   ```

   `serve status` prints the tailnet URL, e.g.
   `https://<node>.<your-tailnet>.ts.net/`. Only tailnet members can reach it
   (this is Serve, not public Funnel).

   Older Tailscale versions use different `serve` syntax — run
   `tailscale serve --help` if the above errors.

## Pulling a frame (from any tailnet device, e.g. the assistant's host)

```bash
curl -s -m 10 https://<node>.<your-tailnet>.ts.net/shot.png -o /tmp/shot.png
```

Then view/analyse `/tmp/shot.png`. The capture is the full virtual desktop (all
monitors); crop to the Depence window if desired.

## Notes / limitations

- Static looks (position aim, beam shape, color, iris/frost/prism) are judgeable
  from one still. Temporal looks (strobe rate, gobo/prism rotation speed,
  movement paths) need a short sequence of frames, not a single shot.
- To capture only a specific window instead of the whole desktop, replace the
  `VirtualScreen` capture with a window-rectangle capture (by window title).
- This is the #75 capture bridge; pairs with `build_preset_palette` (#79) and the
  profile resolver (#74) for a set → render → look → adjust loop.
