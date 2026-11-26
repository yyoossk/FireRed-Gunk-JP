exec(open('/tmp/rc/base.py').read())
ed=sys.argv[1]; rom=ROM if ed=='n' else ROM151; st=POST if ed=='n' else '/tmp/rc/post151.ss'
g=new(st,rom=rom); setlead(g,6,moves=(53,17,89,126),lv=60,nick='リザードン')
warp(g,10,1,4,6,wait=200); g.goto(4,5); g.face('U'); g.run(10); g.tap('A')
for i in range(3): g.run(40); g.tap('A')
g.run(60); downs(g,3); g.run(10); g.tap('A')          # のしかかり
g.run(80); g.tap('A')                                  # msg どのポケモンに → party
g.run(120); shot(g,f'tc_{ed}p'); g.tap('A')            # リザードン
g.run(80); shot(g,f'tc_{ed}q'); g.tap('A')             # あたらしく
g.run(80); shot(g,f'tc_{ed}r'); g.tap('A')             # しかし 4つ
g.run(80); shot(g,f'tc_{ed}s'); g.cmd('tap U 1'); g.run(10); g.tap('A')   # わすれさせますか はい
g.run(150); shot(g,f'tc_{ed}t'); g.tap('A')            # わざ1
for i in range(10): g.run(60); shot(g,f'tc_{ed}u{i}'); g.tap('A')
g.u8(0x02000000); g.close()
