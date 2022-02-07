#-*- coding:utf-8 -*-


from bs4 import BeautifulSoup
from webbrowser import open_new
import re
from time import sleep
from time import time
from pprint import pprint
import bs4
from requests import get
from get_html import HtmlRenderer
import requests
from jaconv import kata2hira
from math import *
import numpy as np
import codecs
from selenium.webdriver import Chrome, ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.common import exceptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from subprocess import CREATE_NO_WINDOW
from pathlib import Path
from time import sleep, time
import os

import pyperclip
import json
from lxml import etree

from concurrent.futures import ThreadPoolExecutor
from functools import partial
import asyncio




findJpn = re.compile('[\u3000-\u303f\u3040-\u309f\u30a0-\u30ff\uff00-\uff9f\u4e00-\u9faf\u3400-\u4dbf]')





def DeleteFileInTEMP():
    tmp = './utils/tmp/'
    for f in os.listdir(tmp):
        os.remove(os.path.join(tmp, f))



def async_loop(func, *args):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(func(*args))
    loop.close()




def GetSoup(url, referer, is_render=False, is_xpath=False):
    headers = {
        'referer': referer,
        "User-Agent": "Mozilla/5.0",
    }
    while True:
        try:
            if is_render:
                renderer = HtmlRenderer()
                resp = renderer.render(url=url)
            else:
                resp = get(url, headers=headers, cookies={'over18':'yes'})

            html = resp.text


            if is_xpath:
                result = etree.HTML(html)
            else:
                result =  BeautifulSoup(html, 'html.parser')
                
                
            return result

        except:
            sleep(2)


async def async_GetSoup(url, referer, is_render=False, is_xpath=False):
    headers = {
        'referer': referer,
        "User-Agent": "Mozilla/5.0",
    }
    while True:
        try:
            if is_render:
                renderer = HtmlRenderer()
                resp = renderer.render(url=url)
            else:
                resp = get(url, headers=headers, cookies={'over18':'yes'})

            html = resp.text


            if is_xpath:
                result = etree.HTML(html)
            else:
                result =  BeautifulSoup(html, 'html.parser')
                
                
            return result

        except:
            sleep(2)




def ListChunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]


def PrettyJson(msg):
    return json.dumps(msg, indent=4, sort_keys=True, ensure_ascii=False)


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








def distance(x1, y1, x2, y2):
    result = sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))
    return result


def vector_inner_cos_to_degree(x1, y1, x2, y2):
    try:
        cos = (x1*x2 + y1*y2) / ( sqrt(x1**2 + y1**2) * sqrt(x2**2 + y2**2) )
        rad = acos(cos)
        return degrees(rad)

    except ZeroDivisionError:
        return 0.0


def ImageDownload(filename, url):
    header = {
        'User-agent' : 'Mozilla/5.0',
        'Referer' : url
    }
    while True:
        try:
            with open(filename, 'wb') as f:
                resp = requests.get(url, headers=header)
                if resp.status_code == 404:
                    break
                f.write(resp.content)
                break
        except ( exceptions.ChunkedEncodingError, exceptions.Timeout, exceptions.ConnectionError ):
            continue




def clickAction(driver, element):
    action = ActionChains(driver)
    action.click(on_element=element)
    action.perform()


