import struct,sys
def wild(rompath):
    r=open(rompath,'rb').read()
    u32=lambda a: struct.unpack_from('<I',r,a-0x08000000)[0]
    # find gWildMonHeaders via port map symbol else vanilla
    a=0x0838C2F4 if "151" not in rompath else 0x08BDDA1C
    import subprocess
    try:
        l=[x for x in open('/home/claude/port/pb/port.map') if ' gWildMonHeaders' in x]
    except: l=[]
    out=[]
    while r[a-0x08000000]!=0xFF:
        g,n=r[a-0x08000000],r[a-0x08000000+1]
        ptrs=[u32(a+4+4*i) for i in range(4)]
        out.append((g,n,ptrs)); a+=20
    return r,out
def lines(r,hdrs,g,n):
    u32=lambda a: struct.unpack_from('<I',r,a-0x08000000)[0]
    cnts=[12,5,5,10]; secs=[[],[],[],[]]
    for (hg,hn,ptrs) in hdrs:
        if (hg,hn)!=(g,n): continue
        for s,p in enumerate(ptrs):
            if not p: continue
            wm=u32(p+4)
            for i in range(cnts[s]):
                sp=struct.unpack_from('<H',r,wm+4*i+2-0x08000000)[0]
                if sp and sp not in secs[s] and len(secs[s])<16: secs[s].append(sp)
    L=0
    for s in secs:
        if s: L+=1+(len(s)+1)//2
    return min(L,32),secs
if __name__=='__main__':
    for rom in sys.argv[1:]:
        r,h=wild(rom); maps=sorted({(g,n) for g,n,_ in h})
        res=[(lines(r,h,g,n)[0],g,n) for g,n in maps]
        res.sort(reverse=True); print(rom, len(maps), res[:12])
