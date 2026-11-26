exec(open('/tmp/rc/base.py').read())
g=new(); warp(g,1,81,17,4)
g.tap('S'); g.run(40)
n=g.u8(0x02037029); order=list(g.peek(0x0203702A,9)[:n]); downs(g,order.index(10)); g.tap('A'); g.run(30); g.tap('A'); g.run(200)
seq='LLLLLLLLLLLLLLUUUU'
for i,k in enumerate(seq): g.cmd(f'tap {k} 1'); g.run(24); shot(g,f'fk{i:02d}')
g.close()
