from pylatex import Document, Section, Subsection, Command,Package
from pylatex.utils import italic, NoEscape


def pronunciation_adjust(string):
    adjust_list=[["$",r"\$"] ,
                 ['ə',r'\textipa{@}'],
                 ['ˈ',r'\textprimstress '],
                 ["'",r'\textprimstress '],
                 #['ˈ'r,'\textipa{"}'],
                 ['ˌ',r'\textipa{""}'],
                 ['ʃ',r'\textipa{S}'],
                 ['ɪ',r'\textipa{I}'],
                 ['ː',r'\textipa{:}'],
                 ['ɜ',r'\textipa{3}'],
                 ['ʊ',r'\textipa{U}'],
                 ['ɒ',r'\textipa{6}'],
                 ['ɑ',r'\textipa{A}'],
                 ['ɔ',r'\textipa{0}'],
                 #['ɔ',r'\textopeno '],
                 ['ʌ',r'\textipa{2}'],
                 ['ɡ',r'\textipa{g}'],
                 ['ʒ',r'\textipa{Z}'],
                 ['ŋ',r'\textipa{N}'],
                 ['ð',r'\textipa{D}'],
                 ['ʊ',r'\textipa{U}'],
                 ['θ',r'\textipa{T}'],
                 ['æ',r'\ae '],
                 ['  ',' ']
                ]
    for ad in adjust_list:
        string=string.replace(ad[0],ad[1])
    return string


def latex_init(title): 
    doc=Document(title,documentclass='ctexart')
    
    doc.preamble.append(Package('tipa'))
    doc.preamble.append(Package('xcolor'))
    doc.preamble.append(Package('enumitem'))
    doc.preamble.append(Package('tcolorbox'))
    doc.preamble.append(Package('geometry','left=1.25in,right=1.25in,top=1in,bottom=1in'))
    
    doc.preamble.append(Command('tcbuselibrary','breakable'))
    doc.preamble.append(Command('tcbuselibrary','skins'))
    doc.preamble.append(Command('setdescription',NoEscape(r'itemsep=0pt,partopsep=0pt,parsep=\parskip,topsep=1pt')))
    doc.append(Command('subsection*',title))
    return doc

def add_word(doc,word,):
    doc.append(NoEscape(r'\noindent\begin{tcolorbox}[breakable,enhanced jigsaw]'))
    doc.append(Command('paragraph',word.spelling))
    if word.rank:
        doc.append("{}".format(word.rank))
    for key,value in word.pronunciations.items():
        doc.append(NoEscape("{}:{}".format(key,pronunciation_adjust(value))))
    
    if len(word.explanations)==1:
        doc.append(NoEscape(r"\par\noindent {}".format(word.explanations[0].latex)))
    else:
        for order,explanation in enumerate(word.explanations):
            doc.append(NoEscape(r"\par\noindent {0}.{1}".format(order+1,explanation.latex)))
    
    doc.append(NoEscape("\end{tcolorbox}\n"))
#word=Word('usage')
#add_word(word)

