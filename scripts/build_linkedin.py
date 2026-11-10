"""Create the condensed 1200px LinkedIn graphic. Requires Pillow and qrcode."""
from datetime import datetime
from pathlib import Path
import re

from PIL import Image, ImageDraw, ImageFont
import qrcode

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / 'index.html').read_text()
OUT = ROOT / 'UniJudge_TRUST2027_CFP_LinkedIn.png'
S = 2
image = Image.new('RGB', (1200*S, 1200*S), '#ffffff')
draw = ImageDraw.Draw(image)
NAVY = '#293e52'
TEAL = '#376f6c'
MINT = '#a7d2c7'
INK = '#202b39'
MUTED = '#536477'
PANEL = '#f0f4f6'
LINE = '#d5dfe5'
FONT = Path('/usr/share/fonts/truetype/lato')
WEBSITE = 'https://acmtrustunijudge.github.io/'


def font(size, bold=False):
    return ImageFont.truetype(str(FONT / ('Lato-Bold.ttf' if bold else 'Lato-Regular.ttf')), round(size*S))


def text(value, x, y, size, color=INK, bold=False):
    draw.text((x*S,y*S), value, fill=color, font=font(size,bold), anchor='lt')


def wrap(value, x, y, width, size=23, leading=30, color=INK, bold=False):
    f = font(size,bold)
    lines=[]
    current=''
    for word in value.split():
        candidate=(current+' '+word).strip()
        if current and draw.textlength(candidate,font=f)>width*S:
            lines.append(current)
            current=word
        else:
            current=candidate
    if current:
        lines.append(current)
    for line in lines:
        text(line,x,y,size,color,bold)
        y+=leading
    return y


def box(bounds, fill, radius=0):
    draw.rounded_rectangle(tuple(round(v*S) for v in bounds), radius=radius*S, fill=fill)


def line(points, color, width=1):
    draw.line([(round(x*S),round(y*S)) for x,y in points], fill=color, width=round(width*S))


# Recognizable workshop header, softened to navy and sage.
box((0,0,1200,266),NAVY)
box((0,260,1200,266),TEAL)
text('CALL FOR PAPERS  /  ACM TRUST 2027 WORKSHOP',50,37,23,MINT,True)
title='Universal Judges (UniJudge)'
size=61
while draw.textlength(title,font=font(size,True))>935*S:
    size-=1
text(title,50,91,size,'white',True)
text('Reliable Judging Across Languages and Modalities',50,168,30,'white')
text('Washington, DC (hybrid)  /  March 7-9, 2027',50,220,25,'#d8e3eb')
# Scale mark from the flyer.
line([(1075,86),(1075,183)],MINT,3)
line([(1043,183),(1107,183)],MINT,3)
line([(1006,102),(1144,102)],MINT,3)
draw.ellipse((1069*S,74*S,1081*S,86*S),outline=MINT,width=3*S)
for center in [1020,1130]:
    line([(center-22,150),(center,102),(center+22,150)],MINT,3)
    line([(center-26,150),(center+26,150)],MINT,3)
    draw.arc(((center-27)*S,131*S,(center+27)*S,165*S),0,180,fill=MINT,width=3*S)

# Equal-height cards hold only information useful in the feed.
box((40,298,586,1042),PANEL,22)
box((610,298,1160,1042),PANEL,22)
text('Topics of interest',68,331,30,TEAL,True)
topics=[
 ('Multilingual and low-resource judges','Cross-lingual consistency, transfer, code-switching and cultural criteria.'),
 ('Multimodal judges','Image, document, audio, video and interactive outputs; evidence use.'),
 ('Multilingual-multimodal evaluation','Vision-language, document, speech and audio systems across languages.'),
 ('Cross-representation consistency','Translation, modality conversion, formatting, verbosity and ordering.')
]
y=398
for title,body in topics:
    end=wrap(title,68,y,490,24,29,TEAL,True)
    end=wrap(body,68,end+11,490,23,30,MUTED)
    assert end <= y+126,(title,end)
    y+=131
line([(68,936),(558,936)],LINE)
end=wrap('Also: judge auditing, robustness, bias, calibration and multi-judge disagreement.',68,957,490,22,29,MUTED)
assert end<1030,end

# Deadlines come from the website.
text('Key dates',640,331,30,TEAL,True)
rows=re.findall(r"\{when:'([^']+)',\s*what:'([^']+)'",HTML)
labels=['Abstract registration','Paper submission','ARR commitment','Acceptance notification','Workshop']
assert len(rows)==len(labels)
y=399
for label,(when,_) in zip(labels,rows):
    if label=='Workshop':
        date=when.replace('March ','Mar ').replace('\\u2013','-')
    else:
        date=datetime.strptime(when,'%B %d, %Y').strftime('%b %d, %Y').replace(' 0',' ')
    text(label,640,y,21.5,MUTED)
    date_font=font(25,True)
    x=1130-draw.textlength(date,font=date_font)/S
    assert x>640+draw.textlength(label,font=font(21.5))/S+8
    text(date,x,y-2,25,INK,True)
    line([(640,y+35),(1130,y+35)],LINE)
    y+=53
text('Deadlines: 11:59 PM AoE',640,674,20,MUTED)
text('What to submit',640,727,28,TEAL,True)
summary='We welcome long and short papers, with archival and non-archival options. See the website for page limits, formatting, and submission policies.'
end=wrap(summary,640,775,490,23,30,INK)
assert end<=910,end
qr=qrcode.make(WEBSITE,border=2).convert('RGB')
qr=qr.resize((108*S,108*S),Image.Resampling.NEAREST)
image.paste(qr,(1022*S,916*S))
wrap('Scan for the full call and submission links',640,941,350,23,30,NAVY,True)

# A legible URL is useful when the image is shared without its post text.
box((0,1072,1200,1200),NAVY)
text('acmtrustunijudge.github.io',50,1098,35,'white',True)
text('Full call for papers and submission details',50,1152,23,'#d8e3eb')
image=image.resize((1200,1200),Image.Resampling.LANCZOS)
image.save(OUT,optimize=True,dpi=(144,144))
print(f'Created {OUT.name}: 1200 x 1200')
