from PIL import Image, ImageDraw, ImageFont
import glob, os, sys
F='/workspace/cadence-prototype/design/ios-54/frames/mac/review-sheet/'
os.makedirs('sbs',exist_ok=True)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',22)
PAD,GAP,LY,SY=24,24,26,70
def frame_for(n):
    base=n[:2]
    m=glob.glob(F+base+'-*.png'); return m[0] if m else None
for p in sorted(glob.glob('build/*.png')):
    n=os.path.basename(p)[:-4]
    f=frame_for(n)
    if not f: print('no frame',n); continue
    a=Image.open(f).convert('RGB'); b=Image.open(p).convert('RGB')
    s=0.5; a=a.resize((int(a.width*s),int(a.height*s)),Image.LANCZOS); b=b.resize((int(b.width*s),int(b.height*s)),Image.LANCZOS)
    W=PAD*2+a.width+GAP+b.width; H=SY+a.height+PAD
    im=Image.new('RGB',(W,H),(255,255,255)); d=ImageDraw.Draw(im)
    d.text((PAD,LY),'FRAME (cadence-prototype d60c889): '+os.path.basename(f)[:-4],fill=(0,0,0),font=font)
    d.text((PAD+a.width+GAP,LY),'BUILD (cadence #61 011eb14): '+n,fill=(0,0,0),font=font)
    im.paste(a,(PAD,SY)); im.paste(b,(PAD+a.width+GAP,SY)); im.save('sbs/'+n+'.png')
