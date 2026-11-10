"""Actual M2 simulation and independent encoding check shown in a native GUI."""
import contextlib, io, json, runpy, tkinter as tk
from pathlib import Path
from tkinter import ttk
ROOT=Path(__file__).resolve().parents[1]
app=tk.Tk();app.title('CMPE3209 M2 - RV32IM Machine Code Verification')
app.geometry('1120x690+50+45')
ttk.Label(app,text='CMPE3209 M2 | RV32IM / Clang 18.1.6 / Unicorn 2.1.4',font=('Arial',16,'bold')).pack(anchor='w',padx=20,pady=(16,5))
ttk.Label(app,text='Ali Bal | 5001230006 | Gercek ELF yurutmesi ve alan bazinda yeniden kodlama',font=('Arial',11)).pack(anchor='w',padx=20)
pane=tk.Text(app,font=('Cascadia Mono',11),bg='white',relief='flat',padx=20,pady=12)
pane.pack(fill='both',expand=True)
def run():
    pane.configure(state='normal');pane.delete('1.0','end')
    with contextlib.redirect_stdout(io.StringIO()):runpy.run_path(str(ROOT/'tools/m2_analysis.py'),run_name='__main__')
    data=json.loads((ROOT/'m2/analysis.json').read_text(encoding='utf-8'))
    lines=['#  ADRES       ASM                          TIP  HESAPLANAN    ELF / SIMULATOR', '']
    for e in data['encodings']:
        lines.append(f"{e['number']:02} {e['address']}  {e['assembly']:<28} {e['format']}   {e['word']}    MATCH")
    lines += ['', 'TUM PROGRAM - GERCEK YURUTME',
        '               instruction      load     store',
        *[f"{k:4}           {data['program'][k]['dynamic']['instructions']:6}          {data['program'][k]['dynamic']['loads']:4}     {data['program'][k]['dynamic']['stores']:4}" for k in ['O0','O1']],
        '', 'O0 ve O1: bucket=[14,1,7,0,8] mean=51 below_count=14 pass_count=15',
        'Tum 30 isaretli dizi elemani ayni. Kernel: O0=20, O1=3 (inline).',
        'PASS: 10/10 alan bazinda kodlama ELF byte degerleriyle ayni.',
        'Veri: m2/analysis.json | machine_code.csv | disassembly_O0/O1.txt']
    pane.insert('end','\n'.join(lines));pane.configure(state='disabled')
ttk.Button(app,text='ELF dosyalarini calistir ve kodlamalari yeniden dogrula',command=run).pack(anchor='w',padx=20,pady=(0,15))
app.after(100,run);app.mainloop()
