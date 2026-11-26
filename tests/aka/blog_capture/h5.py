exec(open('/tmp/rc/base.py').read())
g=new('/tmp/rc/t_arr.ss')
warp(g,42,2,6,7); g.goto(6,6); g.face('U'); g.run(10)
g.tap('A'); g.run(50); g.tap('A'); g.run(50); g.tap('A'); g.run(50)
for i in range(16):
    g.run(40); shot(g,f'x{i:02d}'); g.tap('A')
g.close()
