import sys; sys.path.insert(0,'/tmp/t2'); from common import *
g=Game('jp','/tmp/t2/now_fresh.ss',rom=sys.argv[1]); g.run(10)
sys.path.insert(0,'/tmp/blog'); from name import set_name; set_name(g); g.run(2)
g.tap('S'); g.run(40)
for i in range(3): g.cmd('tap D 1'); g.run(6)
g.run(10); g.shot('/tmp/blog/s/menupc1.png'); g.close()
