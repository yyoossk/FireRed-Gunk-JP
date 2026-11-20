import sys; sys.path.insert(0,'/tmp/t2'); from common import *
from PIL import Image
g=Game('jp','/tmp/t2/now_fresh.ss',rom=sys.argv[1]); g.run(10)
wild(g,19,2)
g.run(200); g.tap('A'); g.run(300)
g.tap('A'); g.run(40); g.tap('l'); g.run(60); g.shot('/tmp/t2/bh0.png')   # move menu + L
g.tap('r'); g.run(60); g.shot('/tmp/t2/bh1.png')                          # move menu + R
g.tap('B'); g.run(40); g.tap('D'); g.run(20); g.tap('A'); g.run(120); g.tap('l'); g.run(60); g.shot('/tmp/t2/bh2.png')  # party + L
g.tap('B'); g.run(120); g.shot('/tmp/t2/bh3.png')
g.tap('l'); g.run(200); g.shot('/tmp/t2/bh4.png')   # quick ball still works
g.close()
W=Image.new('RGB',(1200,160))
for i in range(5): W.paste(Image.open(f'/tmp/t2/bh{i}.png').convert('RGB'),(i*240,0))
W.save('/tmp/t2/bh.png')
