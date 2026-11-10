param([ValidateSet('O0','O1','all')][string]$Optimization = 'all', [string]$ZigPath = '')
$ErrorActionPreference = 'Stop'
# Install ziglang 0.13.0 and set this path if it is not on PATH.
$zig = $ZigPath
if (-not $zig) { $zig = Join-Path $PSScriptRoot '../../tmp/cmpe3209-tools/ziglang/zig.exe' }
if (-not (Test-Path -LiteralPath $zig)) {
    $zig = (& python -c "import pathlib,ziglang; print(pathlib.Path(ziglang.__file__).parent / 'zig.exe')").Trim()
}
if (-not (Test-Path -LiteralPath $zig)) { throw 'Zig 0.13.0 not found. Pass -ZigPath or install ziglang==0.13.0.' }
$env:ZIG_GLOBAL_CACHE_DIR = Join-Path $env:TEMP 'cmpe3209-zig-global'
$env:ZIG_LOCAL_CACHE_DIR = Join-Path $env:TEMP 'cmpe3209-zig-local'
Push-Location (Join-Path $PSScriptRoot '..')
try {
    $levels = if ($Optimization -eq 'all') { @('O0','O1') } else { @($Optimization) }
    foreach ($level in $levels) {
        $common = @('cc','-target','riscv32-freestanding','-mcpu=generic_rv32+m','-mabi=ilp32','-std=c99',"-$level",'-g','-fno-sanitize=all','-ffreestanding','-fno-stack-protector','-fno-pic')
        & $zig @common -Wall -Wextra -pedantic -nostdlib '-Wl,-T,link.ld' '-Wl,-e,main' main.c -o "evidence/main_$level.elf"
        if ($LASTEXITCODE) { throw 'ELF compilation failed' }
        & $zig @common -S main.c -o "evidence/asm_$level.s"
        if ($LASTEXITCODE) { throw 'Assembly compilation failed' }
    }
} finally { Pop-Location }
