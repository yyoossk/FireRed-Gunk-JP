import sys; sys.path.insert(0,'/tmp/t2'); from common import *
from PIL import Image
maps=[('SSANNE_1F_CORRIDOR',10,10),('SSANNE_2F_CORRIDOR',10,10),('SSANNE_3F_CORRIDOR',5,3),('SSANNE_B1F_CORRIDOR',5,3),('SSANNE_DECK',10,10),('SSANNE_KITCHEN',5,5),('SSANNE_CAPTAINS_OFFICE',3,5),('SSANNE_1F_ROOM1',3,4),('SSANNE_2F_ROOM1',3,4),('SSANNE_B1F_ROOM1',3,4)]
for name,rom,st in (('o','/home/claude/roms/Pocket Monsters - FireRed (Japan) (Rev 1).gba','/tmp/walkst/s07_viridian_jp.ss'),('p','/home/claude/work/port.gba','/tmp/t2/now_fresh.ss')):
    g=Game('jp',st,rom=rom); g.run(10)
    for i,(m,x,y) in enumerate(maps):
        g.teleport(m,x,y); g.run(90); g.shot(f'/tmp/t2/ss_{name}{i}.png')
    g.close()
W=Image.new('RGB',(480*2+8,160*len(maps)),(255,255,255))
for i in range(len(maps)):
    W.paste(Image.open(f'/tmp/t2/ss_o{i}.png').convert('RGB').resize((480,160)) if False else Image.open(f'/tmp/t2/ss_o{i}.png').convert('RGB'),(0,i*160))
    W.paste(Image.open(f'/tmp/t2/ss_p{i}.png').convert('RGB'),(248,i*160))
W.crop((0,0,488,160*len(maps))).save('/tmp/ttl/ssanne.png')
