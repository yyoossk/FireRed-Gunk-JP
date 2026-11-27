import sys, struct, os
sys.path.insert(0,'/tmp/t2'); sys.path.insert(0,'/home/claude/tools')
from common import *
import mkmon
ROM='/home/claude/work/port.gba'; ROM151='/home/claude/work/port151.gba'
VAN='/home/claude/roms/Pocket Monsters - FireRed (Japan).gba'
OUT='/tmp/rc/out'; os.makedirs(OUT, exist_ok=True)
def set_name(g):
    sb2 = g.u32(g.R['sb1'] + 4)
    for i, b in enumerate([0x5B, 0x64, 0x5C, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]):
        g.cmd(f'poke {sb2 + i:08X} {b:02X}')
    tid=g.peek(sb2+10,4); P=g.R['party']
    for k in range(6):
        m=P+100*k
        if g.peek(m+4,4)==tid:
            for i,b in enumerate([0x5B,0x64,0x5C,0xFF,0xFF,0xFF,0xFF]): g.cmd(f'poke {m+20+i:08X} {b:02X}')
def freshen(src, dst, rom=ROM):
    g=Game('jp',src,rom=rom); g.run(10); set_name(g); g.run(2)
    g.tap('S'); g.run(30)
    n=g.u8(0x02037029); order=g.peek(0x0203702A,9)[:n]; idx=list(order).index(4)
    for i in range(idx): g.cmd('tap D 1'); g.run(6)
    g.tap('A'); g.run(60); g.tap('A'); g.run(400); g.tap('A'); g.run(900); g.tap('A'); g.run(60)
    g.cmd('reset'); g.run(600)
    for i in range(16): g.tap('A'); g.run(60)
    g.tap('B',4); g.run(300); g.run(60); g.save(dst); g.shot(dst+'.png'); g.close()
POST='/tmp/rc/post.ss'
def new(st=POST, rom=ROM):
    g=Game('jp', st, rom=rom); g.run(10); g.setflag(0x841, False); return g
def shot(g, name): g.shot(f'{OUT}/{name}.png')
def setlead(g, sp, moves=(53, 17, 89, 126), lv=60, nick='リザードン'):
    P=g.R['party']; own=g.peek(P,100); otid=struct.unpack_from('<I',own,4)[0]
    m=bytearray(mkmon.mon(sp, level=lv, nick=nick, pid=0x5151, otid=otid, moves=moves)); m[20:27]=own[20:27]
    for i,b in enumerate(m): g.cmd(f'poke {P+i:08X} {b:02X}')
def wait_idle(g):
    for i in range(30):
        if g.idle(): return
        g.tap('B'); g.run(20)
def warp(g,gr,n,x,y,wait=300):
    runscript(g,bytes([0x39,gr,n,0xFF])+struct.pack('<HH',x,y)+bytes([0x02])); g.run(wait)
def downs(g,k):
    for i in range(k): g.cmd('tap D 1'); g.run(6)
def additem(g, pocket_off, slot, item, qty):
    sb=g.sb1(); sb2=g.u32(g.R['sb1']+4); key=g.u16(sb2+0xF20)
    for i,b in enumerate(struct.pack('<HH', item, qty ^ key)): g.cmd(f'poke {sb+pocket_off+4*slot+i:08X} {b:02X}')
def menu_to(g, item_id):
    g.tap('S'); g.run(30)
    n=g.u8(0x02037029); order=list(g.peek(0x0203702A,9)[:n]); idx=order.index(item_id)
    cur=g.u8(0x02037028) if False else None
    return order, idx

def givemon(g, sp, lv=5):
    runscript(g,bytes([0x79])+struct.pack('<HBH',sp,lv,0)+bytes(9)+b'\x02'); g.run(30)
def setslot(g, slot, sp, moves, lv=50, nick=None):
    P=g.R['party']; own=g.peek(P,100); otid=struct.unpack_from('<I',own,4)[0]
    m=bytearray(mkmon.mon(sp, level=lv, nick=nick or 'ポケモン', pid=0x5151+slot*7, otid=otid, moves=moves)); m[20:27]=own[20:27]
    for i,b in enumerate(m): g.cmd(f'poke {P+100*slot+i:08X} {b:02X}')

def menu_go(g, item):
    """スタートメニューを ひらいて item の ところへ（カーソルの いちを よんで うごかす）"""
    g.tap('S'); g.run(30)
    n=g.u8(0x02037029); order=list(g.peek(0x0203702A,9)[:n]); want=order.index(item)
    cur=g.u8(0x02037028)
    while cur!=want:
        g.cmd('tap D 1' if want>cur else 'tap U 1'); g.run(6); cur=g.u8(0x02037028)
