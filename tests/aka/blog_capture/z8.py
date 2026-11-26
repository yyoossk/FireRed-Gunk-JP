exec(open('/tmp/rc/base.py').read())
for st,tag in ((POST,'p'),('/tmp/t2/now_fresh.ss','o')):
    g=new(st)
    g.tap('S'); g.run(40)
    n=g.u8(0x02037029); order=list(g.peek(0x0203702A,9)[:n]); downs(g,order.index(10)); g.tap('A'); g.run(30); g.tap('A'); g.run(200)
    shot(g,f'fx{tag}0'); g.cmd('tap D 1'); g.run(20); g.cmd('tap D 1'); g.run(20); shot(g,f'fx{tag}1')
    g.close()
g=new(); setlead(g,6)
g.tap('S'); g.run(40); g.tap('D'); g.run(10); g.tap('A'); g.run(60); g.tap('A'); g.run(30); shot(g,'fy0')
