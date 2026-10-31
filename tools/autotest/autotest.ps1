param([string]$Plan, [int]$Timeout = 60, [string]$Log = "$env:TEMP\dave_autotest.txt")
# Runs the IDE/Igor-built game with a scripted autotest plan. Never keeps keyboard focus:
# the previous foreground window is restored and the game window is moved off-screen.
$env:LIB = ""
Add-Type @"
using System; using System.Runtime.InteropServices;
public class W32b {
  [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  [DllImport("user32.dll")] public static extern bool SetWindowPos(IntPtr h, IntPtr after, int x, int y, int cx, int cy, uint flags);
}
"@
$dir = "$env:LOCALAPPDATA\GameMakerStudio2-LTS2026\GMS2TEMP\Dave's_&_Enemies_4E250F5_VM"
Copy-Item $Plan "$dir\autotest.json" -Force
$prev = [W32b]::GetForegroundWindow()
$r = "C:\ProgramData\GameMakerStudio2-LTS2026\Cache\runtimes\runtime-2026.0.0.23\windows\x64\Runner.exe"
$p = Start-Process -FilePath $r -ArgumentList "-game", "`"$dir\Dave's & Enemies.win`"" -PassThru -WorkingDirectory $dir -RedirectStandardOutput $Log
for ($i = 0; $i -lt 50; $i++) {
  Start-Sleep -Milliseconds 100
  $p.Refresh()
  if ($p.MainWindowHandle -ne [IntPtr]::Zero) { break }
}
# SWP_NOSIZE | SWP_NOZORDER | SWP_NOACTIVATE
[W32b]::SetWindowPos($p.MainWindowHandle, [IntPtr]::Zero, -3200, 40, 0, 0, 0x0001 -bor 0x0004 -bor 0x0010) | Out-Null
[W32b]::SetForegroundWindow($prev) | Out-Null
if (!$p.WaitForExit($Timeout * 1000)) { Stop-Process -Id $p.Id -Force; "TIMEOUT after $Timeout s" }
Remove-Item "$dir\autotest.json" -Force -ErrorAction SilentlyContinue
Get-Content $Log | Select-String -Pattern "AUTOTEST|ERROR|rror|FATAL|exception|DATA LOAD" | ForEach-Object { $_.Line }
