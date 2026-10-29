[CmdletBinding()]
param(
    [string]$CodexHome,
    [string]$PackagePath
)

. (Join-Path $PSScriptRoot 'PetPackage.ps1')

try {
    if ([string]::IsNullOrWhiteSpace($PackagePath)) {
        $PackagePath = Join-Path (Split-Path $PSScriptRoot -Parent) 'release\pink-heart-companion'
    }
    Assert-PetPackage $PackagePath
    $target = Get-PetDestination $CodexHome
    if (Test-Path -LiteralPath $target) {
        Assert-PetPackage $target
        Write-Host "Already installed and verified: $target"
        Show-PetInstructions
        exit 0
    }

    $pets = Split-Path $target -Parent
    [IO.Directory]::CreateDirectory($pets) | Out-Null
    Assert-PlainDirectory $pets
    $stage = Join-Path $pets ('.' + $script:PetId + '-' + [guid]::NewGuid().ToString('N'))
    [IO.Directory]::CreateDirectory($stage) | Out-Null
    try {
        foreach ($name in $script:PetHashes.Keys) {
            Copy-Item -LiteralPath (Join-Path $PackagePath $name) -Destination (Join-Path $stage $name)
        }
        Assert-PetPackage $stage
        # Directory.Move fails if the target appeared meanwhile; it never overwrites.
        [IO.Directory]::Move($stage, $target)
    }
    finally {
        if (Test-Path -LiteralPath $stage) {
            Assert-PlainDirectory $stage
            foreach ($name in $script:PetHashes.Keys) {
                $file = Join-Path $stage $name
                if (Test-Path -LiteralPath $file -PathType Leaf) {
                    Remove-Item -LiteralPath $file -Force
                }
            }
            [IO.Directory]::Delete($stage, $false)
        }
    }
    Write-Host "Installed and verified: $target"
    Show-PetInstructions
    exit 0
}
catch {
    [Console]::Error.WriteLine('Installation failed: ' + $_.Exception.Message)
    exit 1
}
