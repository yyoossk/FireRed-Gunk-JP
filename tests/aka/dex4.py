import sys; sys.path.insert(0,'/home/claude/tools')
from walker import *
from PIL import Image
g=Game('jp',sys.argv[2],rom=sys.argv[1]); g.run(30)
for k in ['S','A']: g.tap(k); g.run(60)
g.tap('A'); g.run(60)
for i in range(128): g.cmd('tap D 1')
g.run(20)
for r in range(3):
    g.tap('A'); g.run(60); g.tap('A'); g.run(60); g.tap('B'); g.run(60); g.tap('B'); g.run(60)
    g.cmd('tap D 1'); g.run(20)
g.tap('A'); g.run(60); g.tap('A'); g.run(60); g.shot('/tmp/t2/dw0.png')
g.tap('A'); g.run(60); g.shot('/tmp/t2/dw1.png')
g.tap('B'); g.run(60); g.tap('B'); g.run(60); g.tap('B'); g.run(60); g.tap('B'); g.run(120); g.shot('/tmp/t2/dw2.png')
g.close()
W=Image.new('RGB',(720,160))
for i in range(3): W.paste(Image.open(f'/tmp/t2/dw{i}.png').convert('RGB'),(i*240,0))
W.save('/tmp/t2/dw.png')
