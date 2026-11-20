import sys,struct; sys.path.insert(0,'/tmp/t2'); from common import *
from PIL import Image
g=Game('jp','/tmp/t2/now_fresh.ss',rom=sys.argv[1]); g.run(10)
sb2=g.u32(0x03004FAC)
for i in range(4): g.cmd(f'poke {sb2+0x28+i:08X} FF')
g.teleport('ROUTE10_POKEMON_CENTER_1F',12,6); g.run(90); g.tap('U'); g.run(20)
g.tap('A'); g.run(40)
shots=[]
for i in range(24):
    g.shot(f'/tmp/t2/ai{i:02d}.png'); g.tap('A'); g.run(45)
print('flag',g.getflag(0x2FA))
g.close()
W=Image.new('RGB',(240*8,160*3))
for i in range(24): W.paste(Image.open(f'/tmp/t2/ai{i:02d}.png').convert('RGB'),((i%8)*240,(i//8)*160))
W.save('/tmp/ttl/aide.png')
