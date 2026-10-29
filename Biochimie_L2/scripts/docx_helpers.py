"""Helpers de mise en page Word, fondés exclusivement sur python-docx."""
from pathlib import Path
from datetime import datetime, timezone
from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_TAB_ALIGNMENT
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.opc.constants import RELATIONSHIP_TYPE as RT

ROOT = Path(__file__).resolve().parents[1]
FIGS = ROOT / 'illustrations'
DOCS = ROOT / 'documents'
DOCS.mkdir(parents=True, exist_ok=True)
NAVY='17324D'; TEAL='137C7A'; INK='243746'; MUTED='627582'; PALE='EAF5F3'
BLUE='EAF0F8'; GOLD='D69A36'; GOLD_PALE='FFF4DE'; LINE='D7E3E7'; RED='AC4545'; GREEN='2C795C'
FONT='Calibri'


def rgb(s): return RGBColor.from_string(s)


def xml(tag, **attrs):
    e=OxmlElement(tag)
    for k,v in attrs.items(): e.set(qn(k),str(v))
    return e


def shade(cell, color):
    tcPr=cell._tc.get_or_add_tcPr()
    old=tcPr.find(qn('w:shd'))
    if old is not None: tcPr.remove(old)
    tcPr.append(xml('w:shd', **{'w:fill':color,'w:val':'clear'}))


def cell_margins(cell, top=90, start=115, bottom=90, end=115):
    pr=cell._tc.get_or_add_tcPr()
    m=xml('w:tcMar')
    for tag,v in [('top',top),('start',start),('bottom',bottom),('end',end)]:
        m.append(xml('w:'+tag,**{'w:w':v,'w:type':'dxa'}))
    pr.append(m)


def borders(cell, **edges):
    pr=cell._tc.get_or_add_tcPr(); b=pr.find(qn('w:tcBorders'))
    if b is None: b=xml('w:tcBorders');pr.append(b)
    for edge,spec in edges.items():
        old=b.find(qn('w:'+edge))
        if old is not None: b.remove(old)
        b.append(xml('w:'+edge,**{'w:val':spec.get('val','single'),'w:sz':spec.get('sz',6),'w:color':spec.get('color',LINE)}))


def no_split(row):
    pr=row._tr.get_or_add_trPr();pr.append(xml('w:cantSplit'))


def repeat_header(row):
    row._tr.get_or_add_trPr().append(xml('w:tblHeader'))


def field(paragraph, instruction, cached='1'):
    run=paragraph.add_run()
    run._r.append(xml('w:fldChar',**{'w:fldCharType':'begin'}))
    instr=OxmlElement('w:instrText');instr.set(qn('xml:space'),'preserve');instr.text=' '+instruction+' '
    run._r.append(instr)
    run._r.append(xml('w:fldChar',**{'w:fldCharType':'separate'}))
    t=OxmlElement('w:t');t.text=cached;run._r.append(t)
    run._r.append(xml('w:fldChar',**{'w:fldCharType':'end'}))
    return run


def bookmark(paragraph, name, bid):
    start=xml('w:bookmarkStart',**{'w:id':bid,'w:name':name})
    end=xml('w:bookmarkEnd',**{'w:id':bid})
    paragraph._p.insert(0,start);paragraph._p.append(end)


def internal_link(paragraph, text, anchor, size=10.5, bold=False, color=TEAL):
    h=OxmlElement('w:hyperlink');h.set(qn('w:anchor'),anchor);h.set(qn('w:history'),'1')
    r=OxmlElement('w:r');pr=OxmlElement('w:rPr')
    pr.append(xml('w:rFonts',**{'w:ascii':FONT,'w:hAnsi':FONT}))
    pr.append(xml('w:color',**{'w:val':color}))
    pr.append(xml('w:sz',**{'w:val':int(size*2)}))
    if bold:pr.append(xml('w:b'))
    r.append(pr);t=OxmlElement('w:t');t.text=text;r.append(t);h.append(r);paragraph._p.append(h)


class Builder:
    def __init__(self, kind='Cours'):
        self.doc=Document();self.kind=kind;self.fig_no=0;self.table_no=0;self.page_no=1;self.bid=10;self.sections=[]
        d=self.doc
        sec=d.sections[0]
        sec.page_width=Cm(21);sec.page_height=Cm(29.7)
        sec.top_margin=Cm(2.05);sec.bottom_margin=Cm(1.8);sec.left_margin=Cm(2);sec.right_margin=Cm(2)
        sec.header_distance=Cm(.85);sec.footer_distance=Cm(.85)
        sec.different_first_page_header_footer=True
        self.width=17.0
        self._styles()
        self._fix_bullets()
        self._header_footer()
        props=d.core_properties
        props.title=('Cours — La structure des glucides' if kind=='Cours' else 'Corrigé détaillé — TD 1 de biochimie structurale')
        props.subject='SNV L2 — Biochimie structurale — La structure des glucides'
        props.author='Support pédagogique L2 SNV'
        props.keywords='glucides, Fischer, Haworth, stéréoisomérie, anomères, liaisons osidiques, L2'
        props.comments='Document pédagogique original élaboré à partir du TD fourni. Figures scientifiques vectorielles rasterisées et générées par Python.'
        props.category='Enseignement supérieur — Licence 2'
        props.created=datetime(2026,10,29, tzinfo=timezone.utc)
        props.modified=props.created
        settings=d.settings.element
        settings.append(xml('w:updateFields',**{'w:val':'true'}))
        settings.append(xml('w:doNotHyphenateCaps'))
        # Langue française par défaut, y compris pour les textes nouvellement saisis.
        defaults=d.styles.element.find(qn('w:docDefaults'))
        if defaults is not None:
            rpr=defaults.find(qn('w:rPrDefault'))
            if rpr is not None:
                rp=rpr.find(qn('w:rPr'))
                if rp is not None:rp.append(xml('w:lang',**{'w:val':'fr-FR'}))

    def _styles(self):
        d=self.doc
        specs=[('Normal',11,INK,False,0,6,1.12),('Title',32,NAVY,True,0,12,1.03),
               ('Subtitle',15,TEAL,False,0,8,1.12),('Heading 1',18,NAVY,True,0,10,1.08),
               ('Heading 2',12.5,TEAL,True,9,4,1.08),('Heading 3',11,NAVY,True,7,3,1.08),
               ('Caption',9,MUTED,False,4,8,1.05),('Small',9,MUTED,False,0,4,1.08),
               ('Table Text',10,INK,False,0,2,1.06),('Callout',10.5,INK,False,0,3,1.10),
               ('Equation',13,NAVY,True,5,7,1.10),('Kicker',10,TEAL,True,0,8,1.08)]
        for name,size,color,bold,before,after,spacing in specs:
            if name not in d.styles: d.styles.add_style(name,WD_STYLE_TYPE.PARAGRAPH)
            st=d.styles[name];st.font.name=FONT;st.font.size=Pt(size);st.font.color.rgb=rgb(color);st.font.bold=bold
            pf=st.paragraph_format;pf.space_before=Pt(before);pf.space_after=Pt(after);pf.line_spacing=spacing
            pf.widow_control=True
            if name.startswith('Heading'):pf.keep_with_next=True;pf.keep_together=True
            if name=='Caption':st.font.italic=True;pf.keep_together=True
            if name=='Equation':pf.alignment=WD_ALIGN_PARAGRAPH.CENTER
            if name=='Subtitle':st.font.italic=False
            if name=='Kicker':pf.keep_with_next=True
            rpr=st.element.get_or_add_rPr();rpr.append(xml('w:lang',**{'w:val':'fr-FR'}))
        for name in ['List Bullet','List Number']:
            st=d.styles[name];st.font.name=FONT;st.font.size=Pt(11);st.font.color.rgb=rgb(INK)
            pf=st.paragraph_format;pf.space_after=Pt(4);pf.line_spacing=1.10;pf.left_indent=Cm(.5);pf.first_line_indent=Cm(-.25)
        # Évite le thème bleu par défaut dans les titres et les liens.
        for stname in ['Title','Subtitle','Heading 1','Heading 2','Heading 3']:
            st=d.styles[stname]
            st.element.get_or_add_rPr().append(xml('w:lang',**{'w:val':'fr-FR'}))

    def _fix_bullets(self):
        # Utiliser un vrai point Unicode dans Calibri plutôt que Symbol,
        # afin de conserver le même glyphe dans Word et les autres moteurs.
        style=self.doc.styles['List Bullet']
        numpr=style.element.get_or_add_pPr().find(qn('w:numPr'))
        if numpr is None:return
        numid_el=numpr.find(qn('w:numId'))
        if numid_el is None:return
        numid=numid_el.get(qn('w:val'))
        numbering=self.doc.part.numbering_part.element
        num=numbering.find(qn('w:num')+f'[@{qn("w:numId")}="{numid}"]')
        if num is None:return
        aid=num.find(qn('w:abstractNumId')).get(qn('w:val'))
        abstract=numbering.find(qn('w:abstractNum')+f'[@{qn("w:abstractNumId")}="{aid}"]')
        if abstract is None:return
        lvl=abstract.find(qn('w:lvl'))
        if lvl is None:return
        lvl.find(qn('w:lvlText')).set(qn('w:val'),'•')
        rpr=lvl.find(qn('w:rPr'))
        if rpr is None:rpr=xml('w:rPr');lvl.append(rpr)
        fonts=rpr.find(qn('w:rFonts'))
        if fonts is None:fonts=xml('w:rFonts');rpr.append(fonts)
        for attr in ['w:ascii','w:hAnsi','w:cs']:fonts.set(qn(attr),FONT)

    def _header_footer(self):
        sec=self.doc.sections[0]
        p=sec.header.paragraphs[0];p.paragraph_format.tab_stops.add_tab_stop(Cm(17),WD_TAB_ALIGNMENT.RIGHT)
        p.paragraph_format.space_after=Pt(5)
        r=p.add_run('BIOCHIMIE STRUCTURALE  /  L2 SNV');r.font.size=Pt(8.5);r.font.bold=True;r.font.color.rgb=rgb(MUTED)
        r=p.add_run('\t'+self.kind.upper()+' • TD 1');r.font.size=Pt(8.5);r.font.bold=True;r.font.color.rgb=rgb(TEAL)
        pr=p._p.get_or_add_pPr();b=xml('w:pBdr');b.append(xml('w:bottom',**{'w:val':'single','w:sz':'8','w:color':TEAL,'w:space':'6'}));pr.append(b)
        p=sec.footer.paragraphs[0];p.paragraph_format.tab_stops.add_tab_stop(Cm(17),WD_TAB_ALIGNMENT.RIGHT)
        r=p.add_run('La structure des glucides • 2026 / 2027');r.font.size=Pt(8);r.font.color.rgb=rgb(MUTED)
        r=p.add_run('\t');r.font.size=Pt(8)
        r=p.add_run('Page ');r.font.size=Pt(8);r.font.color.rgb=rgb(MUTED)
        field(p,'PAGE','1').font.size=Pt(8)
        r=p.add_run(' / ');r.font.size=Pt(8);r.font.color.rgb=rgb(MUTED)
        r=field(p,'NUMPAGES','1');r.font.size=Pt(8);r.font.color.rgb=rgb(MUTED)
        # Couverture sans en-tête ni pied de page.
        for area in [sec.first_page_header,sec.first_page_footer]:
            area.paragraphs[0].text=''

    def p(self,text='',style=None,bold=False,color=None,size=None,align=None,after=None,before=None):
        p=self.doc.add_paragraph(style=style)
        if text:
            r=p.add_run(text)
            if bold:r.bold=True
            if color:r.font.color.rgb=rgb(color)
            if size:r.font.size=Pt(size)
        if align is not None:p.alignment=align
        if after is not None:p.paragraph_format.space_after=Pt(after)
        if before is not None:p.paragraph_format.space_before=Pt(before)
        return p

    def rich(self,parts,style=None,after=None):
        p=self.doc.add_paragraph(style=style)
        for item in parts:
            if isinstance(item,str):p.add_run(item)
            else:
                s=item[0];spec=item[1] if len(item)>1 else {}
                r=p.add_run(s);r.bold=spec.get('bold',False);r.italic=spec.get('italic',False)
                if 'color' in spec:r.font.color.rgb=rgb(spec['color'])
                if 'size' in spec:r.font.size=Pt(spec['size'])
        if after is not None:p.paragraph_format.space_after=Pt(after)
        return p

    def bullets(self,items,style='List Bullet'):
        for item in items:self.p(item,style)

    def h1(self,text,anchor=None):
        p=self.p(text,'Heading 1')
        if anchor:self.mark(p,anchor)
        return p

    def h2(self,text):return self.p(text,'Heading 2')
    def h3(self,text):return self.p(text,'Heading 3')

    def mark(self,p,anchor):
        bookmark(p,anchor,self.bid);self.bid+=1

    def new_page(self,kicker=None,title=None,anchor=None):
        self.page_no+=1
        if kicker:
            p=self.p(kicker,'Kicker');p.paragraph_format.page_break_before=True
        if title:
            p=self.h1(title,anchor)
            if not kicker:p.paragraph_format.page_break_before=True

    def cover(self,title,subtitle,descriptor,audience,fig='c00_couverture.png'):
        self.p('SNV  •  LICENCE 2  •  2026 / 2027','Kicker',before=22)
        self.p('BIOCHIMIE\nSTRUCTURALE','Title',size=34,after=16)
        self.p(self.kind.upper(),'Kicker',size=12,after=12)
        self.p(title,'Subtitle',size=24,color=NAVY,bold=True,after=10)
        self.p(subtitle,'Subtitle',size=13,after=16)
        self.figure(fig,width=17,caption=None)
        self.p(descriptor,after=12,size=11)
        self.callout(audience,title='Repère pédagogique',tone='blue')
        self.p('Support original construit à partir du TD n°1 fourni.\nMise en page et figures générées avec Python.','Small',before=12)

    def figure(self,name,width=16.6,caption=None):
        p=self.doc.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before=Pt(3);p.paragraph_format.space_after=Pt(1);p.paragraph_format.keep_with_next=True
        p.add_run().add_picture(str(FIGS/name),width=Cm(width))
        if caption:
            self.fig_no+=1
            self.p(f'Figure {self.fig_no}. {caption}','Caption',align=WD_ALIGN_PARAGRAPH.CENTER)
        return p

    def callout(self,text,title='À retenir',tone='teal'):
        palette={'teal':(PALE,TEAL),'blue':(BLUE,NAVY),'gold':(GOLD_PALE,GOLD),'red':('F9ECE9',RED)}
        bg,accent=palette[tone]
        t=self.doc.add_table(rows=1,cols=1);t.alignment=WD_TABLE_ALIGNMENT.CENTER;t.autofit=False;t.columns[0].width=Cm(17)
        c=t.cell(0,0);c.width=Cm(17);shade(c,bg);cell_margins(c,120,160,120,160)
        borders(c,left={'sz':20,'color':accent},top={'val':'nil'},bottom={'val':'nil'},right={'val':'nil'})
        no_split(t.rows[0])
        p=c.paragraphs[0];p.style=self.doc.styles['Callout'];r=p.add_run(title.upper());r.bold=True;r.font.size=Pt(9);r.font.color.rgb=rgb(accent)
        p=c.add_paragraph(text,style='Callout');p.paragraph_format.space_after=Pt(0)
        self.p('',after=1,size=2)
        return t

    def table(self,headers,rows,widths=None,font=10,caption=None):
        if caption:
            self.table_no+=1;self.p(f'Tableau {self.table_no}. {caption}','Caption',align=WD_ALIGN_PARAGRAPH.LEFT)
        ncols=len(headers)
        widths=widths or [17/ncols]*ncols
        t=self.doc.add_table(rows=1,cols=ncols);t.alignment=WD_TABLE_ALIGNMENT.CENTER;t.autofit=False
        # Fixer aussi la largeur totale dans le XML pour Word et LibreOffice.
        pr=t._tbl.tblPr;tw=pr.find(qn('w:tblW'))
        if tw is not None:tw.set(qn('w:w'),str(int(sum(widths)*567)));tw.set(qn('w:type'),'dxa')
        for i,(c,w) in enumerate(zip(t.columns,widths)):c.width=Cm(w)
        for i,h in enumerate(headers):
            c=t.rows[0].cells[i];c.width=Cm(widths[i]);shade(c,NAVY);cell_margins(c,100,115,100,115)
            c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
            p=c.paragraphs[0];p.style=self.doc.styles['Table Text'];p.paragraph_format.keep_with_next=True
            r=p.add_run(h);r.bold=True;r.font.color.rgb=rgb('FFFFFF');r.font.size=Pt(font)
        repeat_header(t.rows[0]);no_split(t.rows[0])
        for ri,row in enumerate(rows):
            cells=t.add_row().cells
            for i,val in enumerate(row):
                c=cells[i];c.width=Cm(widths[i]);shade(c,'F4F8F9' if ri%2==0 else 'FFFFFF');cell_margins(c)
                borders(c,bottom={'sz':4,'color':LINE})
                c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
                p=c.paragraphs[0];p.style=self.doc.styles['Table Text']
                # Un retour à la ligne manuel reste dans une cellule lisible.
                r=p.add_run(str(val));r.font.size=Pt(font)
                if i==0:r.bold=True;r.font.color.rgb=rgb(NAVY)
            no_split(t.rows[-1])
        self.p('',after=1,size=2)
        return t

    def equation(self,text):return self.p(text,'Equation')

    def question(self,num,title,answer=None):
        p=self.h2(f'{num}. {title}')
        if answer:self.rich([('Réponse. ',{'bold':True,'color':TEAL}),answer])
        return p

    def save(self,filename):
        path=DOCS/filename;self.doc.save(path)
        return path
