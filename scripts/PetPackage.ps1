# Shared by the offline installer and uninstaller. Windows PowerShell 5.1+.
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$script:PetId = 'pink-heart-companion'
$script:PetHashes = [ordered]@{
    'pet.json' = '2848aee07ffc57fe97bc01baabe277962d83d37d97eb1dcf1a1462954902a460'
    'spritesheet.webp' = 'cba7fc11fed373503042a8460c667dfe471f0d8e4a78f7deca05f0175541d6a3'
}

function Get-PetDestination([string]$CodexHome) {
    if ([string]::IsNullOrWhiteSpace($CodexHome)) {
        $CodexHome = $env:CODEX_HOME
    }
    if ([string]::IsNullOrWhiteSpace($CodexHome)) {
        if ([string]::IsNullOrWhiteSpace($env:USERPROFILE)) {
            throw 'USERPROFILE is unavailable. Supply -CodexHome explicitly.'
        }
        $CodexHome = Join-Path $env:USERPROFILE '.codex'
    }
    if ($CodexHome -notmatch '^(?:[A-Za-z]:[\\/]|\\\\[^\\/]+[\\/][^\\/]+(?:[\\/]|$))') {
        throw 'CodexHome / CODEX_HOME must be an absolute filesystem path.'
    }
    $resolvedHome = [IO.Path]::GetFullPath($CodexHome)
    return Join-Path (Join-Path $resolvedHome 'pets') $script:PetId
}

function Assert-PlainDirectory([string]$Path) {
    $item = Get-Item -LiteralPath $Path -Force
    if (-not $item.PSIsContainer -or ($item.Attributes -band [IO.FileAttributes]::ReparsePoint)) {
        throw "Expected a regular directory (no symlink or junction): $Path"
    }
}

function Assert-PetPackage([string]$Path) {
    Assert-PlainDirectory $Path
    $entries = @(Get-ChildItem -LiteralPath $Path -Force)
    if ($entries.Count -ne 2) {
        throw "Expected exactly pet.json and spritesheet.webp; refusing to change: $Path"
    }
    foreach ($name in $script:PetHashes.Keys) {
        $file = Join-Path $Path $name
        $item = Get-Item -LiteralPath $file -Force
        if ($item.PSIsContainer -or ($item.Attributes -band [IO.FileAttributes]::ReparsePoint)) {
            throw "Expected a regular payload file: $file"
        }
        $stream = [IO.File]::OpenRead($file)
        $hasher = [Security.Cryptography.SHA256]::Create()
        try {
            $hash = [BitConverter]::ToString($hasher.ComputeHash($stream)).Replace('-', '')
        }
        finally {
            $stream.Dispose()
            $hasher.Dispose()
        }
        if ($hash -ne $script:PetHashes[$name]) {
            throw "File differs from the approved pet. Refusing to change: $file"
        }
    }
}

function Remove-PetFiles([string]$Path) {
    # No recursive deletion: validate the exact two-file directory first.
    Assert-PetPackage $Path
    foreach ($name in $script:PetHashes.Keys) {
        Remove-Item -LiteralPath (Join-Path $Path $name) -Force
    }
    [IO.Directory]::Delete($Path, $false)
}

function Show-PetInstructions {
    Write-Host 'In Codex: Settings > Pets (or Mini & Pets) > Refresh > Pink Heart Companion.'
    Write-Host 'If it is hidden, use Show pet or /pet. Restart Codex if Refresh is unavailable.'
}
