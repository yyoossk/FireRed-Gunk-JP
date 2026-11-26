exec(open('/tmp/rc/base.py').read())
g=new(); setlead(g,150,moves=(94,58,85,53),lv=100,nick='ミュウツー'); T=0x0818C586; tid=415
sb1=g.u32(0x03004FA8); f=0x500+tid; a=sb1+0xEE0+f//8; v=g.u8(a)&~(1<<(f%8)); g.cmd(f'poke {a:08X} {v:02X}')
runscript(g,bytes([0x5C,3])+struct.pack('<HH',tid,0)+struct.pack('<I',T)+b'\x02')
for i in range(60):
    g.run(30)
    if g.in_battle(): break
    g.tap('A')
E=g.R['party']-600
for i,b in enumerate(struct.pack('<I',0x10)): g.cmd(f'poke {E+100+0x50+i:08X} {b:02X}')
k=0
for i in range(400):
    if g.in_battle() and g.u32(g.R['bcf'])==g.R['act']:
        g.run(20); shot(g,f'tr{k}'); k+=1
        if k>4: break
        enemy_hp(g,1); g.tap('A'); g.run(40); g.tap('A'); g.run(40)
    if not g.in_battle(): break
    g.tap('B'); g.run(10)
g.u8(0x02000000); g.close()
