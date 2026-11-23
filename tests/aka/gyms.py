import sys,struct; sys.path.insert(0,'/tmp/t2'); from common import *
from PIL import Image
S=[]
for name,(m,x,y) in {'celadon':(6,11,33),'viridian':(1,36,11),'cinnabar':(8,20,7)}.items():
    g=Game('jp',sys.argv[2],rom=sys.argv[1]); g.run(10)
    runscript(g,bytes([0x39,3,m,0xFF])+struct.pack('<HH',x,y)+bytes([0x02])); g.run(300)
    for i in range(4): g.hold('U',20); g.run(10)
    g.run(200)
    sb1=g.u32(0x03004FA8); print(name,'map',g.u8(sb1+4),g.u8(sb1+5),'pos',g.u16(sb1),g.u16(sb1+2))
    g.shot(f'/tmp/t2/gy_{name}.png'); S.append(name)
    # walk back out
    for i in range(3): g.hold('D',20); g.run(10)
    g.run(200); sb1=g.u32(0x03004FA8); g.shot(f'/tmp/t2/gy_{name}_out.png'); print('  out map',g.u8(sb1+4),g.u8(sb1+5),'pos',g.u16(sb1),g.u16(sb1+2))
    g.close()
