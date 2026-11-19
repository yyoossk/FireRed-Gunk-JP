import sys; sys.path.insert(0,'/tmp/t2'); from common import *
g=Game('jp','/tmp/walkst/s21_postgame_jp.ss',rom=sys.argv[1]); g.run(10)
g.tap('S'); g.run(20); g.tap('D',5); g.run(10); g.tap('A'); g.run(60); g.tap('A'); g.run(400); g.tap('A'); g.run(900); g.tap('A'); g.run(60)
g.cmd('reset'); g.run(600)
for i in range(16): g.tap('A'); g.run(60)
g.tap('B',4); g.run(300)
g.run(60); g.save(sys.argv[2]); g.shot(sys.argv[2]+'.png')
g.close()
