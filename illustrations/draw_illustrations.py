"""Draw The Support Machine's ten monochrome architectural illustrations."""
from html import escape
from pathlib import Path
import json
import math
import random

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT.parent / 'docs' / 'illustrations'
W, H = 1200, 820
MANIFEST = json.loads((ROOT / 'briefs.json').read_text())
FIGURES = []


class Sketch:
    def __init__(self, number, question, takeaway):
        self.meta = next(f.copy() for f in MANIFEST['figures'] if f['number'] == number)
        FIGURES.append(self.meta)
        self.rng = random.Random(6700 + number)
        self.parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
                      f'<title id="title">{escape(self.meta["title"])}</title>',
                      f'<desc id="desc">{escape(self.meta["caption"])}</desc>',
                      '<defs><pattern id="hatch" patternUnits="userSpaceOnUse" width="8" height="8" patternTransform="rotate(28)"><path d="M 0 0 L 0 8" stroke="#000" stroke-width=".9"/></pattern></defs>',
                      '<rect width="1200" height="820" fill="#fff"/>',
                      '<g fill="none" stroke="#000" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">']
        category = 'GATE' if self.meta['gate'] else 'FIGURE'
        self.text(52, 42, f'THE SUPPORT MACHINE  /  {category} {number:02}', 16, bold=True, spacing=1.2)
        self.text(52, 94, self.meta['title'], 36, bold=True)
        self.text(52, 132, question, 22)
        self.line(52, 730, 1148, 730, width=1.3)
        self.text(52, 762, 'GATE EVIDENCE' if self.meta['gate'] else 'READ THE RESULT', 14, bold=True, spacing=1)
        self.text(52, 791, takeaway, 21)
        self.meta['takeaway'] = takeaway
        self.body_start = len(self.parts)

    def add(self, s):
        self.parts.append(s)

    def path(self, d, fill='none', width=2.5, dash=None):
        self.add(f'<path d="{d}" fill="{fill}" stroke-width="{width}"' + (f' stroke-dasharray="{dash}"' if dash else '') + '/>')

    def line(self, x1, y1, x2, y2, width=2.5, dash=None):
        length = math.hypot(x2-x1, y2-y1)
        wobble = min(1.3, length/35)
        cx = (x1+x2)/2 + self.rng.uniform(-wobble, wobble)
        cy = (y1+y2)/2 + self.rng.uniform(-wobble, wobble)
        self.path(f'M {x1} {y1} Q {cx:.2f} {cy:.2f} {x2} {y2}', width=width, dash=dash)

    def poly(self, pts, fill='none', width=2.5, closed=True):
        d = f'M {pts[0][0]} {pts[0][1]}'
        for a, b in zip(pts, pts[1:] + ([pts[0]] if closed else [])):
            dx = self.rng.uniform(-.9, .9)
            dy = self.rng.uniform(-.9, .9)
            d += f' Q {(a[0]+b[0])/2+dx:.2f} {(a[1]+b[1])/2+dy:.2f} {b[0]} {b[1]}'
        if closed:
            d += ' Z'
        self.path(d, fill=fill, width=width)

    def circle(self, x, y, r, width=2.5, fill='none'):
        self.path(f'M {x+r} {y} C {x+r+.7} {y+r*.56} {x+r*.54} {y+r+.5} {x} {y+r} C {x-r*.57} {y+r} {x-r-.5} {y+r*.55} {x-r} {y} C {x-r} {y-r*.57} {x-r*.56} {y-r-.6} {x} {y-r} C {x+r*.56} {y-r} {x+r+.4} {y-r*.54} {x+r} {y} Z', width=width, fill=fill)

    def text(self, x, y, s, size=22, bold=False, anchor='start', spacing=0, note=False):
        family = 'Bradley Hand, Noteworthy, Arial, sans-serif' if note else 'Arial, Helvetica, sans-serif'
        self.add(f'<text x="{x}" y="{y}" fill="#000" stroke="none" font-family="{family}" font-size="{size}" font-weight="{700 if bold else 400}" text-anchor="{anchor}" letter-spacing="{spacing}">{escape(str(s))}</text>')

    def lines(self, x, y, ss, size=22, bold=False, anchor='middle', gap=None):
        for i, s in enumerate(ss):
            self.text(x, y+i*(gap or size*1.28), s, size, bold, anchor)

    def arrowhead(self, a, b, length=10, width=2.3):
        dx, dy = b[0]-a[0], b[1]-a[1]
        l = math.hypot(dx, dy)
        ux, uy = dx/l, dy/l
        self.poly([(b[0]-length*ux+length*.45*uy, b[1]-length*uy-length*.45*ux), b,
                   (b[0]-length*ux-length*.45*uy, b[1]-length*uy+length*.45*ux)], closed=False, width=width)

    def curve(self, a, c1, c2, b, arrow=False, width=2.3, dash=None):
        self.path(f'M {a[0]} {a[1]} C {c1[0]} {c1[1]} {c2[0]} {c2[1]} {b[0]} {b[1]}', width=width, dash=dash)
        if arrow:
            self.arrowhead(c2, b, width=width)

    def begin(self, x, y, scale=1, rotate=0):
        self.add(f'<g transform="translate({x} {y}) rotate({rotate}) scale({scale})">')

    def end(self):
        self.add('</g>')

    def bubble(self, x, y, scale=1):
        self.begin(x, y, scale)
        self.path('M -25 -18 Q -26 -25 -18 -25 L 23 -25 Q 30 -25 30 -17 L 30 12 Q 30 20 23 20 L -4 20 L -19 32 L -17 20 L -20 20 Q -27 20 -26 12 Z', fill='#fff')
        for xx in [-13, 2, 17]:
            self.circle(xx, -1, 2, fill='#000', width=1)
        self.end()

    def book(self, x, y, scale=1):
        self.begin(x, y, scale)
        self.path('M 0 -18 Q -18 -29 -40 -24 L -40 25 Q -17 21 0 33 Q 18 21 40 25 L 40 -24 Q 19 -29 0 -18 Z', fill='#fff')
        self.path('M 0 -18 Q 1 6 0 33', width=2)
        for yy in [-11, 0, 11]:
            self.path(f'M -31 {yy} Q -18 {yy-2} -9 {yy+5}', width=1.4)
            self.path(f'M 9 {yy+5} Q 20 {yy-2} 31 {yy}', width=1.4)
        self.path('M -43 -18 L -44 30 Q -19 25 -2 38 Q 18 26 44 30 L 44 -18', width=1.2)
        self.end()

    def plug(self, x, y, scale=1):
        self.begin(x, y, scale)
        self.path('M -21 -16 L 23 -16 L 23 1 Q 23 23 1 25 Q -21 23 -21 1 Z', fill='#fff')
        self.line(-12, -16, -12, -37, width=3)
        self.line(14, -16, 14, -37, width=3)
        self.path('M 1 25 L 1 35 C 1 59 36 54 42 39', width=2.4)
        self.path('M -14 4 Q -13 14 -6 16', width=1.2)
        self.end()

    def wrench(self, x, y, scale=1, rotate=0):
        self.begin(x, y, scale, rotate)
        self.path('M -22 -31 C -41 -22 -40 0 -23 10 Q -15 15 -7 11 L 18 44 Q 24 50 31 43 Q 37 38 31 31 L 4 -1 Q 13 -18 -2 -30 L -1 -14 L -12 -9 L -23 -18 Z', fill='#fff')
        self.circle(25, 39, 2.5, width=1.3)
        self.path('M -3 12 L 21 40', width=1.1)
        self.end()

    def crate(self, x, y, scale=1):
        self.begin(x, y, scale)
        self.poly([(-42,-18), (0,-39), (44,-16), (1,8)], fill='#fff')
        self.poly([(-42,-18), (1,8), (1,48), (-42,22)], fill='#fff')
        self.poly([(1,8), (44,-16), (44,24), (1,48)], fill='url(#hatch)', width=1.8)
        self.poly([(-22,-28), (21,-4), (21,8), (10,15), (10,2), (-33,-22)], fill='#fff', width=1.5)
        self.line(-33,8,-14,19,width=1.7)
        self.line(-33,15,-22,22,width=1.4)
        self.end()

    def owner(self, x, y, scale=1):
        self.begin(x, y, scale)
        self.circle(0,-17,10,fill='#fff')
        self.path('M -23 28 Q -22 0 -3 0 L 3 0 Q 22 0 23 28 Z',fill='#fff')
        self.path('M -12 5 L -10 28 M 12 5 L 10 28',width=1.2)
        self.end()

    def cost(self, x, y, scale=1):
        self.begin(x, y, scale)
        self.circle(0,0,21,fill='#fff',width=2)
        self.text(0,9,'$',28,anchor='middle')
        self.curve((-29,6),(-44,-23),(-7,-47),(23,-26),arrow=True,width=1.7)
        self.curve((29,-4),(44,24),(7,47),(-23,26),arrow=True,width=1.7)
        self.end()

    def door(self, x, y, scale=1):
        self.begin(x,y,scale)
        self.poly([(-19,29),(-19,-31),(17,-31),(17,29)],closed=False)
        self.poly([(-19,-31),(4,-21),(4,37),(-19,29)],fill='#fff')
        self.circle(-3,9,1.3,fill='#000',width=1)
        self.line(13,4,41,4,width=2)
        self.arrowhead((25,4),(41,4),length=8,width=2)
        self.line(-26,37,-13,37,width=1.2)
        self.end()

    def calendar(self,x,y,number,rotate=0):
        self.begin(x,y,1,rotate)
        self.poly([(-62,-51),(60,-51),(61,43),(47,58),(-62,57)],fill='#fff')
        self.path('M 61 43 L 46 42 L 47 58',width=1.7)
        self.line(-61,-24,60,-24,width=1.7)
        for xx in [-35,34]:
            self.path(f'M {xx-4} -45 L {xx-4} -60 Q {xx} -67 {xx+4} -60 L {xx+4} -45',width=2.5)
        self.text(0,27,number,48 if len(str(number))<3 else 28,bold=True,anchor='middle')
        self.path('M -65 -45 L -66 61 L 41 62',width=1.1)
        self.end()

    def lens(self,x,y,scale=1):
        self.begin(x,y,scale)
        self.circle(0,0,28,width=2.6,fill='#fff')
        self.path('M -17 -8 Q -10 -21 5 -18',width=1.2)
        self.poly([(17,23),(38,45),(45,38),(23,17)],fill='url(#hatch)',width=2)
        self.end()

    def player(self,x,y,scale=1,keeper=False):
        self.begin(x,y,scale)
        self.circle(0,-49,11,fill='#fff')
        if keeper:
            self.path('M -15 -28 L -32 -13 L -43 -29 L -50 -24 L -35 1 L -17 -7 L -15 23 L 16 23 L 17 -7 L 35 1 L 50 -24 L 43 -29 L 32 -13 L 15 -28 Q 0 -34 -15 -28 Z',fill='#fff')
            self.circle(-47,-30,5,width=1.7,fill='#fff')
            self.circle(47,-30,5,width=1.7,fill='#fff')
        else:
            self.path('M -15 -28 L -32 -9 L -45 -17 L -49 -9 L -30 4 L -17 -8 L -14 23 L 17 23 L 17 -7 L 36 -1 L 47 -19 L 40 -23 L 32 -11 L 15 -28 Q 0 -34 -15 -28 Z',fill='#fff')
        self.poly([(-14,23),(-15,39),(-2,39),(1,28),(4,39),(17,39),(17,23)],fill='#fff',width=2)
        self.path('M -13 39 L -17 59 L -25 63 L -25 67 L -11 67 L -4 41 M 6 40 L 14 61 L 23 61 L 24 66 L 10 68 L 0 43',width=2.3)
        self.line(-10,-25,-8,18,width=1.1)
        self.end()

    def ball(self,x,y,r=14):
        self.circle(x,y,r,fill='#fff',width=1.8)
        self.poly([(x,y-r*.47),(x+r*.47,y-r*.12),(x+r*.27,y+r*.44),(x-r*.27,y+r*.44),(x-r*.47,y-r*.12)],fill='#000',width=.8)
        for a,b in [((0,-.47),(0,-1)),((.47,-.12),(.95,-.3)),((.27,.44),(.57,.83)),((-.27,.44),(-.57,.83)),((-.47,-.12),(-.95,-.3))]:
            self.line(x+a[0]*r,y+a[1]*r,x+b[0]*r,y+b[1]*r,width=1)

    def save(self):
        OUTPUT.mkdir(parents=True,exist_ok=True)
        (OUTPUT / (self.meta['slug']+'.svg')).write_text('\n'.join(self.parts+['</g>','</svg>'])+'\n')
        book = self.parts[:6] + self.parts[self.body_start:] + ['</g>','</svg>']
        book[0] = book[0].replace('width="1200" height="820" viewBox="0 0 1200 820"', 'width="1120" height="545" viewBox="40 170 1120 545"')
        (OUTPUT / (self.meta['slug']+'-book.svg')).write_text('\n'.join(book)+'\n')


def paper(d,x,y,scale=1,rotate=0,review=False):
    d.begin(x,y,scale,rotate)
    d.poly([(-38,-45),(19,-45),(37,-27),(37,46),(-38,46)],fill='#fff',width=2.2)
    d.poly([(19,-45),(19,-27),(37,-27)],closed=False,width=1.5)
    for yy in [-19,0,19]:
        if review:
            d.poly([(-28,yy),(-23,yy+5),(-15,yy-7)],closed=False,width=1.6)
            d.line(-6,yy,24,yy,width=1.4)
        else: d.line(-25,yy,23 if yy!=19 else 11,yy,width=1.5)
    d.end()


def product(d,x,y,scale=1):
    d.begin(x,y,scale)
    d.poly([(-42,-30),(42,-30),(42,27),(-42,27)],fill='#fff',width=2)
    d.line(-42,-15,42,-15,width=1.4)
    for xx in [-32,-24,-16]: d.circle(xx,-23,1.3,fill='#000',width=.6)
    d.poly([(-17,-2),(-25,6),(-17,13)],closed=False,width=1.8)
    d.poly([(-2,-2),(6,6),(-2,13)],closed=False,width=1.8)
    d.wrench(29,13,.63,-20)
    d.end()


def machine(d,x,y,scale=1):
    d.begin(x,y,scale)
    d.poly([(-36,-31),(36,-31),(36,31),(-36,31)],fill='#fff')
    for xx in [-21,0,21]:
        d.line(xx,-31,xx,-42,width=1.6)
        d.line(xx,31,xx,42,width=1.6)
    for yy in [-18,0,18]:
        d.line(-36,yy,-47,yy,width=1.6)
        d.line(36,yy,47,yy,width=1.6)
    d.circle(-11,-3,7,width=1.8)
    d.circle(13,9,5,width=1.8)
    d.line(-9,4,8,8,width=1.6)
    d.path('M -24 -22 L 24 -22',width=1)
    d.end()


def lever(d,x,y,scale=1):
    d.begin(x,y,scale)
    d.poly([(-36,27),(26,27),(41,16),(-20,16)],fill='#fff',width=2)
    d.poly([(-36,27),(26,27),(26,39),(-36,39)],fill='url(#hatch)',width=1.5)
    d.poly([(26,27),(41,16),(41,28),(26,39)],fill='#fff',width=1.5)
    d.circle(0,17,7,fill='#fff',width=1.8)
    d.poly([(-4,12),(17,-31),(25,-27),(4,17)],fill='#fff',width=2)
    d.circle(22,-31,9,fill='#fff',width=2)
    d.curve((-28,-5),(-24,-25),(-10,-38),(4,-39),arrow=True,width=1.4)
    d.end()


def lock(d,x,y,scale=1):
    d.begin(x,y,scale)
    d.path('M -19 -9 L -19 -23 C -19 -48 20 -48 20 -23 L 20 -9',width=3)
    d.poly([(-30,-9),(31,-9),(31,36),(-30,36)],fill='#fff')
    d.circle(0,8,5,width=1.7)
    d.line(0,13,0,24,width=2.2)
    d.path('M -24 27 L -24 31 L -11 31',width=1)
    d.end()


def receipt(d,x,y,scale=1,unknown=False):
    d.begin(x,y,scale)
    d.poly([(-35,-43),(35,-43),(35,45),(24,38),(12,45),(0,38),(-12,45),(-24,38),(-35,45)],fill='#fff',width=2.2)
    d.line(-23,-28,21,-28,width=1.4)
    d.line(-23,-18,8,-18,width=1.2)
    if unknown: d.text(0,24,'?',39,bold=True,anchor='middle')
    else:
        d.circle(0,10,18,width=1.7)
        d.poly([(-10,10),(-2,18),(12,1)],closed=False,width=2)
    d.end()


def diagnose():
    d=Sketch(1,'What is creating the work?',
             'Classified customer tasks and candidate fixes.')
    paper(d,133,383,1.02,-11)
    paper(d,155,395,1.02,5)
    paper(d,167,406,1.02,-3)
    d.lines(151,519,['Customer','questions'],23,True)
    d.curve((220,405),(253,400),(279,398),(312,399),arrow=True)
    paper(d,378,386,.95,3)
    d.lens(400,412,1.25)
    d.lines(389,527,['Read the evidence'],23,True)
    d.text(389,564,'Start with a sample.',26,anchor='middle',note=True)
    d.path('M 486 398 C 565 395 534 238 620 238 M 486 398 C 549 400 556 350 620 350 M 486 398 C 552 397 557 469 620 469 M 486 398 C 557 403 535 586 620 586',width=1.7)
    for yy in [238,350,469,586]: d.arrowhead((596,yy),(620,yy),width=1.7)
    rows=[(238,'Fix the product','Product behavior'),(350,'Improve guidance','Hard-to-find or unclear answer'),(469,'Test automation','Repeatable, bounded task'),(586,'Human investigation','Uncertain or complex problem')]
    product(d,690,236,.78)
    d.book(690,348,.76)
    d.begin(690,466,.82)
    d.curve((-28,-14),(-9,-45),(36,-29),(31,4),arrow=True,width=2)
    d.curve((23,25),(-13,46),(-42,14),(-27,-10),arrow=True,width=2)
    d.poly([(-10,-7),(12,-7),(12,14),(-10,14)],fill='#fff',width=1.6)
    d.end()
    d.owner(681,583,.85)
    d.lens(705,600,.39)
    for yy,title,sub in rows:
        d.text(759,yy-4,title,24,bold=True)
        d.text(759,yy+26,sub,20)
    d.save()


def choose():
    d=Sketch(2,'What should you buy, extend, or build at each layer?',
             'An owner, lifecycle cost and exit path for each component.')
    d.text(70,205,'COMPONENTS',15,bold=True,spacing=1)
    d.text(670,205,'DECIDE AT EACH LAYER',15,bold=True,spacing=1)
    for i,(label,icon) in enumerate([('Conversation platform','chat'),('Knowledge & retrieval','book'),('Tools & integrations','plug'),('Evaluation & reporting','eval')]):
        y=240+i*90
        d.poly([(85,y+56),(480,y+56),(480,y+70),(85,y+70)],fill='url(#hatch)',width=1.6)
        d.poly([(480,y+56),(545,y),(545,y+14),(480,y+70)],fill='url(#hatch)',width=1.6)
        d.poly([(85,y+56),(480,y+56),(545,y),(150,y)],fill='#fff')
        d.text(180,y+38,label,22,bold=True)
        if icon=='chat': d.bubble(150,y+31,.48)
        elif icon=='book': d.book(150,y+30,.38)
        elif icon=='plug': d.plug(148,y+27,.38)
        else:
            d.circle(150,y+27,15,width=1.6,fill='#fff')
            d.line(140,y+33,140,y+27,width=2)
            d.line(150,y+33,150,y+19,width=2)
            d.line(160,y+33,160,y+23,width=2)
    d.path('M 568 239 Q 594 237 594 267 L 594 380 Q 595 400 614 410 Q 596 420 594 442 L 594 550 Q 594 580 568 580',width=1.7)
    d.curve((617,410),(627,409),(637,406),(650,400),arrow=True,width=1.8)
    d.text(908,262,'Choose your mix.',27,anchor='middle',note=True)
    d.crate(726,347,1.05)
    d.plug(900,340,1.12)
    d.wrench(1085,340,1.4,25)
    for x,label in [(726,'BUY'),(902,'EXTEND'),(1080,'BUILD')]:
        d.text(x,434,label,22,bold=True,anchor='middle',spacing=.7)
    d.path('M 671 459 Q 902 468 1133 459',width=1.1)
    d.text(902,490,'All three are options for every layer.',20,anchor='middle')
    d.text(670,543,'OPERATE WHAT YOU CHOOSE',15,bold=True,spacing=1)
    d.owner(726,600,.74)
    d.cost(902,602,.74)
    d.door(1076,601,.74)
    for x,label in [(726,'Owner'),(902,'Lifecycle cost'),(1080,'Exit path')]:
        d.text(x,658,label,20,anchor='middle')
    d.text(85,641,'Illustrative layers',18)
    d.path('M 85 651 Q 173 648 232 652',width=1.1)
    d.save()


def guardrails():
    d=Sketch(3,'What may the system know, say, and do?',
             'Allowed actions, evidence checks and a clear human exit.')
    d.bubble(128,383,1.22)
    d.lines(130,466,['Customer','request'],23,True)
    d.path('M 180 388 L 245 388 M 245 388 C 296 387 258 269 330 269 M 245 388 C 297 387 255 514 330 514',width=1.9)
    d.arrowhead((307,269),(330,269),width=1.9)
    d.arrowhead((307,514),(330,514),width=1.9)
    d.text(382,204,'ANSWER',16,bold=True,spacing=1)
    d.text(383,446,'ACT',16,bold=True,spacing=1)
    d.book(419,266,.95)
    d.bubble(728,267,1.35)
    d.lens(1032,267,1.1)
    for x,ss in [(420,['Applicable','sources']),(730,['Grounded','answer']),(1045,['Review','quality'])]:
        d.lines(x,346,ss,23,True)
    d.curve((483,266),(535,254),(601,255),(659,266),arrow=True,width=2)
    d.curve((785,266),(857,256),(919,257),(983,266),arrow=True,width=2)
    lock(d,419,514,1)
    lever(d,730,513,1.05)
    receipt(d,1043,513,1.0)
    for x,ss in [(420,['Permission','check']),(730,['Execute','within scope']),(1045,['Receipt and','effect check'])]:
        d.lines(x,589,ss,23,True)
    d.curve((463,514),(523,503),(608,503),(669,514),arrow=True,width=2)
    d.curve((789,514),(852,503),(924,503),(991,514),arrow=True,width=2)
    d.begin(367,676)
    d.poly([(-14,-22),(14,-22),(25,-10),(25,10),(14,22),(-14,22),(-25,10),(-25,-10)],fill='#fff',width=1.6)
    d.line(-12,0,12,0,width=2.5)
    d.end()
    d.text(408,684,'Missing evidence or authority? Stop and hand off.',23)
    d.save()


def shadow():
    d=Sketch(4,'Can the candidate handle real cases without touching live customer state?',
             'A reviewed scorecard, observed failures and a release decision.')
    paper(d,138,384,1.1,-4)
    d.circle(167,427,22,fill='#fff',width=1.8)
    d.poly([(167,411),(167,427),(178,433)],closed=False,width=1.8)
    d.lines(141,496,['Same case'],24,True)
    d.lines(141,531,['Request-time','evidence'],20)
    d.path('M 207 396 L 266 396 M 266 396 C 307 397 279 269 355 269 M 266 396 C 307 397 279 524 355 524',width=1.8)
    for yy in [269,524]: d.arrowhead((333,yy),(355,yy),width=1.8)
    d.owner(433,266,1.1)
    d.lens(460,289,.52)
    paper(d,747,269,.95,-2,review=True)
    d.lines(440,347,['Human reference','review'],23,True)
    d.lines(748,347,['Reviewed','reference'],23,True)
    d.curve((505,267),(552,259),(618,259),(683,267),arrow=True,width=2)
    d.path('M 359 419 Q 612 409 858 419 Q 889 422 887 455 L 886 633 Q 886 656 855 657 Q 600 664 355 657 Q 326 657 327 631 L 327 455 Q 327 422 359 419 Z',width=1.4,dash='7 7')
    d.text(354,448,'ISOLATED ENVIRONMENT',15,bold=True,spacing=.6)
    machine(d,439,522,.88)
    paper(d,748,522,.87,-2)
    d.curve((499,522),(556,512),(621,512),(689,522),arrow=True,width=2)
    d.text(439,596,'Candidate run',23,bold=True,anchor='middle')
    d.text(748,596,'Observed behavior',23,bold=True,anchor='middle')
    d.text(605,637,'No customer messages. No live writes.',20,anchor='middle')
    d.curve((798,270),(917,270),(918,355),(977,371),arrow=True,width=1.8)
    d.curve((798,524),(917,524),(919,439),(977,419),arrow=True,width=1.8)
    paper(d,1043,397,1.02,3,review=True)
    d.text(1043,493,'Compare',23,bold=True,anchor='middle')
    d.text(1043,524,'and decide',23,bold=True,anchor='middle')
    d.save()


def launch():
    d=Sketch(5,'Who decides, who watches, and who can stop the rollout?',
             'Named owners, cutover checks and tested recovery capacity.')
    xs=[154,444,744,1040]
    paper(d,154,282,.94,-3,review=True)
    lever(d,444,282,1.02)
    d.begin(744,282)
    d.path('M -41 25 A 45 45 0 1 1 41 25 Z',fill='#fff',width=2.3)
    d.line(-26,-11,-20,-6,width=1.5)
    d.line(0,-27,0,-18,width=1.5)
    d.line(27,-10,21,-5,width=1.5)
    d.line(0,14,24,-13,width=2.4)
    d.circle(0,14,4,fill='#fff',width=1.6)
    d.end()
    d.begin(1040,282)
    d.line(-24,-42,-24,41,width=2.5)
    d.path('M -24 -37 Q -5 -48 13 -35 Q 27 -26 40 -35 L 40 4 Q 26 15 12 2 Q -6 -11 -24 1 Z',fill='#fff',width=2.2)
    d.poly([(-7,-21),(1,-12),(18,-26)],closed=False,width=2)
    d.line(-35,42,-11,42,width=1.4)
    d.end()
    for x in xs[:-1]: d.curve((x+60,282),(x+106,270),(x+163,270),(x+225,282),arrow=True,width=2)
    for x,title,sub,owner in zip(xs,['Ready','Cut over','Observe','Continue'],['Checks and owners','Bounded rollout','Customer evidence','Criteria met'],['Release owner','Routing owner','Support lead','Decision owner']):
        d.text(x,363,title,25,bold=True,anchor='middle')
        d.text(x,397,sub,20,anchor='middle')
        d.text(x,444,owner,20,anchor='middle')
    d.text(906,244,'Pass',19,anchor='middle')
    d.curve((744,465),(744,487),(744,503),(744,522),arrow=True,width=1.8)
    d.text(767,500,'Stop condition',20)
    d.begin(744,574)
    d.line(-44,10,44,10,width=2.2)
    d.line(-44,23,44,23,width=2.2)
    d.poly([(-19,-3),(19,-3),(19,36),(-19,36)],fill='#fff',width=2)
    d.line(0,-3,0,-17,width=2)
    d.circle(0,-30,17,width=2.2,fill='#fff')
    d.line(-12,-42,12,-18,width=1.5)
    d.line(-12,-18,12,-42,width=1.5)
    d.end()
    d.owner(1040,574,1.1)
    d.curve((805,581),(863,567),(920,568),(974,581),arrow=True,width=1.9)
    d.text(744,643,'Contain',24,bold=True,anchor='middle')
    d.text(744,672,'Pause affected capability',19,anchor='middle')
    d.text(1040,643,'Serve customers',24,bold=True,anchor='middle')
    d.text(1040,672,'Staffed human path',19,anchor='middle')
    d.text(75,568,'A release needs',27,note=True)
    d.text(75,601,'a way to stop.',27,note=True)
    d.text(75,660,'Test repairs before restarting',20)
    d.text(75,686,'the affected capability.',20)
    d.save()


def operate():
    d=Sketch(6,'Does feedback lead to a change that helps customers?',
             'An assigned owner, a tested change and later evidence of its effect.')
    paper(d,176,280,.91,-5)
    d.bubble(204,301,.59)
    paper(d,597,280,.91,3)
    d.lens(627,298,.79)
    d.owner(1024,280,1.1)
    for x,ss in [(180,['Customer','evidence']),(600,['Review','failures']),(1024,['Assign','an owner'])]:
        d.lines(x,362,ss,23,True)
    d.curve((242,280),(335,249),(438,251),(525,280),arrow=True,width=2)
    d.curve((674,280),(765,251),(860,251),(953,280),arrow=True,width=2)
    d.curve((1091,312),(1158,365),(1158,455),(1090,511),arrow=True,width=2)
    machine(d,1017,557,.82)
    d.circle(1056,580,18,fill='#fff',width=1.7)
    d.poly([(1047,581),(1053,587),(1066,572)],closed=False,width=2)
    lever(d,600,558,.98)
    d.calendar(178,558,'LATER',-2)
    d.lens(232,596,.57)
    for x,ss in [(1024,['Test the','change']),(600,['Release']),(180,['Check later','outcomes'])]:
        d.lines(x,649,ss,23,True)
    d.curve((951,558),(852,590),(755,590),(670,558),arrow=True,width=2)
    d.curve((535,558),(442,588),(345,588),(260,558),arrow=True,width=2)
    d.curve((105,515),(40,463),(40,373),(107,316),arrow=True,width=2)
    d.text(600,454,'Knowledge · policy · tools · people',23,anchor='middle')
    d.text(600,491,'Keep the loop moving.',28,anchor='middle',note=True)
    d.save()


def sixteen():
    d=Sketch(7,'An illustrative cohort of 100 eligible conversations.',
             'Reported resolution still needs a separate customer-outcome check.')
    specs=[(187,100,'Eligible',10,10,277,'#fff'),(600,40,'Agent-involved',10,4,346,'#000'),(1010,16,'Reported resolved',4,4,346,'#000')]
    for cx,count,label,cols,rows,y,fill in specs:
        d.text(cx,217,str(count),47,bold=True,anchor='middle')
        d.text(cx,254,label,22,bold=True,anchor='middle')
        left=cx-(cols-1)*23/2
        for row in range(rows):
            for col in range(cols): d.circle(left+col*23,y+row*23,7,fill=fill,width=1.5)
    d.curve((324,382),(369,365),(410,365),(454,382),arrow=True,width=2)
    d.lines(390,316,['40%','involved'],20)
    d.curve((737,382),(795,365),(850,365),(908,382),arrow=True,width=2)
    d.lines(825,316,['40%','of those 40'],20)
    d.text(600,570,'40% × 40% = 16%',43,bold=True,anchor='middle')
    d.text(600,611,'40 / 100 × 16 / 40 = 16 / 100',24,anchor='middle')
    d.text(600,671,'Same population. Aligned definitions. One observation period.',22,anchor='middle')
    d.save()


def evaluation():
    d=Sketch(8,'Did the customer return with the same problem?',
             'Customer silence alone does not prove success.')
    for x,s in [(150,'DAY 0'),(580,'DAY 7'),(1010,'DAY 30')]:
        d.text(x,211,s,17,bold=True,anchor='middle',spacing=1)
    d.begin(150,293,1,-2)
    d.path('M -61 -50 Q -66 -50 -66 -40 L -66 27 Q -66 37 -55 37 L -32 37 L -45 58 L -9 37 L 60 37 Q 70 36 69 26 L 68 -40 Q 68 -50 57 -50 Z',fill='#fff')
    d.circle(0,-11,17,width=2)
    d.poly([(-9,-11),(-2,-4),(11,-19)],closed=False,width=2.6)
    d.text(0,22,'Resolved',19,anchor='middle')
    d.end()
    d.calendar(580,295,'7',-2)
    d.lens(639,337,.8)
    d.calendar(1010,295,'30',2)
    d.lens(1069,337,.8)
    d.lines(150,391,['Reported','resolved'],23,True)
    for x in [580,1010]:
        d.lines(x,391,['Related return, reopen','or same-issue contact?'],21)
    d.curve((150,454),(442,448),(805,463),(1134,454),arrow=True,width=2)
    for x in [150,580,1010]:
        d.circle(x,454,6,width=1.8,fill='#fff')
    d.path('M 553 479 L 553 486 Q 784 493 1040 486 L 1040 479',width=1.4)
    d.text(797,516,'Mature windows + known coverage',20,bold=True,anchor='middle')
    d.text(797,542,'Only then does a case enter each rate.',18,anchor='middle')
    d.text(115,517,'Wait for the full window.',25,note=True)
    d.line(52,570,1148,570,width=1.1)
    d.begin(164,637,1,-6)
    d.poly([(-59,-44),(24,-44),(44,-25),(44,46),(-59,46)],fill='#fff',width=1.8)
    d.poly([(24,-44),(24,-25),(44,-25)],closed=False,width=1.3)
    for yy in [-21,-4,13]:
        d.line(-45,yy,15,yy,width=1.4)
    d.end()
    d.lens(210,653,.84)
    d.text(300,606,'WEEKLY INDEPENDENT ANSWER REVIEW',16,bold=True,spacing=.7)
    d.text(300,644,'Correct?  ·  Right intent?  ·  Workable fix?',24,bold=True)
    d.text(300,687,'Try to prove the answer wrong.',27,note=True)
    d.save()


def unknown():
    d=Sketch(9,'What happened before the timeout?',
             'Recover the unfinished step without duplicating a completed effect.')
    paper(d,152,261,.91,-2,review=True)
    lever(d,444,261,.97)
    receipt(d,740,261,.98,unknown=True)
    d.bubble(1040,261,1.2)
    for x,ss in [(152,['Authorized','intent']),(444,['Attempt','execution']),(740,['Receipt and','effect check']),(1040,['Report','result'])]:
        d.lines(x,343,ss,23,True)
    for a,b in [(211,381),(504,681),(794,977)]:
        d.curve((a,261),(a+47,252),(b-47,252),(b,261),arrow=True,width=2)
    d.text(886,222,'Confirmed',19,anchor='middle')
    d.curve((740,390),(740,406),(740,425),(740,443),arrow=True,width=1.8)
    d.text(766,423,'Unknown',19)
    paper(d,675,484,.64,3)
    d.lens(693,501,.61)
    d.owner(797,487,.72)
    d.text(740,555,'Reconcile first',25,bold=True,anchor='middle')
    d.text(740,584,'Provider state or human owner',19,anchor='middle')
    d.text(73,471,'Find the effect',28,note=True)
    d.text(73,506,'before you retry.',28,note=True)
    d.line(52,608,1148,608,width=1.1)
    d.text(52,638,'EXAMPLE',14,bold=True,spacing=1)
    d.circle(231,641,19,fill='#fff',width=1.7)
    d.text(231,649,'$',23,anchor='middle')
    d.circle(253,651,10,fill='#fff',width=1.3)
    d.poly([(248,651),(252,655),(258,646)],closed=False,width=1.3)
    d.begin(600,641,.76)
    d.poly([(-31,-21),(31,-21),(31,21),(-31,21)],fill='#fff',width=1.9)
    d.poly([(-31,-21),(0,5),(31,-21)],closed=False,width=1.5)
    d.circle(28,19,13,fill='#fff',width=1.4)
    d.line(22,13,34,25,width=1.7)
    d.line(22,25,34,13,width=1.7)
    d.end()
    d.bubble(1005,637,.64)
    d.curve((310,648),(374,638),(437,638),(501,648),arrow=True,width=1.8)
    d.curve((698,648),(761,638),(826,638),(892,648),arrow=True,width=1.8)
    d.text(240,687,'Credit applied',22,bold=True,anchor='middle')
    d.text(600,687,'Confirmation failed',22,bold=True,anchor='middle')
    d.text(1004,683,'Recover the message',20,bold=True,anchor='middle')
    d.text(1004,708,'Do not repeat the credit',19,anchor='middle')
    d.save()


def midfield():
    d=Sketch(10,'Prevent repeated problems while keeping a human recovery path.',
             'Protected improvement time, product access and a staffed human path.')
    d.poly([(171,245),(1115,245),(1033,623),(88,623)],width=1.6)
    d.path('M 176 240 Q 635 242 1111 240',width=.9)
    d.poly([(154,323),(308,323),(267,548),(105,548)],closed=False,width=1.3)
    d.line(640,245,620,337,width=1.3)
    d.line(566,586,558,623,width=1.3)
    d.path('M 670 433 C 679 381 651 348 610 348 C 568 347 529 385 522 432 C 512 482 543 518 582 518 C 624 519 660 480 670 433 Z',width=1.3)
    d.poly([(77,349),(145,361),(120,475),(53,461)],fill='url(#hatch)',width=1.5)
    d.poly([(145,361),(157,372),(132,487),(120,475)],fill='#fff',width=1.5)
    d.line(77,349,90,362,width=1.1)
    d.line(53,461,65,474,width=1.1)
    d.line(65,474,132,487,width=1.1)
    d.text(70,213,'Keep the goal staffed.',27,note=True)
    d.curve((285,212),(320,220),(222,300),(214,344),arrow=True,width=1.4)
    d.player(209,425,1.05,keeper=True)
    d.lines(204,581,['Human recovery'],21,True)
    d.curve((295,414),(371,377),(433,380),(503,410),arrow=True,width=2.1,dash='8 7')
    d.text(405,361,'Protected time',24,anchor='middle',note=True)
    d.player(593,420,1.17)
    d.ball(643,501,14)
    d.text(592,569,'Support engineers',22,bold=True,anchor='middle')
    d.curve((657,393),(724,366),(753,310),(830,309),arrow=True,width=2)
    d.curve((665,432),(741,426),(819,428),(883,429),arrow=True,width=2)
    d.curve((671,470),(727,496),(751,549),(805,548),arrow=True,width=2)
    d.book(899,299,.79)
    d.text(899,360,'Documentation',21,bold=True,anchor='middle')
    d.begin(951,426)
    d.poly([(-42,-30),(42,-30),(42,27),(-42,27)],fill='#fff',width=2)
    d.line(-42,-15,42,-15,width=1.4)
    for xx in [-32,-24,-16]:
        d.circle(xx,-23,1.2,fill='#000',width=.5)
    d.poly([(-17,-2),(-25,6),(-17,13)],closed=False,width=1.8)
    d.poly([(-2,-2),(6,6),(-2,13)],closed=False,width=1.8)
    d.wrench(29,13,.63,-20)
    d.end()
    d.text(955,486,'Product fixes',21,bold=True,anchor='middle')
    d.begin(875,550)
    d.line(0,-29,0,28,width=2.2)
    d.poly([(-34,-24),(26,-24),(38,-13),(26,-2),(-34,-2)],fill='#fff',width=2)
    d.poly([(-25,3),(27,3),(27,20),(-25,20),(-34,12)],fill='#fff',width=2)
    d.line(-7,29,10,29,width=1.4)
    d.end()
    d.text(877,604,'Onboarding',21,bold=True,anchor='middle')
    d.text(600,686,'Fix what keeps sending the ball back.',25,anchor='middle',note=True)
    d.save()


for fn in [diagnose,choose,guardrails,shadow,launch,operate,sixteen,evaluation,unknown,midfield]:
    fn()
(OUTPUT/'manifest.json').write_text(json.dumps({
    'style':'Monochrome architect sketch: objects, selective hatching, curved connectors, restrained hand-drawn contours, clear labels.',
    'status':'Approved visual direction for the Second Edition.',
    'width':W,'height':H,'figures':FIGURES},ensure_ascii=False,indent=2)+'\n')
gallery=['# The Support Machine illustrations','',
         'Ten companion drawings in a shared black-and-white architectural sketch style. Each appears beside its discussion in the Second Edition.','']
for figure in FIGURES:
    gallery += [f'## {figure["title"]}','',figure['caption'],'',
                f'![{figure["title"]}]({figure["slug"]}.png)','',
                f'[PNG]({figure["slug"]}.png) · [SVG]({figure["slug"]}.svg)','']
(OUTPUT/'README.md').write_text('\n'.join(gallery))
print(f'Created {len(FIGURES)} full illustrations and {len(FIGURES)} book-layout SVGs.')
