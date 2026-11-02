"""RV32IM ELF execution and independent G2 reference check for M1."""
import json, sys
from pathlib import Path
from elftools.elf.elffile import ELFFile
from unicorn import Uc, UC_ARCH_RISCV, UC_MODE_RISCV32, UC_HOOK_CODE
from unicorn.riscv_const import UC_RISCV_REG_SP, UC_RISCV_REG_RA, UC_RISCV_REG_PC
from capstone import Cs, CS_ARCH_RISCV, CS_MODE_RISCV32

ROOT = Path(__file__).resolve().parents[1]
uc = Uc(UC_ARCH_RISCV, UC_MODE_RISCV32)
uc.mem_map(0x10000, 0x30000)
uc.mem_map(0x100000, 0x10000)
with (ROOT / 'evidence/main_O0.elf').open('rb') as f:
    elf = ELFFile(f)
    for segment in elf.iter_segments():
        if segment['p_type'] == 'PT_LOAD':
            uc.mem_write(segment['p_vaddr'], segment.data())
    symbols = {s.name: s['st_value'] for s in elf.get_section_by_name('.symtab').iter_symbols()}
uc.reg_write(UC_RISCV_REG_SP, 0x110000)
uc.reg_write(UC_RISCV_REG_RA, 0x3fff0)
cs = Cs(CS_ARCH_RISCV, CS_MODE_RISCV32)
trace = []
def hook(machine, address, size, data):
    insn = next(cs.disasm(bytes(machine.mem_read(address, size)), address))
    trace.append({'address': address, 'hex': bytes(insn.bytes).hex(),
                  'mnemonic': insn.mnemonic, 'operands': insn.op_str})
uc.hook_add(UC_HOOK_CODE, hook)
uc.emu_start(symbols['main'], 0x3fff0, count=100000)
assert uc.reg_read(UC_RISCV_REG_PC) == 0x3fff0, 'Program did not return normally'
def read(name, count=1):
    b = bytes(uc.mem_read(symbols[name], 4 * count))
    values = [int.from_bytes(b[i:i+4], 'little', signed=True) for i in range(0,len(b),4)]
    return values if count > 1 else values[0]
x, original = 1230006, []
for _ in range(30):
    x = (1664525 * x + 1013904223) & 0xffffffff
    original.append((x >> 16) % 101)
expected_mean = sum(original) // 30
buckets = [sum(lo <= v <= hi for v in original) for lo,hi in [(0,49),(50,64),(65,74),(75,84),(85,100)]]
expected = {'bucket':buckets, 'mean':expected_mean,
            'below_count':sum(v < expected_mean for v in original),
            'pass_count':sum(v >= 56 for v in original)}
actual = {key:read(key,5 if key=='bucket' else 1) for key in expected}
assert actual == expected, (actual, expected)
assert read('grades',30) == [v | 0x100 if v < expected_mean else v for v in original]
# The first below-average element is used for the selected return-to-caller window.
kernel = None
for i,insn in enumerate(trace):
    for length in range(12,21):
        window = trace[i:i+length]
        if len(window) != length: continue
        mn = {w['mnemonic'] for w in window}
        if ('ret' in mn and 'sw' in mn and 'lw' in mn
            and mn.intersection({'blt','bge','beq','bne','blez','bgtz','bgez','bltz','beqz','bnez'})
            and mn.intersection({'or','ori','addi','add','slli'})):
            # Prefer a window containing the mark operation and return, then caller's array store.
            if 'ori' in mn:
                kernel = window
                break
    if kernel: break
assert kernel, 'No suitable 12-20 instruction kernel found'
result = {'student_number':'5001230006','SID':1230006,'original':original,
          'sum':sum(original),'outputs':actual,
          'addresses':{k:f'0x{symbols[k]:08X}' for k in actual},
          'instruction_count':len(trace),'kernel':kernel,
          'kernel_first':f"0x{kernel[0]['address']:08X}",
          'kernel_last':f"0x{kernel[-1]['address']:08X}",
          'status':'PASS: RV32IM memory equals independent Python reference'}
(ROOT/'evidence/verification.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
(ROOT/'evidence/dynamic_trace.json').write_text(json.dumps(trace,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
