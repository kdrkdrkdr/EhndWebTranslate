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

from threading import Thread, Semaphore, active_count



from UI_MAIN import Ui_MainWindow


# def numCount(a):
#     for i in range(1, 3):
#         print(a+i)



semap = Semaphore(5)




class TransThread(Thread):
    def __init__(self, window, isTrans=True):
        super().__init__()
        self.window = window
        self.isTrans = isTrans

        self.ele_dict = {}

    def run(self):
        try:
            start_time = time()
            self.window.sec.setText("번역 중")
            self.window.btnFrame.setDisabled(True)

            if self.isTrans:
                
                a = self.window.driver.find_elements_by_xpath('.//*[normalize-space(text())]')



                thr = [Thread(target=self.runTrans, args=(self.ele_dict, k)) for k in a]
                n = 10
                thr_sep = [thr[i * n:(i + 1) * n] for i in range((len(thr) + n - 1) // n )]

                for ts in thr_sep:

                    for t in ts:
                        t.start()

                    for t in ts:
                        t.join()



                for k, v in self.ele_dict.items():
                    try:
                        self.window.driver.execute_script("arguments[0].outerHTML = arguments[1]", k, v)
                    except:
                        print(v)


                self.window.sec.setText(f"{int(time()-start_time)}초")

                
            else:
                self.window.driver.refresh()


        # except:
        #     self.window.sec.setText("번역 실패!")

        finally:
            self.window.btnFrame.setDisabled(False)




    def runTrans(self, ele_dict, i):
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
                        modified_html.append(t_j2k(ih))
                    

                ih_elements = ''.join(modified_html)

                self.ele_dict[i] = ih_elements




class EhndTrans(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()

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

        self.driver = webdriver.Chrome(executable_path='./89/chromedriver.exe',options=options)
        # chromedriver_autoinstaller.install()
        # self.driver = webdriver.Chrome(options=options)

        self.setupUi(self)

        QObject.connect(self.show_trans_btn, SIGNAL('clicked()'), self.showTrans)
        QObject.connect(self.show_ori_btn, SIGNAL('clicked()'), self.showOri)
        QObject.connect(self.go_dev_page, SIGNAL('clicked()'), self.goDevPage)

        self.show()



    def showTrans(self):
        tt = TransThread(self, isTrans=True)
        tt.start()


    def showOri(self):
        tt = TransThread(self, isTrans=False)
        tt.start()
    

    def goDevPage(self):
        open_new('https://blog.naver.com/powerapollon')






if __name__ == "__main__":
    freeze_support()
    import sys
    app = QApplication(sys.argv)
    et = EhndTrans()
    app.exec_()
    et.driver.close()
    sys.exit()
    