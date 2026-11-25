import sys,struct; sys.path.insert(0,'/tmp/t2'); from common import *
g=Game('jp',sys.argv[2],rom=sys.argv[1]); g.run(10)
OE=0x02036D6C; SP=0x020205B8
def s16(v): return struct.unpack('<h',struct.pack('<H',v))[0]
def objs():
    r=[]
    for i in range(16):
        a=OE+0x24*i
        if g.u8(a)&1:
            sid=g.u8(a+4); s=SP+0x44*sid
            r.append((i,s16(g.u16(s+0x20))+s16(g.u16(s+0x24)),s16(g.u16(s+0x22))+s16(g.u16(s+0x26))))
    return r
print(objs())
key=sys.argv[3]
for f in range(60):
    g.cmd(f'hold {key} 1'); o=objs()
    print(f, ' '.join(f'{i}:{x},{y}' for i,x,y in o))
g.close()
