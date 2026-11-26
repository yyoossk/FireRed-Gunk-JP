import sys,glob
from PIL import Image, ImageDraw
fs=sys.argv[2:]; out=sys.argv[1]
cols=4; rows=(len(fs)+3)//4
W=Image.new('RGB',(960,rows*172),'white'); d=ImageDraw.Draw(W)
for i,p in enumerate(fs):
    im=Image.open(p).convert('RGB').resize((240,160)); x=(i%4)*240; y=(i//4)*172
    W.paste(im,(x,y)); d.text((x+2,y+160),p.split('/')[-1],fill='black')
W.save(out)
