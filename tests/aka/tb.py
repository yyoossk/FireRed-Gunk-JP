import sys; sys.path.insert(0,'/tmp/t2'); from common import *
mode=sys.argv[2]
g=Game('jp','/tmp/walkst/s21_postgame_jp.ss',rom=sys.argv[1]); g.run(10)
T=0x0818C586
if mode=='double':
    tid=484; g.cmd('')
    g.setflag(0)  # noop
    data=bytes([0x5C,4])+struct.pack('<HH',tid,0)+struct.pack('<III',T,T,T)+b'\x02'
else:
    tid=104
    data=bytes([0x5C,3])+struct.pack('<HH',tid,0)+struct.pack('<I',T)+b'\x02'
# clear trainer flag
f=0x500+tid
sb1=g.u32(0x03004FA8)
# flags at sb1+0xEE0
a=sb1+0xEE0+f//8; v=g.u8(a)&~(1<<(f%8)); g.cmd(f'poke {a:08X} {v:02X}')
runscript(g,data)
for i in range(60):
    g.run(30)
    if g.in_battle(): break
    g.tap('A')
for i in range(25):
    g.run(30); g.tap('B')
g.shot(f'/tmp/t2/tb_{mode}0.png')
g.tap('A'); g.run(40); g.shot(f'/tmp/t2/tb_{mode}1.png')
g.tap('S'); g.run(20); g.shot(f'/tmp/t2/tb_{mode}2.png')
g.tap('S'); g.run(20); g.shot(f'/tmp/t2/tb_{mode}3.png')
g.close()
