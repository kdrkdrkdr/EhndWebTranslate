#-*- coding:utf-8 -*-

from ctypes import (
    WinDLL,
    c_char_p,
    c_int,
    c_wchar_p,
    wintypes,
)

from re import *

from os import path, listdir

import sys

import codecs

from time import sleep


import shutil


J2K_ENGINE_H_DLL = '.\\utils\\J2KEngine.dll'
DAT_DIRECTORY = bytes('.\\utils\\Dat\\', encoding='utf-8')

class TranslateEngine:

    def __init__(self):
        self.LoadDLL = WinDLL(J2K_ENGINE_H_DLL)

        self.Engine = self.LoadDLL.J2K_InitializeEx
        self.Engine.argtypes = [c_char_p, c_char_p]
        self.Engine.restype = wintypes.BOOL

        self.Translate = self.LoadDLL.J2K_TranslateMMNTW

        self.Translate.argtypes = [c_int, c_wchar_p]
        self.Translate.restype = c_wchar_p

        self.StartTranslate = self.Engine(b'CSUSER123455', DAT_DIRECTORY)

    

    def DecodeText(self, japanese: str):
        chars = "↔◁◀▷▶♤♠♡♥♧♣⊙◈▣◐◑▒▤▥▨▧▦▩♨☏☎☜☞↕↗↙↖↘♩♬㉿㈜㏇™㏂㏘＂＇∼ˇ˘˝¡˚˙˛¿ː∏￦℉€㎕㎖㎗ℓ㎘㎣㎤㎥㎦㎙㎚㎛㎟㎠㎢㏊㎍㏏㎈㎉㏈㎧㎨㎰㎱㎲㎳㎴㎵㎶㎷㎸㎀㎁㎂㎃㎄㎺㎻㎼㎽㎾㎿㎐㎑㎒㎓㎔Ω㏀㏁㎊㎋㎌㏖㏅㎭㎮㎯㏛㎩㎪㎫㎬㏝㏐㏓㏃㏉㏜㏆┒┑┚┙┖┕┎┍┞┟┡┢┦┧┪┭┮┵┶┹┺┽┾╀╁╃╄╅╆╇╈╉╊┱┲ⅰⅱⅲⅳⅴⅵⅶⅷⅸⅹ½⅓⅔¼¾⅛⅜⅝⅞ⁿ₁₂₃₄ŊđĦĲĿŁŒŦħıĳĸŀłœŧŋŉ㉠㉡㉢㉣㉤㉥㉦㉧㉨㉩㉪㉫㉬㉭㉮㉯㉰㉱㉲㉳㉴㉵㉶㉷㉸㉹㉺㉻㈀㈁㈂㈃㈄㈅㈆㈇㈈㈉㈊㈋㈌㈍㈎㈏㈐㈑㈒㈓㈔㈕㈖㈗㈘㈙㈚㈛ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⒜⒝⒞⒟⒠⒡⒢⒣⒤⒥⒦⒧⒨⒩⒪⒫⒬⒭⒮⒯⒰⒱⒲⒳⒴⒵⑴⑵⑶⑷⑸⑹⑺⑻⑼⑽⑾⑿⒀⒁⒂"
        for c in chars:
            if c in japanese:
                japanese = japanese.replace(c, f'\\u{str(hex(ord(c)))[2:]}')
        return japanese



    def EncodeText(self, japanese: str):
        return str(
            sub(
                r'(?i)(?<!\\)(?:\\\\)*\\u([0-9a-f]{4})',
                lambda m: chr(int(m.group(1), 16)),
                japanese
            )
        )



    def RunTranslate(self, japanese: str):
        return self.EncodeText(
            self.Translate(
                0,
                self.DecodeText(japanese)
            )
        )




def SetRepeat(origin_text: str, set_repeat_num=10, max_substr_len=8, seperator=''):
    """
    origin_text: 일본어
    set_repeat_num: 같은 문자열 반복 횟수
    max_substr_len: 반복 문자열 최대 길이
    """

    repeated_str_start_idx = []
    changed_text = origin_text

    i = 0
    while i < len(changed_text):
        text_length = len(changed_text)

        upper_repeat_substr_length = (text_length - i) // 2
        if max_substr_len and max_substr_len < upper_repeat_substr_length:
            upper_repeat_substr_length = max_substr_len + 1

        for repeat_length in range(1, upper_repeat_substr_length):
            substr = changed_text[i:i+repeat_length]
            right_start = i + repeat_length
            right_end = right_start + repeat_length
            right_substr = changed_text[right_start:right_end]
            num_repeat_substrs = 1

            while substr == right_substr and right_end <= text_length:
                num_repeat_substrs += 1
                right_start += repeat_length
                right_end += repeat_length
                right_substr = changed_text[right_start:right_end]

            if num_repeat_substrs > set_repeat_num:
                changed_text = changed_text[:i+repeat_length*set_repeat_num] + seperator + changed_text[i+repeat_length*num_repeat_substrs:]
                repeated_str_start_idx.append(i)
                
        i += 1


    result_text = changed_text

    if seperator == '▂':
        idx_sep = [i for i, x in enumerate(result_text) if x == seperator]
        repeat_phrases = [result_text[repeated_str_start_idx[j]:idx_sep[j]] for j in range(len(idx_sep))]

    else:
        repeat_phrases = None

    return [result_text, repeat_phrases]





def CheckRepeatPhrase(origin_text: str):
    changed_text = origin_text
    
    repeated_phrase = SetRepeat(origin_text=changed_text, seperator='▂')[1]
    
    register_phrases = []
    for s in repeated_phrase:
        a = SetRepeat(origin_text=s, set_repeat_num=1)[0]
        register_phrases.append(a)
    
    return register_phrases




t = TranslateEngine()
def TransJ2K(japanese: str, isHtml=False):

    if japanese.replace(' ', '') == '':
        return '\n'

    text = t.RunTranslate(japanese)
    
    if isHtml: # html 후처리
        if text in ['”"', '"”']:
            text = text.replace('”"', '')
            text = text.replace('"”', '')
            
        if text in ['”"', '"”']:
            text = text.replace('”"', '')
            text = text.replace('"”', '')

        else:
            text = text.replace('”', '"')

        text = text.replace('”', '')


    else:
        text = sub('p[\w]*&[\w]*[:|.|a-zA-Z]', '', text)


    return text




def t_j2k(japanese: str, isHtml=False):
    lastjpn = SetRepeat(japanese, set_repeat_num=10)[0]
    text = TransJ2K(japanese=lastjpn, isHtml=isHtml)
    return text

# testURL = https://ncode.syosetu.com/n1031gv/3