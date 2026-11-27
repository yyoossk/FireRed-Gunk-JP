exec(open('/tmp/rc/base.py').read())
def idx(g,item):
    n=g.u8(0x02037029); order=list(g.peek(0x0203702A,9)[:n]); return order.index(item)
for tag,args,unseen in (('r12',(3,30,14,20),False),('cave',(1,72,10,10),False),('caveu',(1,72,10,10),True)):
    g=new(); givemon(g,82); givemon(g,42); wait_idle(g)
    if unseen: g.setflag(0x4AC,True)
    warp(g,*args)
    menu_go(g,11); g.tap('A'); g.run(60); shot(g,f'hf_{tag}'); g.tap('B'); g.run(40); g.tap('B'); g.run(40)
    menu_go(g,0); g.tap('A'); g.run(150)
    for i in range(14): g.cmd('tap D 1'); g.run(4)
    g.run(10); g.tap('A'); g.run(30); shot(g,f'hd_{tag}'); g.u8(0x02000000); g.close()
