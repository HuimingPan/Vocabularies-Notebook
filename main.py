# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 14:56:50 2021

@author: William
"""

from get_word import Word
from latex import latex_init,add_word
import os

filedir = '../Words and Notebooks'
foldname='demo/'
filename='demo.txt'
title=filename[:-4]
filepath=os.path.join(filedir,foldname,filename)
def read_wordsfile(filepath,sort=False,duplicate=False):
    with open(filepath) as f:
        words_list=f.read()
        words_list=words_list.replace(" ","").replace("\n","")
        print(words_list)
        words_list=words_list.split(",")
        if sort:
            print("*****************resort***************")
            words_list.sort()
        if duplicate:
            print("************remove duplicate words***************")
            formatList = list(set(words_list))
            formatList.sort(key=words_list.index)
            words_list=formatList
        print("-------------Read Done!----------------")
        return words_list

words=read_wordsfile(filepath,sort=False,duplicate=True)
doc=latex_init(title)
for word in words:
    add_word(doc,Word(word))
    


doc.generate_pdf(filepath=os.path.join(filedir,foldname),compiler='xelatex')
doc.generate_tex(filepath=os.path.join(filedir,foldname))
print("Done!")
