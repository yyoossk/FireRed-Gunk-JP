exec(open('/tmp/rc/base.py').read())
g=new(); additem(g, 0x430, 0, 4, 20); warp(g,3,19,10,10)
wild(g,19,2)
for i in range(100):
    if g.u32(g.R['bcf'])==g.R['act']: break
    g.tap('B'); g.run(10)
g.run(30); g.hold('L', 40); g.run(10); shot(g,'quickball'); g.close()
g=new(); T=0x0818C586; tid=415
sb1=g.u32(0x03004FA8); f=0x500+tid; a=sb1+0xEE0+f//8; v=g.u8(a)&~(1<<(f%8)); g.cmd(f'poke {a:08X} {v:02X}')
runscript(g,bytes([0x5C,3])+struct.pack('<HH',tid,0)+struct.pack('<I',T)+b'\x02')
for i in range(60):
    g.run(30)
    if g.in_battle(): break
    g.tap('A')
for i in range(100):
    if g.u32(g.R['bcf'])==g.R['act']: break
    g.tap('B'); g.run(10)
g.run(30); g.tap('A'); g.run(30); shot(g,'btl1'); g.tap('S'); g.run(20); shot(g,'btl2')
g.tap('S'); g.run(20); enemy_hp(g,19); g.tap('D'); g.run(8); g.tap('R'); g.run(8); g.tap('A')
for i in range(20):
    g.run(20); shot(g,f'fh{i:02d}')
g.close()
