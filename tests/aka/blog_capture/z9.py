exec(open('/tmp/rc/base.py').read())
for st,tag,clr in ((POST,'a',False),('/tmp/t2/now_fresh.ss','b',True)):
    g=Game('jp',st,rom=ROM); g.run(10)
    if clr: g.setflag(0x841,False)
    g.tap('S'); g.run(40)
    n=g.u8(0x02037029); order=list(g.peek(0x0203702A,9)[:n]); downs(g,order.index(10)); g.tap('A'); g.run(30); g.tap('A'); g.run(200)
    shot(g,f'fz{tag}'); g.close()
