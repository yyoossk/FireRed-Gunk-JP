import sys; sys.path.insert(0,'/tmp/t2'); from common import *
g=Game('jp','/tmp/t2/cur_fresh.ss',rom=sys.argv[1]); g.run(10)
wild(g,int(sys.argv[2]),int(sys.argv[3]))
g.run(500); g.tap('A'); g.run(400)
g.shot('/tmp/t2/f2_0.png')
g.tap('A'); g.run(30); g.tap('D'); g.run(8); g.tap('R'); g.run(8); g.shot('/tmp/t2/f2_1.png'); g.tap('A')
g.run(270)
for i in range(24):
    g.run(5); g.shot(f'/tmp/t2/f2_a{i:02d}.png')
g.close()
