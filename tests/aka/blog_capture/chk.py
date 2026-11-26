import sys,json
exec(open('/tmp/rc/base.py').read())
sys.path.insert(0,'/tmp/rc'); from wh import wild
ed=sys.argv[1]; k=int(sys.argv[2]); K=int(sys.argv[3])
rom=ROM if ed=='n' else ROM151; st=POST if ed=='n' else '/tmp/rc/post151.ss'
r,h=wild(rom); maps=sorted({(g,n) for g,n,_ in h})[k::K]
for g_,n_ in maps:
    t=f'/tmp/rc/chk/{ed}_{g_:02d}_{n_:02d}'
    g=new(st,rom=rom)
    runscript(g,bytes([0x39,g_,n_,0])+struct.pack('<hh',-1,-1)+b'\x02'); g.run(300)
    for i in range(10): 
        if g.idle(): break
        g.tap('B'); g.run(30)
    for tr in range(4):
        g.tap('S'); g.run(30); n=g.u8(0x02037029); order=list(g.peek(0x0203702A,9)[:n])
        if 11 in order and g.u8(0x02037029): break
        g.tap('B'); g.run(20); g.hold('UDLR'[tr],16); g.run(40)
    if 11 not in order: print('no here',g_,n_,order); g.close(); continue
    for i in range(order.index(11)): g.cmd('tap D 1'); g.run(6)
    g.tap('A'); g.run(40); g.shot(t+'_f0.png'); g.cmd('tap D 1'); g.run(10); g.shot(t+'_fm.png')
    for i in range(20): g.cmd('tap D 1'); g.run(6)
    g.run(10); g.shot(t+'_f1.png'); g.tap('B'); g.run(40)
    # now back in start menu: cursor on here; go up to dex (index 0)
    for i in range(order.index(11)): g.cmd('tap U 1'); g.run(6)
    g.tap('A'); g.run(150)
    for i in range(14): g.cmd('tap D 1'); g.run(4)
    g.run(10); g.tap('A'); g.run(30); g.shot(t+'_d0.png'); g.cmd('tap D 1'); g.run(10); g.shot(t+'_dm.png')
    for i in range(20): g.cmd('tap D 1'); g.run(6)
    g.run(10); g.shot(t+'_d1.png')
    g.u8(0x02000000); g.close()
print('done',ed,k)
