#-*- coding:utf-8 -*-


from module._translate_j2k import *
from bs4 import BeautifulSoup
from webbrowser import open_new
import re
from time import time
from pprint import pprint



def WriteFile(text: str, filename: str):
    f = codecs.open(filename, mode='w', encoding='utf-8')
    f.write(u'{}'.format(text))
    f.close()




def ReplacingText(text:str, repl_dict: dict):
    for key, value in repl_dict.items():
        replaced_text = str(text).replace(key, value)

    return replaced_text



def PrettifyHtml(html:str):
    return BeautifulSoup(html, 'html.parser').prettify()


