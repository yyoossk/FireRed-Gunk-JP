import sys,struct; sys.path.insert(0,'/tmp/t2'); from common import *
g=Game('jp','/tmp/t2/f151.ss',rom=sys.argv[1]); g.run(10)
runscript(g,bytes([0x39,3,5,0xFF])+struct.pack('<HH',17,9)+bytes([0x02])); g.run(300)
g.tap('U'); g.run(30)
for i in range(6):
    g.tap('A'); g.run(60); g.shot(f'/tmp/t2/si{i}.png')
g.close()
from PIL import Image
W=Image.new('RGB',(1440,160))
for i in range(6): W.paste(Image.open(f'/tmp/t2/si{i}.png').convert('RGB'),(i*240,0))
W.save('/tmp/t2/si.png')
