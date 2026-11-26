exec(open('/tmp/rc/base.py').read())
import walker
g=new(); g.teleport('SEVEN_ISLAND',10,10); g.run(60); g.face('U'); g.tap('A')
for i in range(4): g.run(30); shot(g,f'sa{i}'); g.tap('A')
wait_idle(g)
g.face('R'); g.step('R'); g.face('U'); g.step('U'); g.run(200); print(g.pos(), walker._events(g))
shot(g,'sb0')
g.u8(0x02000000); g.close()
