exec(open('/tmp/rc/base.py').read())
ST=[('brn',0x10),('psn',0x08),('par',0x40),('slp',0x03),('frz',0x20),('tox',0x80)]
rom=sys.argv[1] if len(sys.argv)>1 else ROM
for k,v in ST:
    g=new('/tmp/rc/early.ss' if rom==ROM else '/tmp/rc/early151.ss',rom=rom)
    runscript(g,bytes([0xB6])+struct.pack('<HBH',19,4,0)+b'\x02'); g.run(5)
    E=g.R['party']-600; P=g.R['party']
    for base in (E,P):
        for i,b in enumerate(struct.pack('<I',v)): g.cmd(f'poke {base+0x50+i:08X} {b:02X}')
    runscript(g,bytes([0xB7,0x02]))
    for i in range(40):
        g.run(30)
        if g.in_battle(): break
    for i in range(100):
        if g.u32(g.R['bcf'])==g.R['act']: break
        g.tap('B'); g.run(10)
    g.run(30); shot(g,f'st_{k}'+('' if rom==ROM else '_s')); g.close()
