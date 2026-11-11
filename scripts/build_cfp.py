"""Build the one-page flyer: pip install reportlab qrcode; python scripts/build_cfp.py."""
import argparse
from datetime import datetime
from html import unescape
from io import BytesIO
from pathlib import Path
import re

import qrcode
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output', type=Path, default=ROOT / 'UniJudge_TRUST2027_CFP.pdf')
parser.add_argument('--theme', choices=['navy', 'slate'], default='navy')
parser.add_argument('--font-dir', type=Path, default=Path('/usr/share/fonts/truetype/lato'))
args = parser.parse_args()
source = (ROOT / 'index.html').read_text()
for name, filename in [('Body', 'Lato-Regular.ttf'), ('Bold', 'Lato-Bold.ttf'), ('Medium', 'Lato-Semibold.ttf')]:
    pdfmetrics.registerFont(TTFont(name, str(args.font_dir / filename)))
pdfmetrics.registerFontFamily('Body', normal='Body', bold='Bold')
HEADER = HexColor('#293e52' if args.theme == 'navy' else '#34464b')
TEAL = HexColor('#376f6c')
MINT = HexColor('#a7d2c7')
INK = HexColor('#202b39')
MUTED = HexColor('#536477')
PANEL = HexColor('#f0f4f6')
LINE = HexColor('#d5dfe5')
WEBSITE = 'https://acmtrustunijudge.github.io/'

def setting(name):
    return re.search(r"var " + name + r"\s*=\s*'([^']+)'", source).group(1)

DIRECT, ARR, EMAIL = (setting(n) for n in ['SUBMIT_URL', 'ARR_COMMIT_URL', 'EMAIL'])
args.output.parent.mkdir(parents=True, exist_ok=True)
c = canvas.Canvas(str(args.output), pagesize=(612, 792), pageCompression=1)
c.setTitle('The First Workshop on Universal Judges: Call for Papers')
c.setAuthor('UniJudge Organizers')
c.setSubject('Reliable Judging Across Languages and Modalities')

def text(value, x, top, width, size=10.2, leading=14, color=INK, font='Body'):
    value = unescape(value)
    for ch in '\u2010\u2011\u2012\u2013\u2014':
        value = value.replace(ch, '-')
    style = ParagraphStyle('p', fontName=font, fontSize=size, leading=leading,
                           textColor=color, linkUnderline=0)
    p = Paragraph(value, style)
    _, height = p.wrap(width, 792)
    p.drawOn(c, x, 792-top-height)
    return top + height

def heading(value, x, top, width):
    return text(value, x, top, width, 12, 15, TEAL, 'Bold') + 8

# Muted version of the original blue header, with its scales illustration.
c.setFillColor(HEADER)
c.rect(0, 646, 612, 146, fill=1, stroke=0)
c.setFillColor(TEAL)
c.rect(0, 642, 612, 4, fill=1, stroke=0)
text('CALL FOR PAPERS  /  THE FIRST WORKSHOP ON UNIVERSAL JUDGES', 40, 26, 532, 9, 12, MINT, 'Bold')
text('Universal Judges (UniJudge)', 40, 52, 435, 29, 34, white, 'Bold')
text('Reliable Judging Across Languages and Modalities', 40, 91, 520, 14.5, 18, white)
text('Co-located with ACM TRUST 2027  /  Washington, DC (hybrid)  /  March 7-9, 2027', 40, 120, 532, 10, 13, HexColor('#d8e3eb'))
c.setStrokeColor(MINT)
c.setLineWidth(1.7)
c.setLineCap(1)
c.setLineJoin(1)
c.circle(531, 747, 3.2, fill=0, stroke=1)
c.line(531, 743, 531, 687)
c.line(514, 687, 548, 687)
c.line(490, 734, 572, 734)
for center in [497, 565]:
    c.line(center, 734, center-12, 708)
    c.line(center, 734, center+12, 708)
    path = c.beginPath()
    path.moveTo(center-15, 708)
    path.lineTo(center+15, 708)
    path.curveTo(center+8, 698, center-8, 698, center-15, 708)
    c.drawPath(path)

# Keep the brief, two-paragraph introduction; detailed policies stay on the website.
y = 173
intro = [
    'AI judges shape model development, safety evaluations and deployment decisions. Their reliability can shift across languages, modalities and representations, even when underlying quality is unchanged.',
    'UniJudge brings together trustworthy AI, evaluation, multilingual NLP, vision, speech and multimodal communities to audit evaluators, compare failure modes and develop shared evaluation protocols.'
]
for paragraph in intro:
    y = text(paragraph, 40, y, 532, 10.3, 14.2) + 7
main_top = y + 12

# Match the social graphic: teal titles with muted descriptions and no bullets.
left = heading('Topics of interest', 40, main_top, 300)
topics = [
    ('Multilingual and low-resource judges', 'Cross-lingual consistency and transfer, underrepresented languages, code-switching, transliteration and culturally dependent criteria.'),
    ('Multimodal judges', 'Image, document, audio, video and interactive outputs; groundedness, hallucination, reasoning and evidence use.'),
    ('Multilingual-multimodal evaluation', 'Vision-language and document systems across languages; multilingual speech and audio.'),
    ('Cross-representation consistency', 'Translation, modality conversion, formatting, verbosity and ordering; counterfactual and perturbation tests.'),
    ('Judge auditing and meta-evaluation', 'Reasoning validity, robustness, bias, calibration and causal faithfulness.'),
    ('Multi-judge systems', 'Judge disagreement, ensembles and aggregation.'),
    ('Benchmarks and protocols', 'Datasets and evaluation protocols for judges in these settings.')
]
for title, detail in topics:
    left = text(title, 40, left, 296, 10.3, 13.5, TEAL, 'Bold') + 4
    left = text(detail, 40, left, 296, 9.8, 13.2, MUTED) + 10
left -= 10

# Read deadlines from the website so the flyer stays in sync.
rows = re.findall(r"\{when:'([^']+)',\s*what:'([^']+)'", source)
labels = ['Abstract registration', 'Paper submission', 'ARR commitment', 'Acceptance notification', 'Workshop']
assert len(rows) == len(labels), 'Check the deadline list against the website.'
dates = []
for label, (when, _) in zip(labels, rows):
    if label == 'Workshop':
        date = when.replace('March ', 'Mar ').replace('\\u2013', '-')
    else:
        date = datetime.strptime(when, '%B %d, %Y').strftime('%b %d, %Y').replace(' 0', ' ')
    dates.append((label, date))

summary = 'We welcome long and short papers, with archival and non-archival options. See the website for page limits, formatting, and submission policies.'

def sidebar():
    right = heading('Important dates', 370, main_top+13, 190)
    for label, date in dates:
        text(label, 370, right, 105, 8.3, 12, MUTED)
        text(date, 474, right, 88, 9.4, 12, INK, 'Bold')
        c.setStrokeColor(LINE)
        c.setLineWidth(.5)
        c.line(370, 792-right-17, 560, 792-right-17)
        right += 23
    right = text('All deadlines: 11:59 PM AoE', 370, right+1, 190, 8, 11, MUTED) + 17
    right = heading('What to submit', 370, right, 190)
    right = text(summary, 370, right, 190, 10, 13.8) + 15
    right = text(f'<link href="{DIRECT}" color="{HEADER.hexval()}"><b>Submit directly via OpenReview</b></link>', 370, right, 190, 9.7, 13) + 7
    right = text(f'<link href="{ARR}" color="{HEADER.hexval()}"><b>Commit an ARR paper</b></link>', 370, right, 190, 9.7, 13) + 15
    qr = qrcode.make(WEBSITE, border=2)
    data = BytesIO()
    qr.save(data, format='PNG')
    c.drawImage(ImageReader(data), 370, 792-right-43, 43, 43, mask='auto')
    text(f'<link href="{WEBSITE}" color="{HEADER.hexval()}">Full call, website and<br/>submission details</link>', 424, right+8, 136, 9, 12.5, MUTED)
    return right + 56

# Measure and then draw a fitted sidebar: no fixed-height gaps after edits.
real_canvas = c
c = canvas.Canvas(BytesIO(), pagesize=(612, 792))
right_bottom = sidebar()
c = real_canvas
c.setFillColor(PANEL)
c.roundRect(358, 792-right_bottom, 214, right_bottom-main_top, 8, fill=1, stroke=0)
sidebar()

# Fit the footer just below the longer column.
y = max(left, right_bottom) + 22
c.setStrokeColor(LINE)
c.setLineWidth(.7)
c.line(40, 792-y, 572, 792-y)
y += 12
organizers = re.search(r'var ORGANIZERS = \[(.*?)\];', source, re.S).group(1)
people = []
for name, affiliation in re.findall(r"name:'([^']+)', aff:'([^']+)'", organizers):
    people.append(name + (f' ({affiliation})' if affiliation != 'Researcher' else ''))
y = text('<b>Organizers</b>  ' + ', '.join(people), 40, y, 532, 9, 12.6) + 9
y = text(f'<b>Contact</b>&nbsp; <link href="mailto:{EMAIL}" color="{TEAL.hexval()}">{EMAIL}</link>&nbsp;&nbsp;&nbsp;&nbsp; <link href="{WEBSITE}" color="{TEAL.hexval()}">Workshop website</link>', 40, y, 532, 9.5, 13)
if y > 760:
    raise RuntimeError(f'Flyer content extends past the bottom margin: {y:.1f}pt')
c.showPage()
c.save()
print(f'Wrote {args.output}; content ends at {y:.1f}pt on a 792pt page.')
