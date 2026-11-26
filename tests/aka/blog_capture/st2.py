exec(open('/tmp/rc/base.py').read())
tag=sys.argv[1]; mv=int(sys.argv[2]); rom=ROM if sys.argv[3]=='n' else ROM151
st='/tmp/rc/early.ss' if sys.argv[3]=='n' else '/tmp/rc/early151.ss'
g=new(st,rom=rom); setlead(g,4,moves=(mv,33,0,0),lv=7,nick='ヒトカゲ')
P=g.R['party']
for i,b in enumerate(struct.pack('<H',999)): g.cmd(f'poke {P+0x56+i:08X} {b:02X}'); g.cmd(f'poke {P+0x58+i:08X} {b:02X}')
wild(g,19,30)
def act():
    for i in range(300):
        if g.in_battle() and g.u32(g.R['bcf'])==g.R['act']: return True
        if not g.in_battle(): return False
        g.tap('B'); g.run(10)
k=0
for turn,slot in ((0,0),(1,0),(2,1),(3,1)):
    if not act(): break
    g.run(20); shot(g,f'm{tag}_{sys.argv[3]}{k}'); k+=1
    g.tap('A'); g.run(20)
    if slot: g.cmd('tap R 1'); g.run(10)
    g.tap('A'); g.run(10)
act(); g.run(20); shot(g,f'm{tag}_{sys.argv[3]}{k}')
g.u8(0x02000000); g.close()
