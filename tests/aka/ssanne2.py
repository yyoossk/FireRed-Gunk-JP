import sys; sys.path.insert(0,'/tmp/t2'); from common import *
from PIL import Image
maps=[m for m in __import__('walker')._MAPS if 'SSANNE' in m and 'ROOM' in m]
for name,rom,st in (('o','/home/claude/roms/Pocket Monsters - FireRed (Japan) (Rev 1).gba','/tmp/walkst/s07_viridian_jp.ss'),('p','/home/claude/work/port.gba','/tmp/t2/now_fresh.ss')):
    g=Game('jp',st,rom=rom); g.run(10)
    for i,m in enumerate(maps):
        g.teleport(m,3,4); g.run(90); g.shot(f'/tmp/t2/sr_{name}{i}.png')
    g.close()
W=Image.new('RGB',(488,160*len(maps)),(255,255,255))
for i in range(len(maps)):
    W.paste(Image.open(f'/tmp/t2/sr_o{i}.png').convert('RGB'),(0,i*160)); W.paste(Image.open(f'/tmp/t2/sr_p{i}.png').convert('RGB'),(248,i*160))
W.save('/tmp/ttl/ssrooms.png'); print(maps)
