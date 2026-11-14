"""Validate the delivered ZIP independently from the working checkout."""
import argparse,hashlib,json,os,subprocess,sys,tempfile,zipfile
from pathlib import Path
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[1]
def main():
 p=argparse.ArgumentParser();p.add_argument('zip');args=p.parse_args();archive=Path(args.zip).resolve()
 tmp=ROOT.parent/'tmp';tmp.mkdir(exist_ok=True)
 check=Path(tempfile.mkdtemp(prefix='final-delivery-',dir=tmp)).resolve()
 assert check.is_relative_to(tmp.resolve())
 with zipfile.ZipFile(archive) as z:
  assert z.testzip() is None
  assert all((check/n).resolve().is_relative_to(check) for n in z.namelist())
  z.extractall(check)
  assert len([n for n in z.namelist() if n.endswith('.pdf')])==1
 expected=json.loads((check/'final/analysis.json').read_text(encoding='utf-8'))
 env=os.environ.copy();deps=ROOT.parent/'tmp/cmpe3209-tools'
 if deps.exists():env['PYTHONPATH']=str(deps)+os.pathsep+env.get('PYTHONPATH','')
 subprocess.run([sys.executable,'tools/final_analysis.py'],cwd=check,env=env,check=True,stdout=subprocess.DEVNULL)
 actual=json.loads((check/'final/analysis.json').read_text(encoding='utf-8'));assert actual==expected
 clone=check/'history-check'
 subprocess.run(['git','clone','--quiet',str(check/'cmpe3209-proje.bundle'),str(clone)],check=True,capture_output=True)
 def git(*a):return subprocess.check_output(['git','-C',str(clone),*a],text=True).strip()
 tags={tag:git('rev-parse',tag+'^{}') for tag in ['M1','M2','final']}
 assert git('rev-parse','HEAD')==tags['final']
 assert (clone/'main.c').read_bytes()==(check/'main.c').read_bytes()
 assert (clone/'pdf/Ali_Bal_5001230006_FINAL_TESLIM_TUTANAGI.pdf').read_bytes()==(check/'Ali_Bal_5001230006_FINAL_TESLIM_TUTANAGI.pdf').read_bytes()
 pages=len(PdfReader(check/'Ali_Bal_5001230006_FINAL_TESLIM_TUTANAGI.pdf').pages);assert pages==39
 print(json.dumps({'zip_crc':'PASS','standalone_analysis_exact_match':True,'cache_and_output_invariants':actual['all_cache_outputs_invariant'],
 'tags':tags,'pages':pages,'zip_sha256':hashlib.sha256(archive.read_bytes()).hexdigest()},indent=2))
if __name__=='__main__':main()
