import urllib.request
from lxml import etree
import lxml.html as lh
import html as ht

class Entry():
    def __init__(self,spelling):
        self.spelling=spelling
        self._get_page()
        self._get_explanations()
        self.latex()
    def _get_page(self):
        searchurl=f'https://dict.youdao.com/w/{self.spelling.replace(" ","%20")}/#keyfrom=dict2.top'  
        response =  urllib.request.urlopen(searchurl)  
        html = response.read()
        self.selector = etree.HTML(html.decode('utf-8'))
    def _get_explanations(self):
        xpath=""
        self.explanation=self.selector.xpath(xpath)

        
class Word():
    def __init__(self,word):
        
        self.spelling=word
        self._get_page()
        self._get_spelling()
        self._get_pronunciation()
        self._get_rank()
        self._get_explanations()

    def _get_page(self):
        searchurl='https://dict.youdao.com/w/eng/'+self.spelling+'/'
        response =  urllib.request.urlopen(searchurl)  
        html = response.read()
        self.selector = etree.HTML(html.decode('utf-8'))
        
    def _get_spelling(self):
        spelling_xpath="//h4/span[@class='title']/text()"
        self.spelling_found=self.selector.xpath(spelling_xpath)
        
        if self.spelling_found:
            self.spelling_found=self.spelling_found[0]
            if self.spelling_found==self.spelling:
                pass
            else:
                print("'{}' is not found, but {} is found"\
                         .format(self.spelling,self.spelling_found))
                self.spelling=self.spelling_found
        else:
            print("***'{}' is not found. It may be an odd word***".format(self.spelling))
        
    def _get_pronunciation(self):
        labels_xpath="//span[@class='pronounce']"
        phonetics_xpath="//h2/div/span/span[@class='phonetic']/text()"
        heads=self.selector.xpath(labels_xpath)
        heads=[head.text.replace(" ","").replace("\n","") for head in heads]
        phonetics=self.selector.xpath(phonetics_xpath)
        self.pronunciations=dict(zip(heads,phonetics))
        
    def _get_rank(self):
        rank_xpath="//span[@class='via rank']/text()"
        try:
            self.rank=self.selector.xpath(rank_xpath)[0]
        except:
            self.rank=""
            print("The rank of '{}' is not found, so this may be a difficult word."\
                  .format(self.spelling))
            
    def _get_explanations(self):
        collins_xpath="//div[@class='collinsMajorTrans']"
        get_collins=self.selector.xpath(collins_xpath)
        number=len(get_collins)
        if number:
            self.explanations=[""]*number
            for order in range(number):
                self.explanations[order]=self._get_explanation(order)
        else:#No collins translations
            explanation_xpath="(//div[@class='trans-container'])[1]/ul/li/text()"
            explanation=self.selector.xpath(explanation_xpath)
            if explanation:
                explanation=Explanation(explanation[0],())
            else:
                explanation=Explanation(" ",())
            self.explanations=[explanation]
        
    def _get_explanation(self,index):      
        collins_meaning_xpath=f"(//div[@class='collinsMajorTrans'])[{index+1}]/p"
        collins_meaning_xpath2=f"(//div[@class='collinsMajorTrans'])[{index+1}]/p/a/text()"
        collins_additional_xpath=f"(//div[@class='collinsMajorTrans'])[{index+1}]/p/span"
        collins_example_EN_xpath=f"(//div[@class='collinsMajorTrans'])[{index+1}]/../div/div/p[1]/text()"
        collins_example_CN_xpath=f"(//div[@class='collinsMajorTrans'])[{index+1}]/../div/div/p[2]/text()"
        
        collins_meaning_xpath=f"(//div[@class='collinsMajorTrans'])[{index+1}]/p"
        collins_additional_xpath=f"(//div[@class='collinsMajorTrans'])[{index+1}]/p/span"
        collins_example_EN_xpath=f"(//div[@class='collinsMajorTrans'])[{index+1}]/../div/div/p[1]/text()"
        collins_example_CN_xpath=f"(//div[@class='collinsMajorTrans'])[{index+1}]/../div/div/p[2]/text()"
        
        additional=self.selector.xpath(collins_additional_xpath)
        translation_special=self.selector.xpath(collins_meaning_xpath2)# in case which have symbol →
        if additional:
            additional=additional[0].text
        else:#There is no additional of this explanation, it may be an odd one.
            additional="\t"
            
        translation=self.selector.xpath(collins_meaning_xpath)
        translation=trans_adjust(ht.unescape(\
                    lh.tostring(translation[0]).decode()),additional,translation_special)
            
        examples_CN=self.selector.xpath(collins_example_CN_xpath)
        examples_EN=self.selector.xpath(collins_example_EN_xpath)
        examples=tuple(zip(examples_EN,examples_CN))
        return Explanation(translation,examples)
       
class Not_word(Entry):
    def __init__(self,spelling):
        super().__init__(spelling)
        self._get_page()
        self._get_spelling()
    def _get_page(self):
        searchurl=f'https://dict.youdao.com/w/{self.spelling.replace(" ","%20")}/#keyfrom=dict2.top'  
        response =  urllib.request.urlopen(searchurl)  
        html = response.read()
        self.selector = etree.HTML(html.decode('utf-8'))
    def _get_spelling(self):
        spelling_xpath="//h4/span[@class='title']/text()"
        self.spelling=self.selector.xpath(spelling_xpath)[0]
    def _get_explanations():
        pass

class Explanation():
    def __init__(self,trans,examples):
        self.trans=trans
        self.examples=examples
        self._get_latex()
    def _get_latex(self):
        self.latex=self.trans
        if self.examples:
            self.latex+="\n\\begin{description}"
            for example in self.examples:
                self.latex+="\n\\item"+"[eg.]"+" {} {}".format(example[0],example[1])
            self.latex+="\n\\end{description}"
            
def trans_adjust(trans,addi,specials):
    replace_dict={
    'N':'<span class="additional" title="名词">N</span>',\
    'N-COUNT':'<span class="additional" title="可数名词">N-COUNT</span>',\
    'N-UNCOUNT':'<span class="additional" title="不可数名词">N-UNCOUNT</span>',\
    'N-VAR':'<span class="additional" title="有变体名词">N-VAR</span>',\
    'N-SING':'<span class="additional" title="单数型名词">N-SING</span>',\
    'N-SING-COLL':'<span class="additional" title="单数型集体名词">N-SING-COLL</span>',\
    'N-PLURAL':'<span class="additional" title="复数型名词">N-PLURAL</span>',\
    'N-IN-NAMES':'<span class="additional" title="名称内的名词">N-IN-NAMES</span>',\
    'N-MASS':'<span class="additional" title="物质名词">N-MASS</span>',\
        
        
    'V':'<span class="additional" title="动词">V</span>',\
    'V-T':'<span class="additional" title="及物动词">V-T</span>',\
    'V-I':'<span class="additional" title="不及物动词">V-I</span>',\
    'V-T/V-I':'<span class="additional" title="及物动词/不及物动词">V-T/V-I</span>',\
    'V-T PASSIVE':'<span class="additional" title="及物动词被动">V-T PASSIVE</span>',\
    'V-RECIP':'<span class="additional" title="及物动词被动">V-RECIP</span>',\
    
    'ADJ':'<span class="additional" title="形容词">ADJ</span>',\
    'ADV':'<span class="additional" title="副词">ADV</span>',\
        
    'COMB in ADJ':'<span class="additional" title="与形容词结合的复合词">COMB in ADJ</span>',\
    'COMB in COLOR':'<span class="additional" title="与颜色结合的复合词">COMB in COLOR</span>',\
        
    'PHRASE':'<span class="additional" title="习语">PHRASE</span>',\
    'PHRASAL VERB':'<span class="additional" title="动词词组">PHRASAL VERB</span>',\
        
    'the INTERNET DOMAIN NAME for':'<span class="additional">the INTERNET DOMAIN NAME for</span>',\
    '\t':'\t'}
    replace_list=["\t","\n","  ","   ","<b>","</b>","<p>","</p>","</a>",\
                  '<span class="additional">','</span>'] 
    trans=trans.replace(replace_dict[addi],addi+" ")
    for rep in replace_list:
        trans=trans.replace(rep,"")
    if specials:
        print(f"special meaning: # {specials} #")
        for special in specials:
            special=special.replace(" ","%20")
            string=f'<a style="text-decoration: none;" class="search-js" href="/w/{special}/?keyfrom=dict.collins" target="_blank">'
            trans=trans.replace(string," ").replace("→"," → ")
    return trans


def symbol_adjust(string):
    adjust_list=[["&","\\&"] ,
                ["%","\\%"] ,                 
                ]
    for ad in adjust_list:
        string=string.replace(ad[0],ad[1])
    return string
