exec(open('/tmp/rc/base.py').read())
P151='/tmp/rc/post151.ss'
g=new(P151,rom=ROM151)
sb=g.sb1(); sb2=g.u32(g.R['sb1']+4); key=g.u16(sb2+0xF20)
print('coins raw', g.u16(sb+0x294)^key)
v=9999^key
for i,b in enumerate(struct.pack('<H',v)): g.cmd(f'poke {sb+0x294+i:08X} {b:02X}')
warp(g,10,15,4,3,wait=200); g.face('U'); g.run(10); g.tap('A')
g.run(40); g.tap('A'); g.run(40); g.cmd('tap D 1'); g.run(10); g.cmd('tap D 1'); g.run(20); shot(g,'pq_0')
g.u8(0x02000000); g.close()
