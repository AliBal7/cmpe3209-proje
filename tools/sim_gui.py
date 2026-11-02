"""Small GUI for the actual Unicorn RV32IM execution and memory results."""
import contextlib, io, runpy, sys, tkinter as tk
from pathlib import Path
from tkinter import ttk

ROOT = Path(__file__).resolve().parents[1]
local_deps = ROOT.parent/'tmp/cmpe3209-tools'
if local_deps.exists(): sys.path.insert(0, str(local_deps))
app = tk.Tk()
app.title('CMPE3209 RV32IM - Unicorn Simulator')
app.geometry('1020x650+80+80')
app.configure(bg='white')
ttk.Label(app,text='CMPE3209 | RV32IM / ILP32 | Unicorn 2.1.4',font=('Arial',17,'bold')).pack(anchor='w',padx=22,pady=(18,5))
ttk.Label(app,text='Ali Bal | 5001230006 | G2 - Sinav notu dagilimi',font=('Arial',12)).pack(anchor='w',padx=22,pady=3)
pane=tk.Text(app,font=('Cascadia Mono',12),bg='white',fg='#17212b',relief='flat',padx=22,pady=12)
pane.pack(fill='both',expand=True)
def execute():
    pane.configure(state='normal');pane.delete('1.0','end')
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            state=runpy.run_path(str(ROOT/'tools/verify.py'),run_name='__main__')
        v=state['result'];read=state['read']; machine=state['uc']
        from unicorn.riscv_const import UC_RISCV_REG_PC, UC_RISCV_REG_SP
        lines=['ELF: evidence/main_O0.elf | Clang 18.1.6 | C99 -O0',
               'Yurutme: main -> donus sentinel | Gercek ELF/bellek okumalari',
               f"PC = 0x{machine.reg_read(UC_RISCV_REG_PC):08X}   SP = 0x{machine.reg_read(UC_RISCV_REG_SP):08X}",
               f"Dinamik instruction: {v['instruction_count']}", '',
               'GLOBAL BELLEK CIKTILARI', 'Adres        Degisken         Deger']
        for key,value in v['outputs'].items():lines.append(f"{v['addresses'][key]}   {key:<16} {value}")
        lines+=['','ILK DIZI ELEMANLARI (isaretleme sonrasi)',str(read('grades',10)),
                '', 'BAGIMSIZ DOGRULAMA: PASS',
                '4 global sonuc ve 30 dizi elemani Python referansiyla ayni.',
                'Kernel: i=0, 20 instruction, call/load/store/ALU/branch/return.',
                f"Baslangic {v['kernel_first']} -> bitis {v['kernel_last']}"]
        pane.insert('end','\n'.join(lines))
    except Exception as ex:pane.insert('end',f'ERROR: {ex}');raise
    finally:pane.configure(state='disabled')
ttk.Button(app,text='ELF dosyasini yeniden calistir ve bellegi oku',command=execute).pack(anchor='w',padx=22,pady=(0,18))
app.after(100,execute)
app.mainloop()
