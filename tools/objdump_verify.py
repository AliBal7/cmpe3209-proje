"""Run GNU RISC-V objdump -d and compare every text word with the exact ELF."""
import argparse,hashlib,json,re,subprocess
from pathlib import Path
from m2_analysis import elf_data
ROOT=Path(__file__).resolve().parents[1]
def main():
 p=argparse.ArgumentParser();p.add_argument('--objdump',required=True);args=p.parse_args()
 exe=Path(args.objdump).resolve();version=subprocess.check_output([str(exe),'--version'],text=True).splitlines()[0]
 checked={}
 for level in ['O0','O1']:
  elf=ROOT/f'evidence/main_{level}.elf'
  raw=subprocess.check_output([str(exe),'-d',str(elf)],cwd=ROOT,text=True)
  # Remove machine-specific absolute workspace prefixes from file heading.
  raw=raw.replace(str(elf),f'evidence/main_{level}.elf')
  (ROOT/f'objdump_{level}.txt').write_text(raw,encoding='utf-8')
  parsed={int(m[0],16):int(m[1],16) for m in re.findall(r'^\s*([0-9a-f]+):\s+([0-9a-f]{8})\s',raw,re.M)}
  expected={r['address']:r['word'] for r in elf_data(elf)['instructions']};assert parsed==expected,(level,len(parsed),len(expected))
  checked[level]={'static_instructions':len(expected),'all_words_match':True,'elf_sha256':hashlib.sha256(elf.read_bytes()).hexdigest()}
 enc=json.loads((ROOT/'m2/analysis.json').read_text(encoding='utf-8'))['encodings']
 parsed={int(m[0],16):int(m[1],16) for m in re.findall(r'^\s*([0-9a-f]+):\s+([0-9a-f]{8})\s',(ROOT/'objdump_O0.txt').read_text(),re.M)}
 for e in enc:assert parsed[int(e['address'],16)]==int(e['word'],16)
 result={'version':version,'command':'riscv-none-elf-objdump -d evidence/main_O0.elf (and O1)',
 'source':'https://github.com/xpack-dev-tools/riscv-none-elf-gcc-xpack/releases/tag/v15.2.0-1',
 'executable_sha256':hashlib.sha256(exe.read_bytes()).hexdigest(),'checked':checked,'ten_encoded_instructions_match':True}
 (ROOT/'final/objdump_provenance.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
