"""Figures scientifiques originales pour le cours de glucides et le corrigé du TD1.
Les structures sont dessinées explicitement, sans image générative ni recursoisement Web.
Exécution : python scripts/generate_illustrations.py
"""
from pathlib import Path
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'illustrations'
OUT.mkdir(parents=True, exist_ok=True)
NAVY = '#17324D'
TEAL = '#137C7A'
PALE = '#EAF5F3'
BLUE = '#EAF0F8'
GOLD = '#D69A36'
GOLD_PALE = '#FFF4DE'
INK = '#243746'
MUTED = '#627582'
RED = '#AC4545'
GREEN = '#2C795C'
LINE = '#D7E3E7'
WHITE = '#FFFFFF'
plt.rcParams.update({
    'font.family': 'DejaVu Sans', 'font.size': 11,
    'axes.unicode_minus': False, 'savefig.facecolor': 'white',
    'mathtext.fontset': 'dejavusans',
})


def canvas(w=12, h=5, xlim=(0, 12), ylim=(0, 5)):
    fig, ax = plt.subplots(figsize=(w, h), dpi=220)
    fig.subplots_adjust(left=.015, right=.985, top=.985, bottom=.015)
    ax.set(xlim=xlim, ylim=ylim)
    ax.set_aspect('equal')
    ax.axis('off')
    return fig, ax


def save(fig, name):
    fig.savefig(OUT / f'{name}.png', dpi=220, bbox_inches='tight', pad_inches=.12)
    plt.close(fig)
    print(name)


def text(ax, x, y, s, size=11, color=INK, weight='normal', ha='center', va='center', **kw):
    # Les PNG de 12 pouces sont insérés dans environ 6,5 pouces Word :
    # compenser cette réduction pour conserver labels et titres lisibles à l’impression.
    return ax.text(x, y, s, fontsize=size*1.55, color=color, weight=weight, ha=ha, va=va, **kw)


def box(ax, x, y, w, h, title, body='', fc=PALE, ec='none', ts=12, bs=10.5, align='center'):
    ax.add_patch(FancyBboxPatch((x-w/2, y-h/2), w, h,
                 boxstyle='round,pad=0.08,rounding_size=0.13', facecolor=fc, edgecolor=ec, linewidth=1.1))
    if body:
        text(ax, x, y+h*.20, title, ts, NAVY, 'bold', ha=align)
        text(ax, x, y-h*.17, body, bs, INK, ha=align)
    else:
        text(ax, x, y, title, ts, NAVY, 'bold', ha=align)


def arrow(ax, a, b, color=TEAL, lw=1.8, style='-|>', connection='arc3,rad=0', ls='-'):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle=style, mutation_scale=14,
                linewidth=lw, color=color, connectionstyle=connection, linestyle=ls,
                shrinkA=4, shrinkB=4))


def fischer(ax, cx, cy, pattern, keto=False, title='', numbers=True, scale=1,
            highlight_reference=True, highlight_carbonyl=True, mark_chiral=False):
    """pattern : True = OH à droite, de haut en bas, pour les centres chiraux."""
    s = scale
    def pt(x, y): return cx+x*s, cy+y*s
    n = len(pattern) + 2 if not keto else len(pattern) + 3
    if not keto:
        ys = [1.45] + [1.45-i*.58 for i in range(1, len(pattern)+1)] + [1.45-(len(pattern)+1)*.58]
    else:
        ys = [1.70, 1.12] + [1.12-i*.58 for i in range(1, len(pattern)+1)] + [1.12-(len(pattern)+1)*.58]
    if highlight_reference:
        yy = ys[-2]
        ax.add_patch(FancyBboxPatch(pt(-.80, yy-.22), 1.60*s, .44*s,
            boxstyle='round,pad=0.02,rounding_size=0.08', fc=PALE, ec='none', zorder=0))
    if highlight_carbonyl:
        yy = ys[0] if not keto else ys[1]
        ax.add_patch(FancyBboxPatch(pt(-.49, yy-.22), 1.19*s, .44*s,
            boxstyle='round,pad=0.02,rounding_size=0.07', fc=GOLD_PALE, ec='none', zorder=0))
    ax.plot(*zip(pt(0, ys[0]), pt(0, ys[-1])), color=NAVY, lw=1.7*s, zorder=1)
    for i, y in enumerate(ys):
        if numbers:
            text(ax, *pt(-1.03, y), str(i+1), 9*s, TEAL, 'bold')
        if i == 0:
            text(ax, *pt(0, y), 'CHO' if not keto else 'CH₂OH', 11*s, NAVY,
                 bbox=dict(fc='white', ec='none', pad=1.5), zorder=4)
        elif keto and i == 1:
            ax.plot(*zip(pt(-.12, y+.035), pt(.43, y+.035)), color=NAVY, lw=1.5*s)
            ax.plot(*zip(pt(-.12, y-.035), pt(.43, y-.035)), color=NAVY, lw=1.5*s)
            text(ax, *pt(.58, y), 'O', 11*s, NAVY, bbox=dict(fc='white', ec='none', pad=1))
        elif i == len(ys)-1:
            text(ax, *pt(0, y), 'CH₂OH', 11*s, NAVY, bbox=dict(fc='white', ec='none', pad=1.5), zorder=4)
        else:
            right = pattern[i-1] if not keto else pattern[i-2]
            ax.plot(*zip(pt(-.52, y), pt(.52, y)), color=NAVY, lw=1.65*s, zorder=2)
            text(ax, *pt(-.65, y), 'OH' if not right else 'H', 10.5*s,
                 NAVY if not right else MUTED, bbox=dict(fc=PALE if highlight_reference and i==len(ys)-2 else 'white', ec='none', pad=.7), zorder=3)
            text(ax, *pt(.65, y), 'OH' if right else 'H', 10.5*s,
                 NAVY if right else MUTED, bbox=dict(fc=PALE if highlight_reference and i==len(ys)-2 else 'white', ec='none', pad=.7), zorder=3)
            if mark_chiral:
                text(ax, *pt(.99, y), '*', 12*s, GOLD, 'bold')
    if title:
        text(ax, cx, cy+2.12*s, title, 12*s, NAVY, 'bold')
    return ys


def ring_points(kind, cx, cy, scale=1, rotate=False):
    if kind in ('p', 'fp'):
        p = {'O': (.65,.65), 1:(1.4,0), 2:(.7,-.6), 3:(-.7,-.6), 4:(-1.4,0), 5:(-.65,.65)}
        if kind == 'fp':
            # Le sixième atome du cycle est C6, et non un CH2OH exocyclique.
            p = {'O': (.65,.65), 2:(1.4,0), 3:(.7,-.6), 4:(-.7,-.6), 5:(-1.4,0), 6:(-.65,.65)}
    else:
        p = {'O': (0,.85), 2:(1.15,.15), 3:(.65,-.85), 4:(-.65,-.85), 5:(-1.15,.15)}
    if rotate:
        p = {k:(-v[0],-v[1]) for k,v in p.items()}
    return {k:(cx+v[0]*scale,cy+v[1]*scale) for k,v in p.items()}


def haworth(ax, cx, cy, sugar='glc', anomer='alpha', kind='p', scale=.85,
            title='', numbers=True, rotate=False, link=None, label_anomeric=True,
            free_color=None, show_title=True):
    """D-glc/gal pyranose ou D-fru furanose. link supprime le OH anomérique.
    rotate=True : rotation de 180° DANS LE PLAN, sans changer la molécule.
    """
    p = ring_points(kind, cx, cy, scale, rotate)
    order = ['O',1,2,3,4,5,'O'] if kind=='p' else (['O',2,3,4,5,6,'O'] if kind=='fp' else ['O',2,3,4,5,'O'])
    for i in range(len(order)-1):
        a,b = p[order[i]],p[order[i+1]]
        front = all(isinstance(k,int) and k in ([2,3,4] if kind=='p' else [3,4]) for k in (order[i],order[i+1]))
        ax.plot(*zip(a,b), color=NAVY, lw=(3.0 if front else 1.9)*scale, solid_capstyle='round', zorder=1)
    ac = 1 if kind=='p' else 2
    if label_anomeric:
        ax.add_patch(Circle(p[ac], .245*scale, fc=GOLD_PALE if link is None else '#FAE8C7', ec='none', zorder=2))
        if free_color:
            ax.add_patch(Circle(p[ac], .29*scale, fc='none', ec=free_color, lw=1.8, zorder=2))
    for k,(x,y) in p.items():
        lab = 'O' if k=='O' else f'C{"₀₁₂₃₄₅₆"[k]}'
        text(ax,x,y,lab,10.5*scale, TEAL if isinstance(k,int) and k==ac else NAVY,
             'bold' if k=='O' or k==ac else 'normal',
             bbox=dict(fc='white',ec='none',pad=1.1*scale),zorder=5)
    def sub(k, up, lab, length=.76, color=NAVY, size=11, dx=0):
        x,y=p[k]
        sign=(1 if up else -1)*(-1 if rotate else 1)
        yy=y+sign*length*scale
        xx=x+dx*scale*(-1 if rotate else 1)
        ax.plot([x,xx],[y,yy],color=NAVY,lw=1.5*scale,zorder=2)
        text(ax,xx,yy,lab,size*scale,color,'normal',bbox=dict(fc='white',ec='none',pad=1.3*scale),zorder=6)
        return xx,yy
    if kind=='p':
        if link is None:
            sub(1, anomer=='beta', 'OH')
        sub(2,False,'OH')
        sub(3,True,'OH',length=.68)
        if link != 'acceptor4':
            sub(4,sugar=='gal','OH')
        _,y6=sub(5,True,'CH₂OH',length=.83)
        if numbers:
            text(ax,p[5][0]+.52*scale,y6+.02*scale,'6',8.5*scale,TEAL,'bold')
    elif kind=='fp':
        sub(2,anomer=='beta','OH',length=.81)
        x1,y1=sub(2,anomer!='beta','CH₂OH',length=.82,dx=.58)
        if numbers:
            text(ax,x1+(.58 if not rotate else -.58)*scale,y1,'1',8.5*scale,TEAL,'bold')
        sub(3,True,'OH',length=.68)
        sub(4,False,'OH')
        sub(5,False,'OH')
        # C6 appartient au cycle : aucun groupe CH2OH supplémentaire en C5.
    else:
        # En C2, OH et CH2OH (C1) occupent les deux positions hors cycle.
        if link is None:
            sub(2,anomer=='beta','OH',length=.81)
        x1,y1=sub(2,anomer!='beta','CH₂OH',length=.82,dx=.58)
        if numbers:
            text(ax,x1+(.58 if not rotate else -.58)*scale,y1,'1',8.5*scale,TEAL,'bold')
        sub(3,True,'OH',length=.69)
        sub(4,False,'OH',length=.72)
        _,y6=sub(5,True,'CH₂OH',length=.87)
        if numbers:
            text(ax,p[5][0]-.53*scale,y6,'6',8.5*scale,TEAL,'bold')
    if title and show_title:
        text(ax,cx,cy-2.10*scale,title,11.5*scale,NAVY,'bold')
    return p


def classification():
    fig,ax=canvas(12,5.5,(0,12),(0,5.5))
    box(ax,6,4.85,5.1,.70,'GLUCIDES',fc=BLUE,ts=15)
    for x,title,body in [(2.15,'Oses','Non hydrolysables\nen oses plus petits'),(6,'Oligosides','Quelques unités osidiques\n(diholosides : 2)'),(9.85,'Polyosides','Longues chaînes\nd’unités osidiques')]:
        arrow(ax,(6,4.46),(x,3.77))
        box(ax,x,3.05,3.45,1.30,title,body,ts=13,bs=10.5)
    text(ax,2.15,1.98,'Glucose • fructose • ribose',10.5,MUTED)
    text(ax,6,1.98,'Saccharose • lactose • maltose',10.2,MUTED)
    text(ax,9.85,1.98,'Amidon • glycogène • cellulose',10,MUTED)
    box(ax,6,.82,10.9,.78,'Deux critères indépendants : nombre d’unités  ×  fonction carbonyle et longueur carbonée',fc=PALE,ts=11.5)
    save(fig,'c01_classification')


def cover():
    fig,ax=canvas(12,4.8,(0,12),(0,4.8))
    ax.add_patch(FancyBboxPatch((.2,.2),11.6,4.4,boxstyle='round,pad=0.1,rounding_size=0.35',fc='#F5F9FA',ec='none'))
    for x,y,r in [(1.1,3.9,.16),(10.85,3.8,.22),(10.65,.8,.11),(2.1,.85,.10)]:
        ax.add_patch(Circle((x,y),r,fc=PALE,ec='none'))
    haworth(ax,3.5,2.6,'glc','alpha',scale=1.03,show_title=False)
    haworth(ax,8.7,2.65,'fru','beta',kind='f',scale=1.02,show_title=False)
    text(ax,3.5,.48,'ALDOSE • CYCLE PYRANE',10,TEAL,'bold')
    text(ax,8.65,.48,'CÉTOSE • CYCLE FURANE',10,TEAL,'bold')
    text(ax,6,4.34,'DES ATOMES AUX STRUCTURES',10.5,MUTED,'bold')
    save(fig,'c00_couverture')


def linear_oses():
    fig,ax=canvas(12,5.2,(0,12),(0,5.2))
    fischer(ax,3.2,2.6,[True,False,True,True],title='D-glucose • aldohexose')
    fischer(ax,8.7,2.55,[False,True,True],keto=True,title='D-fructose • cétohexose')
    arrow(ax,(4.12,4.05),(3.45,4.05),GOLD)
    text(ax,4.3,4.07,'Fonction aldéhyde\nen C1',10,INK,ha='left')
    arrow(ax,(9.7,3.7),(9.27,3.7),GOLD)
    text(ax,9.85,3.7,'Fonction cétone\nen C2',10,INK,ha='left')
    text(ax,3.2,.35,'4 centres chiraux : C2, C3, C4, C5',10.5,TEAL)
    text(ax,8.7,.35,'3 centres chiraux : C3, C4, C5',10.5,TEAL)
    save(fig,'c02_fischer')


def dl_glyceraldehyde():
    fig,ax=canvas(12,4.8,(0,12),(0,4.8))
    fischer(ax,3,2.45,[True],title='D-glycéraldéhyde',highlight_carbonyl=False)
    fischer(ax,9,2.45,[False],title='L-glycéraldéhyde',highlight_carbonyl=False)
    ax.plot([6,6],[.75,4.1],color=MUTED,lw=1.2,ls='--')
    text(ax,6,4.35,'Miroir',10.5,MUTED)
    text(ax,3,.60,'OH de référence à droite',11,TEAL,'bold')
    text(ax,9,.60,'OH de référence à gauche',11,TEAL,'bold')
    box(ax,6,2.5,2.1,1.1,'D / L', 'Configuration\n≠ signe (+)/(−)',fc=BLUE,ts=13,bs=10)
    save(fig,'c03_dl')


def counting():
    fig,ax=canvas(12,4.5,(0,12),(0,4.5))
    box(ax,3.1,3.45,5.1,1.3,'Aldose à n carbones', 'C1 et Cn non chiraux\nm = n − 2',fc=PALE,ts=13)
    box(ax,8.9,3.45,5.1,1.3,'2-cétose à n carbones', 'C1, C2 et Cn non chiraux\nm = n − 3  (n ≥ 4)',fc=BLUE,ts=13)
    box(ax,3.1,1.48,5.1,1.25,'N = 2ᵐ', 'Aldohexose : m = 4 → 16\n8 D + 8 L',fc='white',ec=LINE,ts=16)
    box(ax,8.9,1.48,5.1,1.25,'N = 2ᵐ', 'Cétohexose : m = 3 → 8\n4 D + 4 L',fc='white',ec=LINE,ts=16)
    text(ax,6,.25,'Formules valables pour les formes ouvertes des oses simples considérés ici.',10,MUTED)
    save(fig,'c04_denombrement')


def stereo_map():
    fig,ax=canvas(12,6,(0,12),(0,6))
    box(ax,6,5.35,5.4,.72,'MÊME FORMULE BRUTE',fc=BLUE,ts=13)
    arrow(ax,(4.9,4.98),(2.8,4.30)); arrow(ax,(7.1,4.98),(8.65,4.30))
    box(ax,2.8,3.7,4.65,1.1,'Isomères de constitution','Enchaînement différent\nD-glucose / D-fructose',fc=GOLD_PALE,ts=12,bs=10.5)
    box(ax,8.65,3.7,5.45,1.1,'Stéréoisomères','Même enchaînement\nConfigurations différentes',fc=PALE,ts=12,bs=10.5)
    arrow(ax,(7.4,3.1),(5.6,2.45)); arrow(ax,(9.6,3.1),(10.05,2.45))
    box(ax,5.2,1.8,4.45,1.22,'Énantiomères','Tous les centres inversés\nD-glucose / L-glucose',fc=BLUE,ts=12,bs=10.5)
    box(ax,9.9,1.8,3.7,1.22,'Diastéréoisomères','Pas des images miroir\nD-glucose / D-mannose',fc=PALE,ts=11.5,bs=9.8)
    box(ax,7.7,.43,8.6,.78,'Épimères : 1 centre inversé\nAnomères : au carbone anomérique',fc=GOLD_PALE,ts=10.3)
    arrow(ax,(9.9,1.15),(9.3,.76),GOLD)
    save(fig,'c05_stereoisomerie')


def epimers():
    fig,ax=canvas(12,5.4,(0,12),(0,5.4))
    specs=[(2.0,[True,False,True,True],'D-glucose',None),(6,[False,False,True,True],'D-mannose',2),(10,[True,False,False,True],'D-galactose',4)]
    for cx,pattern,name,c in specs:
        fischer(ax,cx,2.65,pattern,title=name,highlight_reference=False,highlight_carbonyl=False,numbers=True)
        if c:
            yy=2.65+1.45-(c-1)*.58
            ax.add_patch(FancyBboxPatch((cx-.84,yy-.23),1.68,.46,boxstyle='round,pad=0.02,rounding_size=0.06',fc='none',ec=GOLD,lw=2))
            text(ax,cx,.40,f'Épimère en C{c}',11,TEAL,'bold')
        else:
            text(ax,cx,.40,'Configuration de référence',10.5,MUTED)
    save(fig,'c06_epimers')


def cyclization():
    fig,ax=canvas(12,5.6,(0,12),(0,5.6))
    fischer(ax,1.85,2.85,[True,False,True,True],scale=.85,title='D-glucose ouvert',highlight_reference=False)
    arrow(ax,(3.15,2.95),(4.6,2.95)); text(ax,3.88,3.50,'C5–OH attaque C1',9.8,TEAL)
    text(ax,3.75,1.50,'Hémiacétal\nintramoléculaire',8.8,MUTED)
    haworth(ax,6.15,2.95,'glc','alpha',scale=.75,title='α-D-glucopyranose')
    haworth(ax,10,2.95,'glc','beta',scale=.75,title='β-D-glucopyranose')
    arrow(ax,(7.48,3.15),(8.57,3.15)); arrow(ax,(8.57,2.73),(7.48,2.73))
    text(ax,8.03,3.72,'Via la forme\nouverte',9.3,MUTED)
    box(ax,6,.52,11,.65,'Le carbone carbonyle devient un nouveau centre chiral : le carbone anomérique.',fc=GOLD_PALE,ts=10.5)
    save(fig,'c07_cyclisation')


def fischer_to_haworth():
    fig,ax=canvas(12,6,(0,12),(0,6))
    fischer(ax,2.15,2.80,[True,False,True,True],title='Fischer : D-glucose',highlight_carbonyl=False)
    for c,pat in [(2,'D → bas'),(3,'G → haut'),(4,'D → bas'),(5,'D → cycle')]:
        yy=2.80+1.45-(c-1)*.58
        text(ax,3.5,yy,pat,9.2,TEAL,ha='left')
    arrow(ax,(4.65,3.05),(5.7,3.05))
    haworth(ax,7.5,2.85,'glc','alpha',scale=.93,title='α-D-glucopyranose')
    haworth(ax,10.6,2.85,'glc','beta',scale=.78,title='β-D-glucopyranose')
    box(ax,6,5.65,11,.6,'DROITE → BAS   •   GAUCHE → HAUT   (centres conservés, orientation standard)',fc=PALE,ts=11.2)
    box(ax,6,.40,11,.65,'Pour un D-ose ainsi orienté : OH anomérique α vers le bas ; β vers le haut.',fc=GOLD_PALE,ts=11.5)
    save(fig,'c08_fischer_haworth')


def anomers_pair(sugar='glc', name='c09_anomeres_glucose'):
    fig,ax=canvas(11,4.9,(0,11),(0,4.9))
    kind='p' if sugar=='glc' else 'f'
    haworth(ax,2.8,2.75,sugar,'alpha',kind,scale=.92,title=f'α-D-{"glucopyranose" if sugar=="glc" else "fructofuranose"}')
    haworth(ax,8.2,2.75,sugar,'beta',kind,scale=.92,title=f'β-D-{"glucopyranose" if sugar=="glc" else "fructofuranose"}')
    arrow(ax,(4.7,2.9),(6.25,2.9)); arrow(ax,(6.25,2.45),(4.7,2.45))
    text(ax,5.48,3.5,'Même ose\nmême cycle',10,MUTED)
    text(ax,5.48,1.8,'Seul C'+('1' if sugar=='glc' else '2')+'\nchange',10.5,TEAL,'bold')
    save(fig,name)


def fructose_cycles():
    fig,ax=canvas(12,5.1,(0,12),(0,5.1))
    haworth(ax,2.6,2.7,'fru','beta',kind='f',scale=.93,title='β-D-fructofuranose')
    haworth(ax,6.70,2.7,'fru','beta',kind='fp',scale=.93,title='β-D-fructopyranose')
    box(ax,10.45,2.8,2.6,2.5,'Même fructose', 'Furane : 5 atomes\nC2 + C3 + C4 + C5 + O\n\nPyrane : 6 atomes\nC2 à C6 + O',fc=PALE,ts=11.5,bs=9.5)
    text(ax,6,.33,'Furanose / pyranose = taille du cycle ; α / β = configuration anomérique.',11,TEAL)
    save(fig,'c10_fructose_cycles')


def disaccharide(which, name=None):
    fig,ax=canvas(12,5.3,(0,12),(0,5.3))
    cy=2.95
    if which=='saccharose':
        p=haworth(ax,2.7,cy,'glc','alpha',scale=.90,link='donor',show_title=False)
        q=haworth(ax,8.0,cy+.12,'fru','beta',kind='f',scale=.90,rotate=True,link='donor',show_title=False)
        a,b=p[1],q[2]
        yy=cy-.44
        path=[a,(a[0]+.40,yy),(b[0]-.42,yy),b]
        ax.plot(*zip(*path),color=NAVY,lw=1.8,zorder=3)
        ox=(a[0]+b[0])/2
        text(ax,ox,yy,'O',12,RED,bbox=dict(fc='white',ec='none',pad=1.8),zorder=6)
        text(ax,ox,cy+.46,'α(1↔2)β',12,TEAL,'bold')
        text(ax,2.7,.49,'α-D-glucopyranosyl',11,NAVY,'bold')
        text(ax,8.0,.49,'β-D-fructofuranoside',11,NAVY,'bold')
        text(ax,6,5.03,'SACCHAROSE • les deux carbones anomériques sont engagés',12,NAVY,'bold')
        text(ax,10.8,1.0,'Cycle fructose\ntourné de 180°\ndans le plan',8.8,MUTED)
    else:
        donor='gal' if which=='lactose' else 'glc'
        alpha=which=='maltose'
        p=haworth(ax,2.65,cy,donor,'alpha' if alpha else 'beta',scale=.88,link='donor',show_title=False)
        q=haworth(ax,8.55,cy,'glc','beta' if which=='lactose' else 'alpha',scale=.88,link='acceptor4',show_title=False,free_color=GREEN)
        a,b=p[1],q[4]
        yy=cy+(-.40 if alpha else .40)
        path=[a,(a[0]+.38,yy),(b[0]-.38,yy),b]
        ax.plot(*zip(*path),color=NAVY,lw=1.8,zorder=3)
        ox=(a[0]+b[0])/2
        text(ax,ox,yy,'O',12,RED,bbox=dict(fc='white',ec='none',pad=1.8),zorder=6)
        text(ax,ox,cy+(-.88 if alpha else .90),'α(1→4)' if alpha else 'β(1→4)',11.5,TEAL,'bold')
        text(ax,2.65,.49,'β-D-galactopyranosyl' if donor=='gal' else 'α-D-glucopyranosyl',10.7,NAVY,'bold')
        text(ax,8.55,.49,'β-D-glucopyranose' if which=='lactose' else 'α-D-glucopyranose',10.7,NAVY,'bold')
        title='β-LACTOSE' if which=='lactose' else 'α-MALTOSE'
        text(ax,6,5.03,title+' • une extrémité anomérique reste libre',12,NAVY,'bold')
        arrow(ax,(10.8,1.48),(9.78,2.77),GREEN,lw=1.4)
        text(ax,10.82,1.10,'C1 libre\nréducteur',9.7,GREEN,'bold')
    save(fig,name or f'c11_{which}')


def reducing_flow():
    fig,ax=canvas(12,5.7,(0,12),(0,5.7))
    box(ax,6,4.98,7.8,.77,'Un carbone anomérique est-il encore hémiacétal / hémicétal ?',fc=BLUE,ts=12)
    arrow(ax,(4.1,4.58),(2.85,3.85),GREEN); arrow(ax,(7.9,4.58),(9.2,3.85),RED)
    text(ax,3.15,4.35,'OUI',10,GREEN,'bold');text(ax,8.8,4.35,'NON',10,RED,'bold')
    box(ax,2.85,3.1,4.9,1.3,'Ouverture du cycle possible','Forme carbonyle accessible\n→ sucre réducteur',fc=PALE,ts=12)
    box(ax,9.15,3.1,4.9,1.3,'Anomères bloqués','Pas d’ouverture directe\n→ non réducteur',fc='#F9ECE9',ts=12)
    box(ax,2.85,1.15,4.9,1.18,'Glucose • fructose libres','Lactose • maltose\nMutarotation possible',fc='white',ec=LINE,ts=11.5,bs=10.5)
    box(ax,9.15,1.15,4.9,1.18,'Saccharose','Deux centres anomériques\ntransformés en acétal/cétal',fc='white',ec=LINE,ts=11.5,bs=10.5)
    text(ax,6,.15,'Les cétones libres réagissent aussi aux tests alcalins après isomérisation en aldoses.',10,MUTED)
    save(fig,'c12_reducteur')


def glycosidic_formation():
    fig,ax=canvas(12,3.8,(0,12),(0,3.8))
    box(ax,2.1,2.45,3.5,1.4,'OH anomérique','D’un ose cyclisé\n(rôle du donneur)',fc=GOLD_PALE,ts=12)
    box(ax,6.0,2.45,3.0,1.4,'HO–R','Autre OH accepteur\nanomérique ou non',fc=PALE,ts=12)
    text(ax,4.03,2.45,'+',20,MUTED)
    arrow(ax,(7.64,2.45),(8.62,2.45))
    box(ax,10.13,2.45,2.8,1.4,'Ose–O–R','Liaison osidique',fc=BLUE,ts=12)
    text(ax,8.1,1.92,'− H₂O',10.5,TEAL)
    box(ax,6,.65,10.9,.8,'Bilan formel de condensation — en cellule : donneurs activés et enzymes spécifiques.',fc='white',ec=LINE,ts=11)
    save(fig,'c13_liaison')


def exercise_source():
    fig,ax=canvas(11,5.2,(0,11),(0,5.2))
    fischer(ax,2.8,2.6,[True,False,True,True],title='A • D-glucose')
    fischer(ax,8.2,2.55,[False,True,True],keto=True,title='B • D-fructose')
    text(ax,2.8,.30,'Droite / gauche : D – G – D – D',10.5,TEAL)
    text(ax,8.2,.30,'Droite / gauche : G – D – D',10.5,TEAL)
    save(fig,'x01_identification')


def enantiomers_glucose():
    fig,ax=canvas(11,5.2,(0,11),(0,5.2))
    fischer(ax,2.8,2.6,[True,False,True,True],title='D-glucose')
    fischer(ax,8.2,2.6,[False,True,False,False],title='L-glucose')
    ax.plot([5.5,5.5],[.75,4.35],ls='--',color=MUTED,lw=1.2)
    text(ax,5.5,4.6,'Miroir',10.5,MUTED)
    text(ax,5.5,.35,'Les QUATRE centres chiraux sont inversés : ce sont des énantiomères.',11,TEAL)
    save(fig,'x02_enantiomere')


def decision_tree():
    fig,ax=canvas(12,5.5,(0,12),(0,5.5))
    box(ax,6,4.85,7.4,.7,'Comparer d’abord la formule brute et la connectivité',fc=BLUE,ts=12)
    arrow(ax,(6,4.48),(6,4.05))
    box(ax,6,3.55,7.4,.7,'Même constitution ? Si non : isomères de constitution',fc=GOLD_PALE,ts=11.5)
    arrow(ax,(6,3.16),(6,2.76))
    box(ax,6,2.27,7.4,.7,'Images miroir non superposables ? Si oui : énantiomères',fc=PALE,ts=11.5)
    arrow(ax,(6,1.9),(6,1.5))
    box(ax,6,1.0,8.8,.75,'Sinon : diastéréoisomères → un seul centre inversé ? épimères',fc=BLUE,ts=11.5)
    text(ax,6,.19,'Anomères = épimères appartenant à des formes cycliques, au seul carbone anomérique.',10.5,TEAL)
    save(fig,'x03_decision')


def rotation_fructose():
    fig,ax=canvas(11,4.9,(0,11),(0,4.9))
    haworth(ax,2.7,2.65,'fru','beta',kind='f',scale=.91,title='Orientation standard')
    haworth(ax,8.2,2.65,'fru','beta',kind='f',scale=.91,rotate=True,title='Rotation de 180° dans le plan')
    arrow(ax,(4.7,2.8),(6.2,2.8));text(ax,5.45,3.35,'Même\nmolécule',10.5,TEAL)
    text(ax,5.5,.2,'La rotation échange haut et bas : elle ne change pas la configuration β.',10.5,MUTED)
    save(fig,'x04_rotation')


def requested_rings():
    fig,ax=canvas(11,4.9,(0,11),(0,4.9))
    haworth(ax,2.75,2.7,'glc','alpha',scale=.96,title='α-D-glucopyranose')
    haworth(ax,8.2,2.7,'fru','beta',kind='f',scale=.96,title='β-D-fructofuranose')
    text(ax,5.5,3.0,'Aldose A\nC1 anomérique',10.5,TEAL)
    text(ax,5.5,2.25,'Cétose B\nC2 anomérique',10.5,TEAL)
    text(ax,5.5,.30,'Les hydrogènes portés par les carbones sont implicites ; les carbones sont numérotés.',10,MUTED)
    save(fig,'x05_cycles_demandes')


def make_all():
    classification(); cover(); linear_oses(); dl_glyceraldehyde(); counting(); stereo_map(); epimers()
    cyclization(); fischer_to_haworth(); anomers_pair(); anomers_pair('fru','c09b_anomeres_fructose')
    fructose_cycles(); disaccharide('saccharose'); disaccharide('lactose'); disaccharide('maltose')
    reducing_flow(); glycosidic_formation(); exercise_source(); enantiomers_glucose(); decision_tree(); rotation_fructose(); requested_rings()

if __name__ == '__main__':
    make_all()
