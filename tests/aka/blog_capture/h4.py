exec(open('/tmp/rc/base.py').read())
g=new('/tmp/rc/t_arr.ss')
warp(g,42,2,6,7); print(g.pos(), g.objects())
r=g.goto(6,6); g.face('U'); g.run(10)
g.tap('A')
for i in range(12):
    g.run(50); shot(g,f'w{i:02d}')
    g.tap('A') if i<3 else None
g.save('/tmp/rc/t_desk.ss'); g.close()
