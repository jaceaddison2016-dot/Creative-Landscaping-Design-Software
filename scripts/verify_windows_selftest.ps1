# Execute ogp-change-control section 2.8 in PowerShell, without console pipes.
# Reused for the portable and installed binary; the child exit code is mandatory.
param([Parameter(Mandatory = $true)][string]$Executable)
$ErrorActionPreference = 'Stop'
if (-not (Test-Path $Executable)) { throw "Executable missing: $Executable" }
$p = Start-Process -FilePath $Executable -ArgumentList '--selftest' -Wait -PassThru
if ($p.ExitCode -ne 0) { throw "Desktop self-test failed: $($p.ExitCode)" }
Write-Host 'Desktop self-test passed: Qt3D imports, Qt version and Agent API binding'
