exec(open('/tmp/rc/base.py').read())
ed=sys.argv[1]; rom=ROM if ed=='n' else ROM151; st=POST if ed=='n' else '/tmp/rc/post151.ss'
def here(g,tag):
    menu_go(g,11); g.tap('A'); g.run(50); shot(g,tag); g.tap('B'); g.run(40); g.tap('B'); g.run(40)
    menu_go(g,0); g.tap('A'); g.run(150)
    for i in range(14): g.cmd('tap D 1'); g.run(4)
    g.run(10); g.tap('A'); g.run(30); shot(g,tag+'d'); g.tap('B'); g.run(30); g.tap('B'); g.run(120); g.tap('B'); g.run(60)
g=new(st,rom=rom); givemon(g,82); givemon(g,42); wait_idle(g)   # レアコイル・ゴルバットを つかまえた ことに
warp(g,1,72,10,10)
here(g,f'bl_{ed}0')
g.setflag(0x4AC,True)
here(g,f'bl_{ed}1')
warp(g,3,0,10,10); here(g,f'bl_{ed}2')
g.u8(0x02000000); g.close()
