param([string]$ZigPath = '')
$ErrorActionPreference = 'Stop'
$zig = $ZigPath
if (-not $zig) { $zig = Join-Path $PSScriptRoot '../../tmp/cmpe3209-tools/ziglang/zig.exe' }
if (-not (Test-Path -LiteralPath $zig)) {
    $zig = (& python -c "import pathlib,ziglang; print(pathlib.Path(ziglang.__file__).parent / 'zig.exe')").Trim()
}
$env:ZIG_GLOBAL_CACHE_DIR = Join-Path $env:TEMP 'cmpe3209-zig-global'
$env:ZIG_LOCAL_CACHE_DIR = Join-Path $env:TEMP 'cmpe3209-zig-local'
Push-Location (Join-Path $PSScriptRoot '..')
try {
    & $zig cc -target riscv32-freestanding -mcpu=generic_rv32+m -mabi=ilp32 -std=c99 -O0 -g -fno-sanitize=all -ffreestanding -fno-stack-protector -fno-pic -Wall -Wextra -pedantic -nostdlib '-Wl,-T,link.ld' '-Wl,-e,main' main_v2.c -o final/main_v2_O0.elf
    if ($LASTEXITCODE) { throw 'V2 ELF compilation failed' }
} finally { Pop-Location }
