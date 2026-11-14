"""Produce a submission-only ZIP with full PDF and tagged Git history."""
import hashlib,json,shutil,subprocess,zipfile
from pathlib import Path
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT.parent/'output/CMPE3209_FINAL_SON_TESLIM';OUT.mkdir(parents=True,exist_ok=True)
def git(*args):return subprocess.check_output(['git','-C',str(ROOT),*args],text=True).strip()
def main():
 head=git('rev-parse','HEAD');assert head==git('rev-parse','final^{}')
 assert not git('status','--porcelain'),'Package only a clean, tagged working tree'
 pdf=ROOT/'pdf/Ali_Bal_5001230006_FINAL_TESLIM_TUTANAGI.pdf'
 assert len(PdfReader(pdf).pages)==39
 bundle=OUT/'cmpe3209-proje.bundle'
 subprocess.run(['git','-C',str(ROOT),'bundle','create',str(bundle),'--all'],check=True,capture_output=True)
 subprocess.run(['git','-C',str(ROOT),'bundle','verify',str(bundle)],check=True,capture_output=True)
 files={pdf.name:pdf,'cmpe3209-proje.bundle':bundle}
 names=['main.c','main_v2.c','link.ld','asm_O0.s','asm_O1.s','objdump_O0.txt','objdump_O1.txt','trace.csv','requirements-verify.txt',
 'evidence/main_O0.elf','evidence/main_O1.elf','evidence/verification.json',
 'm2/analysis.json','m2/c_to_assembly.csv','m2/machine_code.csv','m2/machine_code_verification.jpg',
 'tools/build.ps1','tools/build_v2.ps1','tools/final_analysis.py','tools/final_trace.py','tools/cache_sim.py',
 'tools/m2_analysis.py','tools/final_gui.py','tools/final_plots.py','tools/objdump_verify.py']
 files.update({n:ROOT/n for n in names})
 files.update({p.relative_to(ROOT).as_posix():p for p in (ROOT/'final').iterdir() if p.is_file()})
 archive=OUT/'Ali_Bal_5001230006_CMPE3209_FINAL_TESLIM.zip'
 with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for name,path in sorted(files.items()):z.write(path,name)
 with zipfile.ZipFile(archive) as z:
  assert z.testzip() is None and set(z.namelist())==set(files)
  assert len([n for n in z.namelist() if n.endswith('.pdf')])==1
  assert all('mail' not in n.lower() and 'readme' not in n.lower() for n in z.namelist())
  for name,path in files.items():assert z.read(name)==path.read_bytes()
 shutil.copy2(pdf,OUT/pdf.name)
 bundle.unlink() # History remains inside the one submission ZIP.
 print(json.dumps({'archive':str(archive),'files':len(files),'pdf_pages':39,'commit':head,'bytes':archive.stat().st_size,
 'sha256':hashlib.sha256(archive.read_bytes()).hexdigest()},indent=2))
if __name__=='__main__':main()
