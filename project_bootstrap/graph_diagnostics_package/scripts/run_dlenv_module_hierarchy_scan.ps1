param(
  [string]$ConfigPath = "project_bootstrap/graph_diagnostics_package/configs/module_hierarchy_scan_batteries_v1.json",
  [string]$PythonExe = "C:\ProgramData\anaconda3\envs\DLEnv\python.exe"
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$packageRoot = Split-Path -Parent $scriptDir
$projectBootstrapRoot = Split-Path -Parent $packageRoot
$repoRoot = Split-Path -Parent $projectBootstrapRoot

if (-not (Test-Path $PythonExe)) {
  throw "Python executable not found: $PythonExe"
}

$resolvedConfig = Join-Path $repoRoot $ConfigPath
if (-not (Test-Path $resolvedConfig)) {
  throw "Config not found: $resolvedConfig"
}

Push-Location $repoRoot
try {
  & $PythonExe "project_bootstrap/baseline_scaffold/src/scan_module_hierarchy_candidates.py" --config $resolvedConfig
}
finally {
  Pop-Location
}
