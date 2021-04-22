#-*- coding:utf-8 -*-


from module._translate_j2k import t_j2k
from module._requirement_func import *

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import chromedriver_autoinstaller

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.common import exceptions
from selenium.webdriver.chrome.service import Service as ChromeService

from subprocess import CREATE_NO_WINDOW

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
        # self.window.log_browser.append("LoadDriverWindow")



class AutoTrans(QThread):
    def __init__(self, window):
        QThread.__init__(self)
        self.window = window


    def stop(self):
        self.terminate()


    def run(self):
        current_url = self.window.driver.current_url
        while True:
            sleep(1)
            new_url = self.window.driver.current_url
            if current_url != new_url:
                self.window.st.stop()
                self.window.st.isAuto = True
                self.window.st.start()
                current_url = new_url



class TransThread(QThread):
    def __init__(self, window, isTrans=True, isAuto=False):
        QThread.__init__(self)
        self.window = window
        self.isTrans = isTrans
        self.isAuto = isAuto
        self.setTerminationEnabled = True
        

    def stop(self):
        self.window.btnSetting(setNum=1)
        self.window.show_status.setText("번역 중지")
        self.terminate()


    def run(self):
        self.window.btnSetting(setNum=0)
        try:
            start_time = time()
            self.window.sec.setText("")

            if self.isTrans:
                if self.isAuto:
                    self.window.show_status.setText("자동 번역 중")
                else:
                    self.window.show_status.setText("번역 중")

                a = self.window.driver.find_elements_by_xpath('.//*[normalize-space(text())]')
                async_loop(self.rt, a)
                self.window.sec.setText(f"{round(time()-start_time, 3)}초")
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
                                k = t_j2k(japanese=ih)
                                if self.window.isPrintBoth.isChecked(): 
                                    # k = f"{ih}({k})"
                                    k = f"{ih}<br>{k}"
                                modified_html.append(k)
                                self.window.printLog(f"번역O -> {ih}")

                            else:
                                modified_html.append(ih)
                                self.window.printLog(f"번역X -> {ih}")
                                
                                

                    ih_elements = ''.join(modified_html)

                    self.window.driver.execute_script("arguments[0].outerHTML = arguments[1]", i, ih_elements)


        except exceptions.StaleElementReferenceException:
            # self.window.printLog("StaleElementRefernceException")
            pass


    async def rt(self, a):
        s = [asyncio.ensure_future(self.runTrans(i)) for i in a]
        await asyncio.gather(*s)



class EhndTrans(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()

        self.lastUrl = ""
        


        options = Options()
        options.add_experimental_option("excludeSwitches" , ["enable-automation", "load-extension", "enable-logging"])

        # self.driver = Chrome(executable_path='./89/chromedriver.exe',options=options)

        path = chromedriver_autoinstaller.install('./')
        chrome_service = ChromeService(path)
        chrome_service.creationflags = CREATE_NO_WINDOW


        self.driver = Chrome(options=options, service=chrome_service)
        
        self.driver.get("https://www.google.com")

        self.setupUi(self)


        self.show_trans_btn.clicked.connect(self.showTrans)
        self.show_ori_btn.clicked.connect(self.showOri)
        self.go_dev_page.clicked.connect(self.goDevPage)
        self.reloadBtn.clicked.connect(self.reloadWindow)
        self.stop_trans_btn.clicked.connect(self.stopTrans)
        self.window_list.currentIndexChanged.connect(self.setWindow)
        self.isAutoTrans.stateChanged.connect(self.autoTrans)
        

        self.st = TransThread(self, isTrans=True)
        self.so = TransThread(self, isTrans=False)
        self.ldw = LoadDriverWindow(self)
        self.at = AutoTrans(self)


        self.btnSetting(setNum=1)
        self.reloadWindow()

        self.show()



    def showTrans(self):
        self.st.start()

    def stopTrans(self):
        self.st.stop()


    def showOri(self):
        self.so.start()
    

    def goDevPage(self):
        open_new('https://blog.naver.com/PostList.nhn?blogId=powerapollon&categoryNo=33&from=postList')


    def reloadWindow(self):
        self.ldw.start()


    def setWindow(self):
        dw_handles = self.driver.window_handles
        self.driver.switch_to.window(dw_handles[self.window_list.currentIndex()])


    def autoTrans(self):
        if self.isAutoTrans.isChecked():
            self.at.start()
        else:
            self.at.stop()
    
    

    def printLog(self, msg):
        if self.isPrintLog.isChecked():
            self.log_browser.append(msg)
            self.log_browser.verticalScrollBar().setValue(self.log_browser.verticalScrollBar().maximum())

    
    def btnSetting(self, setNum):
        if setNum == 0:
            self.show_trans_btn.setDisabled(True)
            self.show_ori_btn.setDisabled(True)
            self.window_list.setDisabled(True)
            self.reloadBtn.setDisabled(True)
            self.go_dev_page.setDisabled(True)
            self.isPrintBoth.setDisabled(True)
            self.isAutoTrans.setDisabled(True)
            self.stop_trans_btn.setDisabled(False)

        if setNum == 1:
            self.show_trans_btn.setDisabled(False)
            self.show_ori_btn.setDisabled(False)
            self.window_list.setDisabled(False)
            self.reloadBtn.setDisabled(False)
            self.go_dev_page.setDisabled(False)
            self.isPrintBoth.setDisabled(False)
            self.isAutoTrans.setDisabled(False)
            self.stop_trans_btn.setDisabled(True)



if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    et = EhndTrans()
    app.exec_()
    et.driver.quit()
    sys.exit()