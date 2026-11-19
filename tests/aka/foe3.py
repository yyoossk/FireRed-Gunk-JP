import sys; sys.path.insert(0,'/tmp/t2'); from common import *
g=Game('jp','/tmp/t2/s21_fresh.ss',rom=sys.argv[1]); g.run(10)
T=0x0818C586; tid=415
sb1=g.u32(0x03004FA8); f=0x500+tid; a=sb1+0xEE0+f//8; v=g.u8(a)&~(1<<(f%8)); g.cmd(f'poke {a:08X} {v:02X}')
runscript(g,bytes([0x5C,3])+struct.pack('<HH',tid,0)+struct.pack('<I',T)+b'\x02')
for i in range(60):
    g.run(30)
    if g.in_battle(): break
    g.tap('A')
g.run(600); g.tap('A'); g.run(300); g.shot('/tmp/t2/f3_0.png')
# open bag and come back (screen reload)
g.tap('R'); g.run(10); g.tap('A'); g.run(120); g.shot('/tmp/t2/f3_1.png'); g.tap('B'); g.run(150); g.shot('/tmp/t2/f3_2.png')
# attack with thunderbolt until faint & next mon
for k in range(2):
    g.tap('L'); g.run(8); g.tap('U'); g.run(8); g.tap('A'); g.run(30); g.tap('D'); g.run(8); g.tap('R'); g.run(8); g.tap('A')
    for i in range(16):
        g.run(60); g.shot(f'/tmp/t2/f3_k{k}_{i:02d}.png'); g.tap('B')
g.close()
