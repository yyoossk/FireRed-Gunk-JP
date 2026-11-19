def unlz(d,o=0):
    assert d[o]==0x10; n=int.from_bytes(d[o+1:o+4],'little'); i=o+4; out=bytearray()
    while len(out)<n:
        f=d[i]; i+=1
        for b in range(8):
            if len(out)>=n: break
            if f&(0x80>>b):
                x=(d[i]<<8)|d[i+1]; i+=2; L=(x>>12)+3; dist=(x&0xFFF)+1
                for _ in range(L): out.append(out[-dist])
            else: out.append(d[i]); i+=1
    return bytes(out)
def lz(data):
    out=bytearray([0x10])+len(data).to_bytes(3,'little'); i=0; n=len(data)
    while i<n:
        fpos=len(out); out.append(0); f=0
        for b in range(8):
            if i>=n: break
            best=(0,0)
            for dist in range(2, min(i,4096)+1):  # dist>=2 for VRAM safety
                L=0
                while L<18 and i+L<n and data[i+L]==data[i-dist+L]: L+=1
                if L>best[0]: best=(L,dist)
                if L==18: break
            if best[0]>=3:
                L,dist=best; x=((L-3)<<12)|(dist-1); out+=bytes([x>>8,x&0xff]); f|=0x80>>b; i+=L
            else: out.append(data[i]); i+=1
        out[fpos]=f
    while len(out)%4: out.append(0)
    return bytes(out)
