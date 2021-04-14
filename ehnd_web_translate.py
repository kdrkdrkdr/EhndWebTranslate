#-*- coding:utf-8 -*-

from module._translate_j2k import t_j2k
from module._requirement_func import *

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions

import asyncio

from UI_MAIN import Ui_MainWindow


findJpn = re.compile('[\u3000-\u303f\u3040-\u309f\u30a0-\u30ff\uff00-\uff9f\u4e00-\u9faf\u3400-\u4dbf]')


def async_loop(func, *args):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(func(*args))
    loop.close()





class LoadDriverWindow(QThread):
    def __init__(self, window):
        QThread.__init__(self)
        self.window = window
        self.winList = []



    def run(self):
        self.window.window_list.clear()
        self.dw_handles = self.window.driver.window_handles
        cwh = self.window.driver.current_window_handle
        
        for dw in self.dw_handles:
            self.window.driver.switch_to.window(dw)
            self.window.window_list.addItem(self.window.driver.title)

        self.window.driver.switch_to.window(cwh)






class TransThread(QThread):
    def __init__(self, window, isTrans=True):
        QThread.__init__(self)
        self.working = True
        self.window = window
        self.isTrans = isTrans
        self.setTerminationEnabled = True

        self.ehnd_webtr_log = ""


    def stop(self):
        self.window.btnSetting(setNum=1)
        self.window.show_status.setText("번역 중지!")
        self.terminate()


    def run(self):
        self.window.btnSetting(setNum=0)
        try:
            start_time = time()
            self.window.sec.setText("")

            if self.isTrans:
                self.window.show_status.setText("번역 중")
                a = self.window.driver.find_elements_by_xpath('.//*[normalize-space(text())]')
                
                async_loop(self.rt, a)

                self.window.sec.setText(f"{int(time()-start_time)}초")
                self.window.show_status.setText("번역 성공")

                
            else:
                self.window.driver.refresh()
                self.window.sec.setText("")
                self.window.show_status.setText("원본 보기")


        except:
            self.window.show_status.setText("번역 실패")

        finally:
            self.window.btnSetting(setNum=1)



    async def runTrans(self, i):
        try:
            if i.is_displayed():

                inner = i.get_attribute('innerHTML')
                outer = i.get_attribute('outerHTML')
                
                if bool(len(re.sub(r'\s+', '', inner))):
                    p_html = PrettifyHtml(outer).split('\n')

                    modified_html = []
                    for ih in p_html:
                        
                        if re.sub(r'\s+', '', ih).startswith('<'):
                            modified_html.append(ih)
                        else:

                            isJpn = findJpn.search(ih)

                            if isJpn != None:
                                modified_html.append(t_j2k(japanese=ih))
                                print("번역O -> ", ih)
                            else:
                                modified_html.append(ih)
                                print("번역X -> ", ih)
                                

                    ih_elements = ''.join(modified_html)

                    self.window.driver.execute_script("arguments[0].outerHTML = arguments[1]", i, ih_elements)


        except exceptions.StaleElementReferenceException:
            print("StaleElementRefernceException")


    async def rt(self, a):
        s = [asyncio.ensure_future(self.runTrans(i)) for i in a]
        await asyncio.gather(*s)



class EhndTrans(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setThread = None

        options = webdriver.ChromeOptions()
        options.add_argument("disable-gpu") 
        options.add_argument("disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # prefs = \
        # {
        #     'profile.default_content_setting_values': 
        #     {
        #         'cookies' : 2, 'images': 2, 'plugins' : 2, 'popups': 2, 'geolocation': 2, 'notifications' : 2, 'auto_select_certificate': 2, 'fullscreen' : 2, 'mouselock' : 2, 'mixed_script': 2, 'media_stream' : 2, 'media_stream_mic' : 2, 'media_stream_camera': 2, 'protocol_handlers' : 2, 'ppapi_broker' : 2, 'automatic_downloads': 2, 'midi_sysex' : 2, 'push_messaging' : 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop' : 2, 'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement' : 2, 'durable_storage' : 2
        #     }
        # }
        # options.add_experimental_option('prefs', prefs)

        # self.driver = webdriver.Chrome(executable_path='./89/chromedriver.exe',options=options)

        chromedriver_autoinstaller.install('./')
        self.driver = webdriver.Chrome(options=options)
        self.driver.get("https://www.google.com")

        self.setupUi(self)

        QObject.connect(self.show_trans_btn, SIGNAL('clicked()'), self.showTrans)
        QObject.connect(self.show_ori_btn, SIGNAL('clicked()'), self.showOri)
        QObject.connect(self.go_dev_page, SIGNAL('clicked()'), self.goDevPage)
        QObject.connect(self.reloadBtn, SIGNAL('clicked()'), self.reloadWindow)
        QObject.connect(self.stop_trans_btn, SIGNAL('clicked()'), self.stopThread)
        self.window_list.currentIndexChanged.connect(self.setWindow)

        self.btnSetting(setNum=1)
        self.reloadWindow()

        self.show()



    def showTrans(self):
        st = TransThread(self, isTrans=True)
        self.setThread = st
        st.start()


    def showOri(self):
        so = TransThread(self, isTrans=False)
        self.setThread = so
        so.start()
    

    def goDevPage(self):
        open_new('https://blog.naver.com/powerapollon')


    def reloadWindow(self):
        ldw = LoadDriverWindow(self)
        self.setThread = ldw
        ldw.start()


    def setWindow(self):
        dw_handles = self.driver.window_handles
        self.driver.switch_to.window(dw_handles[self.window_list.currentIndex()])

    
    def stopThread(self):
        self.setThread.stop()

    
    def btnSetting(self, setNum):
        if setNum == 0:
            self.show_trans_btn.setDisabled(True)
            self.show_ori_btn.setDisabled(True)
            self.window_list.setDisabled(True)
            self.reloadBtn.setDisabled(True)
            self.go_dev_page.setDisabled(True)
            self.stop_trans_btn.setDisabled(False)

        if setNum == 1:
            self.show_trans_btn.setDisabled(False)
            self.show_ori_btn.setDisabled(False)
            self.window_list.setDisabled(False)
            self.reloadBtn.setDisabled(False)
            self.go_dev_page.setDisabled(False)
            self.stop_trans_btn.setDisabled(True)



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    et = EhndTrans()
    app.exec_()
    et.driver.quit()
    sys.exit()