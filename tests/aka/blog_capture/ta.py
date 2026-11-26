exec(open('/tmp/rc/base.py').read())
import walker
ed=sys.argv[1]; rom=ROM if ed=='n' else ROM151; st=POST if ed=='n' else '/tmp/rc/post151.ss'
g=new(st,rom=rom); setlead(g,6,moves=(53,17,89,126),lv=60,nick='リザードン')
warp(g,10,1,4,6,wait=200); print([(o['lid'],o['x'],o['y']) for o in walker._events(g)['objs']])
g.goto(4,5); g.face('U'); g.run(10); g.tap('A')
for i in range(5): g.run(40); shot(g,f'ta_{ed}_a{i}'); g.tap('A') if i<3 else None
for i in range(17): g.cmd('tap D 1'); g.run(6)
g.run(10); shot(g,f'ta_{ed}_list_end')
for i in range(14): g.cmd('tap U 1'); g.run(6)
g.run(10); shot(g,f'ta_{ed}_list3')     # のしかかり
g.tap('A')
for i in range(10): g.run(40); shot(g,f'ta_{ed}_b{i}'); g.tap('A')
P=g.R['party']
for i in range(20): g.run(40); shot(g,f'ta_{ed}_c{i:02d}'); g.tap('A')
g.run(60); shot(g,f'ta_{ed}_d')
g.tap('B'); g.run(60); g.tap('A'); g.run(60); shot(g,f'ta_{ed}_e'); 
g.u8(0x02000000); g.close()
