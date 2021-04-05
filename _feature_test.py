import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions

from module._requirement_func import *

# chromedriver_autoinstaller.install('./utils/')

options = webdriver.ChromeOptions()
options.add_argument("disable-gpu") 
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_experimental_option('excludeSwitches', ['enable-logging'])



driver = webdriver.Chrome(executable_path='./89/chromedriver.exe',options=options)
driver.get('https://ncode.syosetu.com/n1031gv/2/')
sleep(1)



a = driver.find_elements_by_xpath('.//*[normalize-space(text())]')



entire_text = []
element_type = []

for i in a:
    if i.is_displayed():

        inner = i.get_attribute('innerHTML')
        outer = i.get_attribute('outerHTML')

        if BeautifulSoup(inner, 'html.parser').text:
            p_html = PrettifyHtml(outer).split('\n')

            et = [ih for ih in p_html if not re.sub(r'\s+', '', ih).startswith('<')]
            entire_text.extend(et)
            element_type.append(i)