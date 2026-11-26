exec(open('/tmp/rc/base.py').read())
g=new(); ps=g.u32(0x03004FB0); g.cmd(f'poke {ps:08X} 00')
src=g.peek(ps+4+(15*30+0)*80,80)
for s in range(29):
    a=ps+4+s*80
    for i,b in enumerate(src): g.cmd(f'poke {a+i:08X} {b:02X}')
g.run(5)
givemon(g,16)
for i in range(40):
    g.run(6); shot(g,f'bu{i:02d}')
g.close()
