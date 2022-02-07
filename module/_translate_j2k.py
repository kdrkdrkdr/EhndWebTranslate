#-*- coding:utf-8 -*-

from ctypes import (
    WinDLL,
    c_char_p,
    c_int,
    c_wchar_p,
    wintypes,
)

import re
from os import path, listdir
import sys
import codecs
from time import sleep
import shutil
import html
from os.path import isfile
import neologdn
from jaconv import kata2hira







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
            re.sub(
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





    
    
forcePre = './utils/Ehnd/Force_PreFilter_@JP.txt'
forcePost = './utils/Ehnd/Force_PostFilter_@KR.txt'

if not isfile(forcePre): codecs.open(forcePre, 'w', encoding='utf-8').close()
if not isfile(forcePost): codecs.open(forcePost, 'w', encoding='utf-8').close()


f_jp = codecs.open(forcePre, 'r', encoding='utf-8').readlines()
f_kr = codecs.open(forcePost, 'r', encoding='utf-8').readlines()


import flashtext

keyword_processor_jp = flashtext.KeywordProcessor()
keyword_processor_kr = flashtext.KeywordProcessor()

for j in f_jp:
    try:
        if not j.lstrip().startswith("//"):
            jp = j.split('\t')
            keyword_processor_jp.add_keyword(jp[0], jp[1])
    except IndexError:
        pass


for k in f_kr:
    try:
        if not k.lstrip().startswith("//"):
            kr = k.split('\t')
            keyword_processor_kr.add_keyword(kr[0], kr[1])
    except IndexError:
        pass





t = TranslateEngine()

def t_j2k(japanese: str, isForceFilter=False, isRemoveOri=False):
    lastjpn = neologdn.normalize(japanese, repeat=10)


    if japanese.replace(' ', '') == '':
        return '\n'

    if isForceFilter:
        text = keyword_processor_jp.replace_keywords(japanese)

    text = t.RunTranslate(japanese)
    text = re.sub('p[\w]*&[\w]*[:|.|a-zA-Z]', '', text)

    if isForceFilter:
        text = keyword_processor_kr.replace_keywords(text)

    if isRemoveOri:
        text = re.sub('\[(?<=\[)[^\]]*(?=\])]', '', text)

    return text.strip()





def furiRead(text: str):

    # 카타카나 -> 히라가나
    text = kata2hira(text)

    # 히라가나 요음 조합
    text = text.replace('きゃ', '캬').replace('きゅ', '큐').replace('きょ', '쿄')
    text = text.replace('ぎゃ', '갸').replace('ぎゅ', '규').replace('ぎょ', '교')
    text = text.replace('しゃ', '샤').replace('しゅ', '슈').replace('しょ', '쇼')
    text = text.replace('じゃ', '쟈').replace('じゅ', '쥬').replace('じょ', '죠')
    text = text.replace('ちゃ', '차').replace('ちゅ', '츄').replace('ちょ', '쵸')
    text = text.replace('にゃ', '냐').replace('にゅ', '뉴').replace('にょ', '뇨')
    text = text.replace('ひゃ', '햐').replace('ひゅ', '휴').replace('ひょ', '효')
    text = text.replace('ふぁ', '화').replace('ふぃ', '휘').replace('ふぇ', '훼').replace('ふぉ', '후')
    text = text.replace('みゃ', '먀').replace('みゅ', '뮤').replace('みょ', '묘')
    text = text.replace('りゃ', '랴').replace('りゅ', '류').replace('りょ', '료')
    text = text.replace('びゃ', '뱌').replace('びゅ', '뷰').replace('びょ', '뵤')
    text = text.replace('ぴゃ', '퍄').replace('ぴゅ', '퓨').replace('ぴょ', '표')


    # ん
    text = text.replace('たん', '탄').replace('ちん', '친').replace('つん', '친').replace('てん', '텐').replace('とん', '톤')
    text = text.replace('だん', '딘').replace('ぢん', '진').replace('づん', '즌').replace('でん', '덴').replace('どん', '돈')
    text = text.replace('さん', '산').replace('しん', '신').replace('すん', '슨').replace('せん', '센').replace('そん', '손')
    text = text.replace('ざん', '잔').replace('じん', '진').replace('ずん', '즌').replace('ぜん', '젠').replace('ぞん', '존')
    text = text.replace('なん', '난').replace('にん', '닌').replace('ぬん', '눈').replace('ねん', '넨').replace('のん', '논')
    text = text.replace('らん', '란').replace('りん', '린').replace('るん', '룬').replace('れん', '렌').replace('ろん', '론')

    text = text.replace('まん', '마').replace('みん', '미').replace('むん', '문').replace('めん', '멘').replace('もん', '몬')
    text = text.replace('ばん', '반').replace('びん', '빈').replace('ぶん', '분').replace('べん', '벤').replace('ぼん', '본')
    text = text.replace('ぱん', '판').replace('ぴん', '핀').replace('ぷん', '푼').replace('ぺん', '펜').replace('ぽん', '폰')

    text = text.replace('かん', '칸').replace('きん', '킨').replace('くん', '쿤').replace('けん', '켄').replace('こん', '콘')
    text = text.replace('がん', '간').replace('ぎん', '긴').replace('ぐん', '군').replace('げん', '겐').replace('ごん', '곤')

    text = text.replace('あん', '앙').replace('いん', '잉').replace('うん', '운').replace('えん', '엔').replace('おん', '온')
    text = text.replace('はん', '와').replace('ひん', '히').replace('ふん', '훈').replace('へん', '에').replace('ほん', '혼')
    text = text.replace('やん', '야').replace('ゆん', '유').replace('よん', '욘')
    text = text.replace('わん', '완').replace('ゐん', '이').replace('ゑん', '엔').replace('をん', '오')


    # 히라가나 탁음, 반탁음
    text = text.replace('が', '가').replace('ぎ', '기').replace('ぐ', '구').replace('げ', '게').replace('ご', '고')
    text = text.replace('ざ', '자').replace('じ', '지').replace('ず', '즈').replace('ぜ', '제').replace('ぞ', '조')
    text = text.replace('だ', '다').replace('ぢ', '지').replace('づ', '즈').replace('で', '데').replace('ど', '도')
    text = text.replace('ば', '바').replace('び', '비').replace('ぶ', '부').replace('べ', '베').replace('ぼ', '보')    
    text = text.replace('ぱ', '파').replace('ぴ', '피').replace('ぷ', '푸').replace('ぺ', '페').replace('ぽ', '포')


    # 히라가나 50음도
    text = text.replace('あ', '아').replace('い', '이').replace('う', '우').replace('え', '에').replace('お', '오')
    text = text.replace('か', '카').replace('き', '키').replace('く', '쿠').replace('け', '케').replace('こ', '코')
    text = text.replace('さ', '사').replace('し', '시').replace('す', '스').replace('せ', '세').replace('そ', '소')
    text = text.replace('た', '타').replace('ち', '치').replace('つ', '츠').replace('て', '테').replace('と', '토')
    text = text.replace('な', '나').replace('に', '니').replace('ぬ', '누').replace('ね', '네').replace('の', '노')
    text = text.replace('は', '하').replace('ひ', '히').replace('ふ', '후').replace('へ', '헤').replace('ほ', '호')
    text = text.replace('ま', '마').replace('み', '미').replace('む', '무').replace('め', '메').replace('も', '모')
    text = text.replace('ら', '라').replace('り', '리').replace('る', '루').replace('れ', '레').replace('ろ', '로')
    text = text.replace('や', '야').replace('ゆ', '유').replace('よ', '요')
    text = text.replace('わ', '와').replace('ゐ', '이').replace('ゑ', '에').replace('を', '오')


    # 촉음 っ
    while 'っ' in text:
        text = list(text)
        tsu_pos = text.index('っ')
        
        if len(text) <= tsu_pos + 1:
            return ''.join(text[:-1]) + '쓰'
        
        if tsu_pos == 0:
            text[tsu_pos] = '쓰'
        
        else:
            text[tsu_pos] = text[tsu_pos + 1]

        text = ''.join(text)


    return text
