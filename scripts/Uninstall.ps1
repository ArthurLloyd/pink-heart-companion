[CmdletBinding()]
param([string]$CodexHome)

. (Join-Path $PSScriptRoot 'PetPackage.ps1')

try {
    $target = Get-PetDestination $CodexHome
    if (-not (Test-Path -LiteralPath $target)) {
        Write-Host "Not installed: $target"
        exit 0
    }
    Assert-PlainDirectory (Split-Path $target -Parent)
    Remove-PetFiles $target
    Write-Host "Uninstalled: $target"
    Write-Host 'In Codex, select another pet and refresh the list.'
    exit 0
}
catch {
    [Console]::Error.WriteLine('Uninstall failed: ' + $_.Exception.Message)
    exit 1
}
