exec(open('/tmp/rc/base.py').read())
for tag,args in (('cave',(1,81,17,4)),('route',(3,30,14,20)),('indoor',(5,4,7,6)),('pallet',(3,0,10,10))):
    g=new(); warp(g,*args)
    g.tap('S'); g.run(40)
    n=g.u8(0x02037029); order=list(g.peek(0x0203702A,9)[:n]); downs(g,order.index(10)); g.tap('A'); g.run(30); g.tap('A'); g.run(200)
    shot(g,f'lb_{tag}0')
    for i in range(3): g.cmd('tap L 1'); g.run(20)
    shot(g,f'lb_{tag}1'); g.close()
