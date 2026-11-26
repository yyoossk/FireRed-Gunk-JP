exec(open('/tmp/rc/base.py').read())
ed=sys.argv[1]; rom=ROM if ed=='n' else ROM151; st=POST if ed=='n' else '/tmp/rc/post151.ss'
g=new(st,rom=rom)
g.tap('S'); g.run(30); n=g.u8(0x02037029); order=list(g.peek(0x0203702A,9)[:n])
downs(g,order.index(5)); g.tap('A'); g.run(90); shot(g,f'op_{ed}0')
for i in range(7): g.cmd('tap D 1'); g.run(8)
g.cmd('tap R 1'); g.run(10); shot(g,f'op_{ed}1')
g.tap('B'); g.run(120); print('flag', g.getflag(0x4AB))
g.tap('S'); g.run(30); downs(g,order.index(5)); g.tap('A'); g.run(90); shot(g,f'op_{ed}2'); g.tap('B'); g.run(120)
# no path at nurse
g.teleport('VIRIDIAN_CITY_POKEMON_CENTER_1F', 7, 4); g.run(30); g.face('U'); g.run(10)
g.tap('A'); g.run(60); g.tap('A'); g.run(30); g.cmd('tap D 1'); g.run(10); g.tap('A'); g.run(60); shot(g,f'op_{ed}no'); g.tap('A'); g.run(60)
oid=g.u8(g.R['avatar']+5); print('facing after no', g.u8(g.R['objs']+oid*0x24+0x18)&0xF, g.idle())
g.u8(0x02000000); g.close()
