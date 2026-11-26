exec(open('/tmp/rc/base.py').read())
P151='/tmp/rc/post151.ss'
g=new(P151,rom=ROM151)
sb=g.sb1(); sb2=g.u32(g.R['sb1']+4); key=g.u16(sb2+0xF20)
print('coins raw', g.u16(sb+0x294)^key)
v=9999^key
for i,b in enumerate(struct.pack('<H',v)): g.cmd(f'poke {sb+0x294+i:08X} {b:02X}')
warp(g,10,15,4,3,wait=200); g.face('U'); g.run(10); g.tap('A')
for i in range(3): g.run(40); shot(g,f'kpc{i}'); g.tap('A') if i<1 else None
g.u8(0x02000000); g.close()
# dex area Bellsprout
g=new(P151,rom=ROM151); givemon(g,69); wait_idle(g)
g.tap('S'); g.run(60); g.tap('A'); g.run(60); g.tap('A'); g.run(60)
for i in range(68): g.cmd('tap D 1')
g.run(40); g.tap('A'); g.run(80); shot(g,'kdy0'); g.tap('A')
for i in range(4): g.run(13); shot(g,f'kdy{i+1}')
g.u8(0x02000000); g.close()
