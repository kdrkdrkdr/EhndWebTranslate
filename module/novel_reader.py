# 소설 제목, 횟차, 링크 가져오는 파일


from concurrent import futures
from re import sub
from url_normalize import url_normalize
from module._requirement_func import *
from module._translate_j2k import *

""" # 소설 사이트 추가 근황

syosetu.org             |   O
syosetu.com             |   O
kakuyomu.jp             |   O
alphapolis.co.jp        |   O
pixiv.net               |   O
novelist.jp             |   O
estar.jp                |   O

akatsuki-novels.com     |   X
silufenia.com           |   X
mai-net.net             |   X
tinami.com              |   X
"""


class NovelReader(object):
    def __init__(self, novel_url):
        novel_url = url_normalize(novel_url)

        
        if 'syosetu.org' in novel_url:
            self.base_url = 'https://syosetu.org'
            self.novel_id = sub('[\D]', '', novel_url.replace(' ', '').split('syosetu.org/novel/')[1].split('/')[0])
            self.novel_url = f'{self.base_url}/novel/?mode=r18_cs_end&nid={self.novel_id}'
            self.soup = GetSoup(self.novel_url, self.base_url)
            self.is_r18 = True if 'あなたは18歳以上ですか？' in str(self.soup) else False



        elif 'syosetu.com' in novel_url:
            self.is_r18 = True if 'novel18' in novel_url else False
            self.base_url = 'https://novel18.syosetu.com' if self.is_r18 else 'https://ncode.syosetu.com'
            self.novel_id = novel_url.split('syosetu.com/')[1].split('/')[0]
            self.novel_url = self.base_url + f'/{self.novel_id}'
            self.soup = GetSoup(self.novel_url, self.base_url)



        elif 'kakuyomu.jp' in novel_url:
            self.base_url = 'https://kakuyomu.jp/works'
            self.novel_id = novel_url.split('works/')[1].split('/episodes')[0]
            self.novel_url = self.base_url + f'/{self.novel_id}'
            self.soup = GetSoup(self.novel_url, self.base_url)
            self.info = self.soup.find_all('li', {'class':'widget-toc-episode'})
            self.episode_ids = [i.find('a')['href'].split('/episodes')[1] for i in self.info]
            


        elif 'alphapolis.co.jp' in novel_url:
            self.base_url = 'https://www.alphapolis.co.jp'
            self.novel_url = novel_url.split('/episode')[0]
            self.soup = GetSoup(self.novel_url, self.base_url)
            self.info = self.soup.find('div', {'class':'episodes'}).find_all('div', {'class':'episode'})
            self.episode_URLs = [self.base_url+i.find('a')['href'] for i in self.info]



        elif 'pixiv.net' in novel_url:
            self.base_url = 'https://pixiv.net'
            
            if '/series/' in novel_url:
                self._soup = GetSoup(novel_url, self.base_url, is_render=True, is_xpath=True)
                self._n_url = self.base_url+self._soup.xpath('//*[@id="root"]/div[2]/div[3]/div/div/main/section/div[1]/div[3]/div[1]/ul/li[1]/div[1]/a')[0].attrib['href']
            else:
                self._n_url = novel_url

            self.soup = GetSoup(self._n_url, self.base_url, is_render=True)
            self.ol = self.soup.find_all('ol')

            if len(self.ol) > 2:
                self.info = self.ol[0].find_all('a')
                self.episode_URLs = [self.base_url+i['href'] for i in self.info]
                
            self.novel_url = novel_url



        elif 'novelist.jp' in novel_url:
            self.base_url = novel_url.replace(novel_url.split('.jp')[1], '')
            self.novel_id = novel_url.split('.jp/')[1].split('.')[0]
            self.novel_url = self.base_url + f'/{self.novel_id}.html'
            self.soup = GetSoup(self.novel_url, self.base_url)
            self.epiCount = int(sub('[\D]', '', str(self.soup.find('div', {'class':'work_right'}).find_all('p')[1]).split('<br/>')[1]))



        elif 'estar.jp' in novel_url:
            self.base_url = 'https://estar.jp'
            self.novel_id = novel_url.split('novels/')[1].split('/')[0]
            self.novel_url = f'{self.base_url}/novels/{self.novel_id}'

            self.titleList = []
            self.epi_page = []

            self._epi_idx_page = int(sub('[\D]', '', GetSoup(f"{self.novel_url}/episodes", self.base_url).find('p', {'class':'currentPage'}).text))
            for i in range(self._epi_idx_page):
                self._soup = GetSoup(f'https://estar.jp/novels/{self.novel_id}/episodes?page={i+1}', self.base_url).find('div', {'class':'episodeList'})
                self.titleList.extend([j.text for j in self._soup.find_all('div', {'class':'label'})])
                self.epi_page.extend([int(sub('[\D]', '', j.text)) for j in self._soup.find_all('p', {'class':'meta'})])

            self.soup = GetSoup(self.novel_url, self.base_url)
            self.entire_pages = int(GetSoup(self.novel_url+'/viewer?page=1', self.base_url).find('input', {'type':'number'})['max'])






    def is_short_story(self):
        if 'syosetu.org' in self.novel_url:
            try: self.soup.find('span', {'itemprop':'name'}).text; return False
            except AttributeError: return True
        
        elif 'syosetu.com' in self.novel_url:
            try: self.soup.find('div', {'class':'index_box'}).text; return False
            except AttributeError: return True

        elif 'kakuyomu.jp' in self.novel_url:
            return False# 단편의 개념이 없는 사이트

        elif 'alphapolis.co.jp' in self.novel_url:
            return False

        elif 'pixiv.net' in self.novel_url:
            return (len(self.ol) == 2)

        elif 'novelist.jp' in self.novel_url:
            return not self.soup.select_one('body > div.main_box > div.container > div.center_box > h2:nth-child(5)').text == '目次'

        elif 'estar.jp' in self.novel_url:
            return False








    def get_big_title(self):
        if 'syosetu.org' in self.novel_url:
            if self.is_short_story():
                bigTitle = self.soup.find('div', {'class':'ss'}).find('a').text
            else:
                bigTitle = self.soup.find('span', {'itemprop':'name'}).text

        
        elif 'syosetu.com' in self.novel_url:
            bigTitle = self.soup.find('p', {'class':'novel_title'}).text


        elif 'kakuyomu.jp' in self.novel_url:
            bigTitle = self.soup.find('span', {'id':'catchphrase-body'}).text


        elif 'alphapolis.co.jp' in self.novel_url:
            bigTitle = self.soup.find('h2', {'class':'title'}).text.replace('\n', '')


        elif 'pixiv.net' in self.novel_url:
            if self.is_short_story():
                bigTitle = self.soup.find('h1').text
            else:
                bigTitle = self.soup.find_all('header')[1].find('h2').text


        elif 'novelist.jp' in self.novel_url:
            bigTitle = self.soup.find('h2').text


        elif 'estar.jp' in self.novel_url:
            bigTitle = self.soup.find('h1', {'class':'title'}).text



        return t_j2k(bigTitle)








    def get_small_titles(self):
        if 'syosetu.org' in self.novel_url:
            if self.is_short_story(): 
                return "[단편] " + t_j2k(self.get_big_title())
            else:
                titleList = []
                c = self.soup.find('div', {'id':'maind'}).find_all('div', {'class':'ss'})[2].find_all('tr')
                
                for i in c:
                    l = i.find_all('a', {'style':'text-decoration:none;'})
                    if len(l) !=0:
                        titleList.append(l[0].text)

                return t_j2k('\n'.join(titleList)).split('\n')



        elif 'syosetu.com' in self.novel_url:
            if self.is_short_story(): 
                return "[단편] " + t_j2k(self.get_big_title())
            else:
                titleList = [i.text.replace('\n', '') for i in self.soup.find('div', {'class':'index_box'}).find_all('dd', {'class':'subtitle'})]
                return t_j2k('\n'.join(titleList)).split('\n')



        elif 'kakuyomu.jp' in self.novel_url:
            titleList = [i.find('span', {'class':'widget-toc-episode-titleLabel js-vertical-composition-item'}).text for i in self.info]
            return t_j2k('\n'.join(titleList)).split('\n')



        elif 'alphapolis.co.jp' in self.novel_url:
            titleList = [i.find('span', {'class':'title'}).text for i in self.info]
            return t_j2k('\n'.join(titleList)).split('\n') 



        elif 'pixiv.net' in self.novel_url:
            if self.is_short_story():
                return "단편 " + t_j2k(self.get_big_title())
            else:
                titleList = [i.text for i in self.info]
                return t_j2k('\n'.join(titleList)).split('\n') 



        elif 'novelist.jp' in self.novel_url:
            titleList = [f'{i+1} 페이지' for i in range(self.epiCount)]
            return t_j2k('\n'.join(titleList)).split('\n') 

        

        elif 'estar.jp' in self.novel_url:
            return t_j2k('\n'.join(self.titleList)).split('\n') 








    def get_content(self, novel_round):
        if 'syosetu.org' in self.novel_url:
            if self.is_short_story():
                epiURL = self.novel_url
            else:
                epiURL = f'{self.novel_url}&volume={novel_round+1}'

            return '\n'.join([n.text for n in GetSoup(epiURL, self.base_url).find('div', {'id':'honbun'}).find_all('p')])



        elif 'syosetu.com' in self.novel_url:
            if self.is_short_story():
                epiURL = self.novel_url
            else:
                epiURL = url_normalize(f'{self.novel_url}/{novel_round+1}')

            return '\n'.join([n.text for n in GetSoup(epiURL, self.base_url).find('div', {'id':'novel_honbun'}).find_all('p')])



        elif 'kakuyomu.jp' in self.novel_url:
            epiURL = url_normalize(f'{self.novel_url}/episodes/{self.episode_ids[novel_round]}')
            return '\n'.join([n.text for n in GetSoup(epiURL, self.base_url).find('div', {'class':'widget-episodeBody js-episode-body'}).find_all('p')])



        elif 'alphapolis.co.jp' in self.novel_url:
            epiURL = self.episode_URLs[novel_round]
            return GetSoup(epiURL, self.base_url).find('div', {'id':'novelBoby'}).text.replace('\t', '')


        
        elif 'pixiv.net' in self.novel_url:
            if self.is_short_story():
                epiURL = self.novel_url
            else:
                epiURL = self.episode_URLs[novel_round]
            self.novel_id = sub('[\D]', '', epiURL)
            return json.loads(GetSoup(epiURL, self.base_url).find('meta', {'id':'meta-preload-data'})['content'])['novel'][self.novel_id]['content'].replace('[newpage]', '')



        elif 'novelist.jp' in self.novel_url:
            epiURL = f'{self.base_url}/{self.novel_id}_p{novel_round+1}.html'
            nSoup = GetSoup(epiURL, self.base_url).find('div', {'class':'work_read'})
            nSoup.find('div', {'class':'work_read_header'}).extract()
            return nSoup.text




        elif 'estar.jp' in self.novel_url:
            if novel_round+1 == len(self.epi_page):
                ran = range(self.epi_page[novel_round], self.entire_pages+1)
            else:
                ran = range(self.epi_page[novel_round], self.epi_page[novel_round+1])
            

            return '\n\n\n'.join([GetSoup(f'https://estar.jp/novels/{self.novel_id}/viewer?page={i}', self.base_url).find('div', {'lang':'ja'}).text for i in ran])