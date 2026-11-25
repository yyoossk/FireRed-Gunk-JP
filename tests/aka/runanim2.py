import sys,hashlib; sys.path.insert(0,'/tmp/t2'); from common import *
from PIL import Image
t=sys.argv[3]
g=Game('jp',sys.argv[2],rom=sys.argv[1]); g.run(10)
g.cmd('hold BL 10')
for i in range(36):
    g.cmd('hold BL 1'); g.shot(f'/tmp/t2/rx_{t}_{i}.png')
g.close()
names={}; seq=[]
for i in range(36):
    im=Image.open(f'/tmp/t2/rx_{t}_{i}.png').convert('RGB').crop((112,64,128,88))
    seq.append(names.setdefault(hashlib.md5(im.tobytes()).hexdigest(),chr(65+len(names))))
print(t,''.join(seq))
