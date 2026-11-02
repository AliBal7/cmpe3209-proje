$ErrorActionPreference = 'Stop'
# Install ziglang 0.13.0 and set this path if it is not on PATH.
$zig = Join-Path $PSScriptRoot '../../tmp/cmpe3209-tools/ziglang/zig.exe'
$env:ZIG_GLOBAL_CACHE_DIR = Join-Path $env:TEMP 'cmpe3209-zig-global'
$env:ZIG_LOCAL_CACHE_DIR = Join-Path $env:TEMP 'cmpe3209-zig-local'
Push-Location (Join-Path $PSScriptRoot '..')
try {
    $common = @('cc','-target','riscv32-freestanding','-mcpu=generic_rv32+m','-mabi=ilp32','-std=c99','-O0','-g','-fno-sanitize=all','-ffreestanding','-fno-stack-protector','-fno-pic')
    & $zig @common -Wall -Wextra -pedantic -nostdlib '-Wl,-T,link.ld' '-Wl,-e,main' main.c -o evidence/main_O0.elf
    if ($LASTEXITCODE) { throw 'ELF compilation failed' }
    & $zig @common -S main.c -o evidence/asm_O0.s
    if ($LASTEXITCODE) { throw 'Assembly compilation failed' }
} finally { Pop-Location }
