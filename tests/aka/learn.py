import sys; sys.path.insert(0,'/tmp/t2'); from common import *
g=Game('jp','/tmp/walkst/s14_brock_jp.ss',rom=sys.argv[1]); g.run(10)
wild(g,113,100)   # Chansey Lv100
g.run(300); g.tap('A'); g.run(100)
enemy_hp(g,1)
g.tap('A'); g.run(30); g.tap('A'); g.run(10)  # fight -> first move
k=0
for i in range(60):
    g.run(40); g.shot(f'/tmp/t2/ln{k:02d}.png'); k+=1
    g.tap('A')
g.close()
