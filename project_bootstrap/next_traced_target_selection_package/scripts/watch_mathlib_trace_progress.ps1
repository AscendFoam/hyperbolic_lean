param(
  [string]$LogPath = "artifacts/logs/mathlib_hierarchy_probe_v1/trace_run.log",
  [int]$TailLines = 40
)

if (-not (Test-Path $LogPath)) {
  throw "Log not found: $LogPath"
}

while ($true) {
  Clear-Host
  Write-Host ("[watch] " + (Get-Date -Format "yyyy-MM-dd HH:mm:ss"))
  $item = Get-Item $LogPath
  Write-Host ("[watch] log_size=" + $item.Length + " bytes")
  Write-Host ("[watch] last_write=" + $item.LastWriteTime)
  Write-Host ""
  Get-Content $LogPath -Tail $TailLines
  Start-Sleep -Seconds 15
}
