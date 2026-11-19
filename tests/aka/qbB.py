import sys; sys.path.insert(0,'/tmp/t2'); from common import *
g=Game('jp','/tmp/t2/now_fresh.ss',rom=sys.argv[1]); g.run(10)
wild(g,19,2)
g.run(200); g.tap('A'); g.run(300); g.shot('/tmp/t2/qb0.png')
g.tap('B'); g.run(30); g.shot('/tmp/t2/qb1.png')
g.tap('B'); g.run(30); g.shot('/tmp/t2/qb2.png')
g.tap('D'); g.run(20); g.tap('B'); g.run(40); g.shot('/tmp/t2/qb3.png')
g.close()
from PIL import Image
W=Image.new('RGB',(960,160))
for i in range(4): W.paste(Image.open(f'/tmp/t2/qb{i}.png').convert('RGB'),(i*240,0))
W.resize((1920,320),Image.NEAREST).save('/tmp/ttl/qb.png')
