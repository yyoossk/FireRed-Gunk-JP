import sys; sys.path.insert(0,'/tmp/t2'); from common import *
g=Game('jp','/tmp/walkst/s21_postgame_jp.ss',rom=sys.argv[1]); g.run(10)
g.shot('/tmp/t2/rl0.png')
g.tap('S'); g.run(20)
# go to レポート: menu order ずかん ポケモン バッグ パソコン 名前 レポート
g.tap('D',5); g.run(10); g.shot('/tmp/t2/rl1.png'); g.tap('A'); g.run(60); g.tap('A'); g.run(400); g.tap('A'); g.run(900); g.tap('A'); g.run(60)
g.cmd('reset'); g.run(600)
for i in range(12): g.tap('A'); g.run(60)
g.run(60); g.shot('/tmp/t2/rl2.png'); g.save('/tmp/t2/s21_fresh.ss')
g.hold('L',20); g.run(30); g.shot('/tmp/t2/rl3.png')
g.close()
