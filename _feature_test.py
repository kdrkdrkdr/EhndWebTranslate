import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions

from module._requirement_func import *

# chromedriver_autoinstaller.install('./utils/')





def runTrans(i):
    print(i)
    # try:
    #     if i.is_displayed():

    #         inner = i.get_attribute('innerHTML')
    #         outer = i.get_attribute('outerHTML')
            
    #         if bool(len(re.sub(r'\s+', '', inner))):
    #             p_html = PrettifyHtml(outer).split('\n')

    #             modified_html = []
    #             for ih in p_html:
                    
    #                 if re.sub(r'\s+', '', ih).startswith('<'):
    #                     modified_html.append(ih)
    #                 else:
    #                     modified_html.append(t_j2k(ih))
                    

    #             ih_elements = ''.join(modified_html)

    #             nDict = {}
    #             nDict[i] = ih_elements

    # except:
    #     pass


    # return nDict



from multiprocessing import Pool, freeze_support
if __name__ == "__main__":
    freeze_support()

    options = webdriver.ChromeOptions()
    options.add_argument("disable-gpu") 
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(executable_path='./89/chromedriver.exe',options=options)
    driver.get('https://syosetu.org/novel/254978/')
    sleep(1)



    a = driver.find_elements_by_xpath('.//*[normalize-space(text())]')
    pprint(a)
    print(type(a))

    driver.close()

    p = Pool(len(a))
    pprint(p.map(runTrans, a))




    # for k, v in ele_dict.items():
    #     try:
    #         driver.execute_script("arguments[0].outerHTML = arguments[1]", k, v)
    #     except:
    #         print(v)


# b = t_j2k('##########'.join())

    