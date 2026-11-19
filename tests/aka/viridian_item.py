# トキワシティの キズぐすり（くすりポケット）を ひろえるか
import sys,struct; sys.path.insert(0,'/tmp/t2'); from common import *
g=Game('jp','/tmp/t2/now_fresh.ss',rom=sys.argv[1]); g.run(10)
g.teleport('VIRIDIAN_CITY',14,5); g.run(80); g.hold('R',40); g.run(30); g.tap('R'); g.run(20)
g.tap('A'); g.run(90); g.tap('A'); g.run(60); g.shot('/tmp/t2/pk1.png'); g.tap('A'); g.run(60)
print('flag 0x1CD (ひろった)',g.getflag(0x1cd))
g.close()
