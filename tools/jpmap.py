import struct,sys,json
R=open('/home/claude/roms/Pocket Monsters - FireRed (Japan) (Rev 1).gba','rb').read()
u=lambda a:struct.unpack_from('<I',R,a-0x08000000)[0]
MG=0x08311F70
M=json.load(open('/home/claude/pret/data/maps/map_groups.json'))
def mapid(name):
    for gi,g in enumerate(M['group_order']):
        if name in M[g]: return gi,M[g].index(name)
def mh(g,n): return u(u(MG+4*g)+4*n)
if __name__=='__main__':
    for name in sys.argv[1:]:
        g,n=mapid(name); h=mh(g,n); ev=u(h+4)
        c=R[ev-0x8000000:ev-0x8000000+4]; ob=u(ev+4)
        print(name,g,n,'header',hex(h),'mapscripts',hex(u(h+8)))
        for k in range(c[0]):
            o=ob+24*k; print('  obj',k,R[o-0x8000000+1],struct.unpack_from('<hh',R,o-0x8000000+4),'script',hex(u(o+16)),'flag',hex(struct.unpack_from('<H',R,o-0x8000000+20)[0]))
        bg=u(ev+16)
        for k in range(c[3]):
            o=bg+12*k; print('  bg',struct.unpack_from('<hh',R,o-0x8000000),hex(u(o+8)))
