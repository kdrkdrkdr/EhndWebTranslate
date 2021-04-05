
from module._requirement_func import *
from module._translate_j2k import *


text = '''
レオピン少年は、生まれつき器用であった。
彼はその器用さを活かし、幼い頃から様々なクラフトを行ない、仲間たちに貢献してきた。

レオピンは『王立開拓学園』に仲間たちとともに進学。
しかし入学式での『能力開花の儀式』において、レオピンに与えられたステータスは悲惨なものであった。

『職業は無職』
『ステータスは、器用さ以外は初期値のままで成長しない』
『スキルは器用貧乏』

器用さ以外に全く取り柄のないレオピンを、クラスメイトたちは『追放』。
レオピンは『特別養成学級』という、落ちこぼれのクラスに入れられてしまう。

ひとりぼっちになってしまったレオピン。
しかし与えられたスキル『器用貧乏』が、意外な性能を持っていることに気付く。

それは、

『器用さのステータスを、他のステータスに変換できる』
『好きな職業に転職できる』

というものであった。

レオピンはまず『木こり』に転職し、森から木材を得る。
さらに『大工』に転職し、誰よりも立派な家を建築。

『鑑定士』に転職してレアアイテムを判別し、『戦斧使い』に転職してチョッカイを掛けてきた他のクラスの生徒を撃退。
『レンジャー』に転職してダンジョンを探索、『ニンジャ』に転職して罠を楽々くぐり抜ける。

レオピンは単独（ソロ）で、なんでもこなせるだけの力を手に入れていた。
ひたすら無双しているうちに、幼なじみの聖女に慕われ、美女錬金術師から見初められ、レオピンの活躍はさらに知れ渡っていく。

一方、レオピンを追放したクラスメイトたちは、レオピンの能力を目の当たりにして追放を後悔。
家は掘っ立て小屋のままで、探索もままならず、じょじょに学園内での居場所を失っていき、破滅する。
'''


from multiprocessing import Process, freeze_support



if __name__ == "__main__":
    freeze_support()

    prc = [Process(target=t_j2k, args=(f"{p}. {text}",)) for p in range(300)]

    for p in prc:
        p.start()

    for p in prc:
        p.join()



    print("완료!")





# def runTrans(ele_dict, i):
#     if i.is_displayed():

#         inner = i.get_attribute('innerHTML')
#         outer = i.get_attribute('outerHTML')
        
#         print(len(re.sub(r'\s+', '', inner)))
#         if bool(re.sub(r'\s+', '', inner)):
#             p_html = PrettifyHtml(outer).split('\n')

#             modified_html = []
#             for ih in p_html:
                
#                 if ih.startswith('<'):
#                     modified_html.append(ih)
#                 else:
#                     modified_html.append(t_j2k(ih))
                

#             ih_elements = ''.join(modified_html)

#         ele_dict[i] = ih_elements

