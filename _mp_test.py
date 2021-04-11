import asyncio
from module._requirement_func import *
from module._translate_j2k import *


jText = '''
女は面倒。男同士でつるんでる方が気が楽。そんな女嫌いの男子高校生だった主人公は、ある朝学校に向かう途中、スマホを弄りながらよそ見運転をしていた中年女に撥ねられ、意識を失う。
次に目覚めた時、彼は見知らぬ異世界で、ホーク・ゴルドなる大金持ちの家の子供、それも、甘やかされて育ったがために、モラルもへったくれもない極度の女好きの肥満児に転生してしまっていた。
いきなり第2の人生を歩むことを余儀なくされてしまった彼は、金や権力に群がる女たちを遠ざけ、ついでに美女メイドや美幼女妹、美少女婚約者たちからなんとか距離を置こうと足掻き始める。
しかし00年代後半生まれの彼は知らなかった。この世界が90年代に発売された懐かしのギャルゲー『エレメンツイレブン』の世界であり、ホーク・ゴルドはそのお邪魔キャラであることを。

【現在第4部1章まで完結しました】
いよいよ原作ゲームが開始する年になってしまいましたが果たして

美少女!美男子!幼女!イケメン!みたいな、恋愛脳の美男美女ばかりの展開に少しばかり胃もたれしてしまったそこのあなた、たまには箸休めにポッチャリ系男主人公と洋画の吹き替えみたいな渋い声してそうなおっさん達が主体で綴られていく、恋愛要素のうっすい物語はいかがですか?
※全体的に自業自得とはいえ美少女たちが若干酷い目に遭う描写(TF・石化・etc)を含みます。そういった要素に抵抗のある方はご注意ください

'''


start = time()
async def WriteThread(num):
    jpn = t_j2k(jText)
    WriteFile(jpn, f'{num}.txt')
    return jpn

async def main():
    s = [asyncio.ensure_future(WriteThread(i)) for i in range(10)]
    await asyncio.gather(*s)

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(main())




# start2 = time()
# def WriteThread2(num):
#     jpn = t_j2k(jText)
#     WriteFile(jpn, f'{num}.txt')
#     return jpn

# thr = [Thread(target=WriteThread2, args=(i,)) for i in range(10)]

# for t in thr:
#     t.start()

# for t in thr:
#     t.join()
# print(time()-start2)