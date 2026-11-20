import sys; sys.path.insert(0,'/home/claude/tools')
from walker import *
from PIL import Image
g=Game('jp',sys.argv[2],rom=sys.argv[1]); g.run(30)
n=int(sys.argv[3])
for k in ['S','A']: g.tap(k); g.run(60)
g.tap('A'); g.run(60)
g.tap('R', n-1) if False else None
for i in range(n-1): g.cmd('tap D 1')
g.run(30); g.shot('/tmp/t2/dz0.png')
g.tap('A'); g.run(60); g.tap('A'); g.run(10)
for i in range(1,4): g.shot(f"/tmp/t2/dz{i}.png"); g.run(11)
g.close()
W=Image.new('RGB',(960,160))
for i in range(4): W.paste(Image.open(f'/tmp/t2/dz{i}.png').convert('RGB'),(i*240,0))
W.resize((1920,320),Image.NEAREST).save('/tmp/t2/dz.png')
