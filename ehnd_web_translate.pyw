#-*- coding:utf-8 -*-


from ctypes import WinError
from genericpath import exists
import subprocess
from PySide2 import QtWidgets
from PySide2 import QtCore
from pydub.audio_segment import AudioSegment
from pyppeteer.launcher import connect
from urllib3.exceptions import ConnectTimeoutError


from module._translate_j2k import *
from module._requirement_func import *
from module.novel_reader import NovelReader
from module.file_trans import FileTranslationThread 


from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import chromedriver_autoinstaller

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.common import exceptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from subprocess import CREATE_NO_WINDOW
from pathlib import Path

import asyncio
import keyboard

import smtplib
from email.mime.text import MIMEText

from furigana.furigana import print_html as sent_to_furi

from UI_MAIN import Ui_MainWindow

import requests
import uuid
import json
import codecs
from pprint import pprint
import imageio
from urllib.request import urlopen

from time import sleep

import numpy as np
from PIL import ImageFont, ImageDraw, Image, ImageGrab
import re

import os
import os.path
from flask import Flask, jsonify, request, render_template
from flask_autoindex import AutoIndex
import ini
from shutil import rmtree

import qdarkstyle

import string
import random
import clipboard

import tkinter as tk
import numpy as np



class StartWebServer(QThread):
    def __init__(self, window):
        QThread.__init__(self)

    def run(self):
        app = Flask(__name__)
        AutoIndex(app, browse_root=os.path.curdir)

        @app.route('/EHND_TRANSLATE', methods=['POST'])
        def WebTransForIMG():
            params = json.loads(request.get_data(), encoding='utf-8')
            print(params)
            j = params['jpn']
            return jsonify({'kor':t_j2k(j)})
        


#         # youdao 번역기 파일을 ehnd 용으로 수정함. 복구 파일은 IMG_OCR_OLD 디렉터리 확인
#         # os.system('cd ./IMG_OCR/ && start /b translate_demo.py --mode web --use-inpainting --use-cuda --translator=youdao')
        app.run()





class LiveVoiceRecognition(QThread):
    update_jpText = Signal(str)
    update_koText = Signal(str)
    

    def __init__(self, window):
        QThread.__init__(self)
        self.window = window
        self.options = Options()
        self.options.add_argument('--use-fake-device-for-media-stream')
        self.options.add_argument('--use-fake-ui-for-media-stream')
        self.options.add_argument('--disable-gpu')
        self.chrome_service = ChromeService(self.window.path)
        self.chrome_service.creationflags = CREATE_NO_WINDOW
        self.driver = Chrome(options=self.options, service=self.chrome_service)
        self.driver.get('http://127.0.0.1:5000/utils/live_voice_recognition.html')
        

    def run(self):
        while True:
            try:
                self.driver.minimize_window()
                if self.window.tabWidget.currentIndex() == 3 and self.window.isLiveTrans.isChecked():
                    mid = self.driver.find_element(By.ID, 'mid').text
                    fin = self.driver.find_element(By.ID, 'fin').text

                    currText = ''
                    if len(mid.replace(' ', '')) == 0:
                        currText = str(fin)
                    else:
                        currText = str(mid)

                    self.update_jpText.emit(currText)
                    self.update_koText.emit(t_j2k(currText))

            except ( exceptions.WebDriverException, exceptions.NoSuchWindowException ):
                self.driver = Chrome(options=self.options, service=self.chrome_service)
                self.driver.get('http://127.0.0.1:5000/utils/live_voice_recognition.html')

            finally:
                sleep(0.5)







class LoadDriverWindow(QThread):
    def __init__(self, window):
        QThread.__init__(self)
        self.window = window

    def run(self):
        while True:
            try:
                cwh = self.window.driver.current_window_handle

                r = get('http://localhost:1972/json').json()
                
                for i in r:
                    if i['type'] == 'page':
                        self.currentHandle = 'CDwindow-' + i['id']

                        if (cwh != self.currentHandle) and (self.window.isAutoTrans.isChecked() or not self.window.st.isRunning()):
                            self.window.driver.switch_to.window(self.currentHandle)

                        break

            except (exceptions.WebDriverException, requests.exceptions.ConnectionError):
                if self.window.isAlive:
                    self.window.driver = Chrome(options=self.window.options, service=self.window.chrome_service)


            except:
                continue









class AutoTrans(QThread):
    def __init__(self, window):
        QThread.__init__(self)
        self.window = window


    def stop(self):
        self.terminate()


    def run(self):
        current_url = self.window.driver.current_url
        while True:
            try:
                sleep(1)
                new_url = self.window.driver.current_url
                if current_url != new_url:
                    self.window.st.stop()
                    self.window.st.isAuto = True
                    self.window.st.start()
                    current_url = new_url
            except:
                continue








class SendFeedback(QThread):
    def __init__(self, window):
        QThread.__init__(self)
        self.window = window

    def run(self):
        self.window.btnSetting(setNum=0)
        try:
            self.window.show_status.setText("건의 중")
            e_sub = self.window.adviceSubject.text()
            e_con = self.window.adviceContent.toPlainText()
            
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login('ehnd.webtrans.feedback@gmail.com', 'ehndwtfb')
            msg = MIMEText(e_con)
            msg['Subject'] = e_sub
            s.sendmail("ehnd.webtrans.feedback@gmail.com", "ehnd.webtrans.feedback@gmail.com", msg.as_string())
            s.quit()

            self.window.show_status.setText("건의 완료")

        except:
            self.window.show_status.setText("건의 실패")


        finally:
            self.window.btnSetting(setNum=1)








class LoadNovelRound(QThread):
    def __init__(self, window):
        QThread.__init__(self)
        self.window = window

    def run(self):
        self.window.btnSetting(setNum=0)
        
        syosetuURL = self.window.syosetuUrl.text()
        nr = NovelReader(syosetuURL)
        self.window.nREADER = nr


        bigTitle = nr.get_big_title()
        smallTitles = nr.get_small_titles()

        if nr.is_short_story():
            item = QListWidgetItem()
            item.setText(smallTitles)
            self.window.novel_idx.addItem(item)

        else:
            for st in smallTitles:
                item = QListWidgetItem()
                item.setText(st)
                self.window.novel_idx.addItem(item)

        self.window.novel_title.setText("제목: " + bigTitle)
        self.window.btnSetting(setNum=1)









class TransThread(QThread):
    changeValue = Signal(int)

    def __init__(self, window, isTrans=True, isAuto=False):
        QThread.__init__(self)
        self.window = window
        self.isTrans = isTrans
        self.isAuto = isAuto
        self.setTerminationEnabled = True
    
    def stop(self):
        if self.isRunning():
            self.window.btnSetting(setNum=1)
            self.window.show_status.setText("번역 중지")
            self.terminate()



    def run(self):
        self.window.btnSetting(setNum=0)
        self.window.count = 0

        try:
            self.waitUntilPageLoaded()

            self.window.sec.setText("")

            if self.isTrans:

                if self.isAuto:
                    self.window.show_status.setText("자동 번역 중")
                else:
                    self.window.show_status.setText("번역 중")

                sleep(1) # 최소한의 window_handle 설정 시간
                start_time = time()
                

                pageList = [None,]
                pageList.extend(self.window.driver.find_elements(By.TAG_NAME, 'frame'))
                pageList.extend(self.window.driver.find_elements(By.TAG_NAME, 'iframe'))
                

                for idx, p in enumerate(pageList):
                    try:
                        if idx != 0:
                            self.window.driver.switch_to.frame(p)


                        self.setRubyTag()

                        textNode = self.getAllTextNode()
                        
                        if idx == 0:
                            self.window.progressBar.setMaximum(len(textNode) + len(pageList)-1)
                            async_loop(self.rt, textNode, False)
                        else:
                            async_loop(self.rt, textNode, True)
                        
                    
                    except exceptions.StaleElementReferenceException:
                        pass

                    
                    except exceptions.NoSuchFrameException:
                        self.window.progressBar.setMaximum(self.window.progressBar.maximum()-1)
                        pass
                        

                    finally:
                        if idx != 0:
                            self.window.driver.switch_to.default_content()
                            self.window.count += 1
                        

                self.window.count = self.window.progressBar.maximum()
                self.window.sec.setText(f"{round(time()-start_time, 3)}초")
                self.window.show_status.setText("번역 성공")
                
            else:
                self.window.driver.refresh()
                self.window.sec.setText("")
                self.window.show_status.setText("원본 보기")

        except Exception as e:
            print(e)
            self.window.show_status.setText("번역 실패")

        finally:
            self.window.btnSetting(setNum=1)




    def waitUntilPageLoaded(self):
        WebDriverWait(self.window.driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')




    def getAllTextNode(self):
        textNode = self.window.driver.find_elements(By.XPATH, '//*[text()[normalize-space()]]')
        textNode += self.window.driver.find_elements(By.TAG_NAME, 'input')
        textNode += self.window.driver.find_elements(By.TAG_NAME, 'img')
        # textNode += self.window.driver.find_elements(By.TAG_NAME, 'source')

        return textNode



    def deleteElement(self, element):
        self.window.driver.execute_script("arguments[0].parentNode.removeChild(arguments[0]);", element)


   
    def setRubyTag(self):
        ruby_rt = self.window.driver.find_elements(By.XPATH, '//rt[text()="・"]')

        lastP = ""
        for i in ruby_rt:
            xp = self.getAbsoluteXPath(i)

            currP = xp.split('/ruby')[0]

            if lastP != currP:
                lastP = currP
                lastRB = self.window.driver.find_element(By.XPATH, xp.replace('/rt', '/rb'))
                
            else:
                try:
                    rb = self.window.driver.find_element(By.XPATH, xp.replace('/rt', '/rb'))
                    self.window.driver.execute_script("arguments[0].innerHTML = arguments[1]", lastRB, lastRB.text+rb.text)
                    self.deleteElement(self.window.driver.find_element(By.XPATH, xp.split('/rt[1]')[0]))

                except:
                    pass
                



    def getAbsoluteXPath(self, element):
        return self.window.driver.execute_script(
            "function absoluteXPath(element) {"+
                    "var comp, comps = [];"+
                    "var parent = null;"+
                    "var xpath = '';"+
                    "var getPos = function(element) {"+
                    "var position = 1, curNode;"+
                    "if (element.nodeType == Node.ATTRIBUTE_NODE) {"+
                    "return null;"+
                    "}"+
                    "for (curNode = element.previousSibling; curNode; curNode = curNode.previousSibling) {"+
                    "if (curNode.nodeName == element.nodeName) {"+
                    "++position;"+
                    "}"+
                    "}"+
                    "return position;"+
                    "};"+

                    "if (element instanceof Document) {"+
                    "return '/';"+
                    "}"+

                    "for (; element && !(element instanceof Document); element = element.nodeType == Node.ATTRIBUTE_NODE ? element.ownerElement : element.parentNode) {"+
                    "comp = comps[comps.length] = {};"+
                    "switch (element.nodeType) {"+
                    "case Node.TEXT_NODE:"+
                    "comp.name = 'text()';"+
                    "break;"+
                    "case Node.ATTRIBUTE_NODE:"+
                    "comp.name = '@' + element.nodeName;"+
                    "break;"+
                    "case Node.PROCESSING_INSTRUCTION_NODE:"+
                    "comp.name = 'processing-instruction()';"+
                    "break;"+
                    "case Node.COMMENT_NODE:"+
                    "comp.name = 'comment()';"+
                    "break;"+
                    "case Node.ELEMENT_NODE:"+
                    "comp.name = element.nodeName;"+
                    "break;"+
                    "}"+
                    "comp.position = getPos(element);"+
                    "}"+

                    "for (var i = comps.length - 1; i >= 0; i--) {"+
                    "comp = comps[i];"+
                    "xpath += '/' + comp.name.toLowerCase();"+
                    "if (comp.position !== null) {"+
                    "xpath += '[' + comp.position + ']';"+
                    "}"+
                    "}"+

                    "return xpath;"+

                    "} return absoluteXPath(arguments[0]);", element)




    async def runTrans(self, i, isFrame):
        try:
            if i.is_displayed():


                inner = i.get_attribute('innerHTML')
                outer = i.get_attribute('outerHTML')


                if outer.startswith('<input'):
                    val = i.get_attribute('value')
                    k = t_j2k(
                        japanese=val,
                        isForceFilter=self.window.isActivateFF.isChecked(),
                        isRemoveOri=self.window.isActivateRO.isChecked(),
                    )

                    isJpn = findJpn.search(val)
                    if isJpn != None:
                        if self.window.isPrintBoth.isChecked():
                            k = f"{val}\n{k}"
                        
                        self.window.driver.execute_script(f"arguments[0].setAttribute('value', arguments[1])", i, k)
                        self.window.printLog(f"번역O -> {val}")

                    else:
                        self.window.printLog(f"번역X -> {inner}")



                elif outer.startswith('<pre'):
                    isJpn = findJpn.search(inner)

                    if isJpn != None:
                        k = t_j2k(
                            japanese=inner,
                            isForceFilter=self.window.isActivateFF.isChecked(),
                            isRemoveOri=self.window.isActivateRO.isChecked(),
                        )

                        if self.window.isPrintBoth.isChecked():
                            jp = inner.split('\n')
                            kr = k.split('\n')


                            new_k = ""
                            for jap, kor in zip(jp, kr):

                                if self.window.isPrintFuri.isEnabled() and self.window.isPrintFuri.isChecked():
                                    try:
                                        furiText = sent_to_furi(jap)
                                        new_k += furiText+'\n'+kor

                                    except:
                                        new_k += jap+'\n'+kor

                                else:
                                    new_k += jap+'\n'+kor

                            k = new_k
                                
                        self.window.printLog(f"번역O -> {inner}")


                    else:
                        self.window.printLog(f"번역X -> {inner}")

                    self.window.driver.execute_script("arguments[0].innerHTML = arguments[1]", i, k)





                elif outer.startswith('<img') or outer.startswith('<source'):
                    if self.window.isTransImage.isChecked():

                        if outer.startswith('<img'):
                            imgSourceAttr = 'src'
                        else:
                            imgSourceAttr = 'srcset'


                        image_file = i.get_attribute(imgSourceAttr)
                        
                        if i.size['width'] < 128 or i.size['height'] < 128:
                            return

                        print(image_file)

                        data = {
                            'url' : image_file
                        }

                        base_url = 'https://touhou.ai/imgtrans'
                        r = requests.post(f'{base_url}/manual-translate', data=data)
                        j = r.json()
                        tr = j['trans_result']
                        src_text = [res['s'] for res in tr]
                        trans_text = t_j2k('\n'.join(src_text)).split('\n')

                        a = []
                        for s, t in zip(src_text, trans_text):
                            a.append({'s': s, 't': t})
                        j['trans_result'] = a


                        r2 = requests.post(f'{base_url}/post-translation-result', json=j)


                        try:
                            j = r2.json()
                            status = j['status']
                            taskId = j['task_id']
                            print(j)
                            
                            img_addr = f'https://touhou.ai/imgtrans/result/{taskId}/final.jpg'
                            
                        except KeyError as ke:
                            print(ke)
                            

                        self.window.driver.execute_script(f"arguments[0].setAttribute(arguments[1], arguments[2])", i, imgSourceAttr, img_addr)

                        print("완료")


        


                
                else:
                    if bool(len(inner.strip())):
                        p_html = PrettifyHtml(inner).split('\n')
                        
                        lastTAG = ""
                        modified_html = ""

                        lastRT_LENGTH = None

                        for ih in p_html:
                            
                            if ih.lstrip().startswith('<'):
                                modified_html += ih
                                lastTAG = ih

                            else:
                                # isJpn = findJpn.search(ih)

                                isRB = lastTAG.lstrip().startswith('<rb>') # 원문
                                isRT = lastTAG.lstrip().startswith('<rt>') # 후리가나
                                
                                

                                # if isJpn != None:
                                if not isRT:
                                    k = t_j2k(
                                        japanese=ih,
                                        isForceFilter=self.window.isActivateFF.isChecked(),
                                        isRemoveOri=self.window.isActivateRO.isChecked(),
                                    )

                                    if isRB:
                                        lastRT_LENGTH = re.sub('[\w]', '・', k)
                                    
                                    
                                    if self.window.isPrintBoth.isChecked():
                                        if self.window.isPrintFuri.isChecked():
                                            try:
                                                if not (isRT or isRB):
                                                    ih = sent_to_furi(ih)
                                            except IndexError:
                                                pass

                                        k = f"{ih}<br>{k}"


                                    modified_html += k
                                    self.window.printLog(f"번역O -> {ih}")

                                
                                else:
                                    ch = set(ih.replace(' ', ''))
                                    if '・' in ch and len(ch)==1:
                                        modified_html += lastRT_LENGTH
                                    else:
                                        modified_html += furiRead(ih)
                                                

                                # else:
                                #     modified_html += ih
                                #     self.window.printLog(f"번역X -> {ih}")

                        
                        self.window.driver.execute_script("arguments[0].innerHTML = arguments[1]", i, modified_html)




        except exceptions.StaleElementReferenceException:
            self.window.printLog("StaleElementReferenceException")


        except IndexError:
            self.window.printLog("FURIGANA INDEXERROR")


        finally:
            if not isFrame:
                self.window.count += 1
                



    async def rt(self, a, isFrame):
        s = [asyncio.ensure_future(self.runTrans(i, isFrame)) for i in a]
        await asyncio.gather(*s)






# MAIN WINDOW
class EhndTrans(QMainWindow, Ui_MainWindow):
    
    def __init__(self):
        super().__init__()

        self.lastUrl = ""
        self.count = 0
        self.wholeCount = 1
        self.isAlive = True
        self.nREADER = None
        self.currentRecognizedText = ""

        self.options = Options()
        self.options.add_argument('--force-dark-mode')
        self.options.add_argument('--remote-debugging-port=1972')
        self.options.add_argument(f"--user-data-dir={Path.home()}\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
        self.options.add_experimental_option("excludeSwitches" , ["enable-automation", "load-extension", "enable-logging"])

        try:
            # os.system('taskkill /f /im chromedriver.exe')
            self.path = chromedriver_autoinstaller.install('./')
            # self.path = os.path.abspath('./92/chromedriver.exe')
            self.chrome_service = ChromeService(self.path)
            self.chrome_service.creationflags = CREATE_NO_WINDOW
            self.driver = Chrome(options=self.options, service=self.chrome_service)

        
        except exceptions.InvalidArgumentException:
            QMessageBox.information(self, '오류 메세지', '프로그램에 의해 열린 모든 크롬 창을 먼저 닫아주세요.', QMessageBox.Yes)
            return

        except IndexError:
            QMessageBox.information(self, '오류 메세지', '크롬을 찾을 수 없습니다. 크롬을 설치해주세요.', QMessageBox.Yes)
            open_new('https://www.google.com/chrome/')
            return


        self.ws = StartWebServer(self)
        self.ws.start()


        self.setupUi(self)
        self.setFont(QFont('나눔고딕OTF', 10))
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyside2())
        self.setWindowIcon(QIcon("./utils/sayo.ico"))

        
        self.config = ini.parse(codecs.open('./utils/Ehnd/ehnd_conf.ini', encoding='utf-8').read())
        try:
            tfd = self.config['CONFIG']['TRANSED_FILE_DIRECTORY']
        except KeyError:
            tfd = os.getcwd()
        finally:
            self.transed_file_dir.setText(tfd)
    

        self.st = TransThread(self, isTrans=True)
        self.so = TransThread(self, isTrans=False)
        self.at = AutoTrans(self)
        self.sfb = SendFeedback(self)

        self.ftt = FileTranslationThread(self, self.path)
        self.lnr = LoadNovelRound(self)


        QObject.connect(self.show_trans_btn, SIGNAL('clicked()'), self.showTrans)
        QObject.connect(self.show_ori_btn, SIGNAL('clicked()'), self.showOri)
        QObject.connect(self.go_dev_page, SIGNAL('clicked()'), self.goDevPage)
        QObject.connect(self.stop_trans_btn, SIGNAL('clicked()'), self.stopTrans)
        QObject.connect(self.adviceSubmitBtn, SIGNAL('clicked()'), self.sendEmailFeedback)
        self.isAutoTrans.stateChanged.connect(self.autoTrans)
        self.isActivateSK.stateChanged.connect(self.setShortKey)
        self.isPrintBoth.stateChanged.connect(self.setFuri)

        QObject.connect(self.file_select_btn, SIGNAL('clicked()'), self.selectFiles)
        QObject.connect(self.select_file_dir_btn, SIGNAL('clicked()'), self.selectTransedFileDir)
        QObject.connect(self.file_translate_btn, SIGNAL('clicked()'), self.runFileTrans)
        QObject.connect(self.file_translate_stop_btn, SIGNAL('clicked()'), self.ftt.stop)
        QObject.connect(self.open_file_dir_btn, SIGNAL('clicked()'), self.openFolder)
        QObject.connect(self.clear_fileList_btn, SIGNAL('clicked()'), self.SelectedFileList.clear)
        self.select_all.stateChanged.connect(self.checkAllList)

        QObject.connect(self.normalTransBtn, SIGNAL('clicked()'), self.normalTrans)
        QObject.connect(self.loadSyosetu, SIGNAL('clicked()'), self.load_novel_round)
        self.novel_idx.currentItemChanged.connect(self.load_novel_content)

        self.fontComboBox.currentIndexChanged.connect(self.changeFontAndSize)
        self.fontSizeBox.valueChanged.connect(self.changeFontAndSize)

        QObject.connect(self.prevBtn, SIGNAL('clicked()'), self.load_prev_content)
        QObject.connect(self.nextBtn, SIGNAL('clicked()'), self.load_next_content)

        QObject.connect(self.copyKtext, SIGNAL('clicked()'), self.copyResult)

       


        self.lvr = LiveVoiceRecognition(self)
        self.lvr.update_jpText.connect(self._handle_live_trans_jp)
        self.lvr.update_koText.connect(self._handle_live_trans_ko)
        self.lvr.start()
        

        self.prevBtn.setDisabled(True)
        self.nextBtn.setDisabled(True)


        self.isActivateSK.setChecked(True)
        self.setFuri()


        self.setFixedSize(self.size())
        

        self.btnSetting(setNum=1)

        self.ldw = LoadDriverWindow(self)
        self.ldw.start()


        self.timer = QBasicTimer()        
        self.timer.start(777, self)

        self.show()




    @Slot(str)
    def _handle_live_trans_jp(self, ja_text): self.japaneseText.setText(ja_text)

    @Slot(str)
    def _handle_live_trans_ko(self, ko_text): self.koreanText.setText(ko_text)


    def copyResult(self):
        clipboard.copy(self.koreanText.toPlainText())
        



    def changeFontAndSize(self):
        currFont = self.fontComboBox.currentText()
        currSize = self.fontSizeBox.value()
        self.syosetuBrowser.setFont(QFont(currFont, currSize))



    def openFolder(self):
        os.system('explorer \"{}\"'.format(self.transed_file_dir.text().replace('/', '\\')))


    
    def timerEvent(self, event):
        self.progressBar.setValue(self.count)


    def closeEvent(self, event):
        self.isAlive = False


    def showTrans(self):
        self.st.stop()
        self.st.start()


    def stopTrans(self):
        self.st.stop()


    def showOri(self):
        self.so.start()
    

    def goDevPage(self):
        open_new('https://blog.naver.com/PostList.nhn?blogId=powerapollon&categoryNo=33&from=postList')



    def autoTrans(self):
        if self.isAutoTrans.isChecked():
            self.at.start()
        else:
            self.at.stop()
    

    def sendEmailFeedback(self):
        self.sfb.start()
    

    def setShortKey(self):
        if self.isActivateSK.isChecked():
            keyboard.add_hotkey("alt+t", self.showTrans)
            keyboard.add_hotkey("alt+o", self.showOri)
            keyboard.add_hotkey("alt+s", self.stopTrans)
        else:
            keyboard.remove_all_hotkeys()


    def setFuri(self):
        if not self.isPrintBoth.isChecked():
            self.isPrintFuri.setEnabled(False)
        else:
            self.isPrintFuri.setEnabled(True)



    def printLog(self, msg):
        if self.isPrintLog.isChecked():
            self.log_browser.append(msg)
            self.log_browser.verticalScrollBar().setValue(self.log_browser.verticalScrollBar().maximum())



    def selectFiles(self):
        fileList = QFileDialog.getOpenFileNames(self, 'Open File', '', 'ALL Files(*);; Text File(*.txt);; MP3 File(*.mp3);; MS Word file(*.docx);; MS Presentation file(*.pptx);; MS EXCEL(*.xlsx);; PDF(*.pdf);; PNG IMAGE(*.png);; JPG IMAGE(*.jpg);; MP4 VIDEO(*.mp4)')[0]

        for fl in fileList:
            item = QListWidgetItem()
            item.setText(fl)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Checked)
            self.SelectedFileList.addItem(item)




    def checkAllList(self):
        for idx in range(self.SelectedFileList.count()):
            if self.select_all.isChecked():
                
                self.SelectedFileList.item(idx).setCheckState(Qt.Checked)
            else:
                self.SelectedFileList.item(idx).setCheckState(Qt.Unchecked)

        




    def selectTransedFileDir(self):
        dir_loc = QFileDialog.getExistingDirectory(self, 'Find Folder')
        if len(dir_loc) == 0:
            return 
            
        self.config['CONFIG']['TRANSED_FILE_DIRECTORY'] = dir_loc

        r = codecs.open('./utils/Ehnd/ehnd_conf.ini', 'r', encoding='utf-8').read().split('\n')
        for i, s in enumerate(r):
            if 'TRANSED_FILE_DIRECTORY=' in s:
                r[i] = f'TRANSED_FILE_DIRECTORY={dir_loc}'
                break

        codecs.open('./utils/Ehnd/ehnd_conf.ini', 'w', encoding='utf-8').write('\n'.join(r))
        self.transed_file_dir.setText(dir_loc)




    def runFileTrans(self):
        self.ftt.start()





    def normalTrans(self):
        self.btnSetting(setNum=0)
        jpText = self.japaneseText.toPlainText()
        start_time = time()
        krText = t_j2k(jpText)
        self.koreanText.clear()
        self.koreanText.append(krText)
        self.sec.setText(f"{round(time()-start_time, 3)}초")
        self.show_status.setText('일반 번역 완료')
        self.btnSetting(setNum=1)



    def load_novel_round(self):
        self.novel_idx.clear()
        self.syosetuBrowser.clear()
        self.prevBtn.setDisabled(True)
        self.nextBtn.setDisabled(True)
        self.lnr.start()

    

    def load_novel_content(self, item):
        if self.novel_idx.currentRow()+1 == self.novel_idx.count(): self.nextBtn.setDisabled(True)
        else: self.nextBtn.setDisabled(False)

        if self.novel_idx.currentRow() == 0: self.prevBtn.setDisabled(True)
        else: self.prevBtn.setDisabled(False)


        self.btnSetting(setNum=0)
            
        syosetuURL = self.syosetuUrl.text()

        curr_idx = self.novel_idx.currentRow()
        novel_content = self.nREADER.get_content(novel_round=curr_idx)
        self.syosetuBrowser.clear()

        self.show_status.setText('소설 번역 중')
        start_time = time()
        j = novel_content
        k = t_j2k(
            japanese=j.replace('(・)', ''),
            isForceFilter=self.n_isActivateFF.isChecked(),
            isRemoveOri=self.n_isActivateRO.isChecked(),
        )

        if self.n_isPrintBoth.isChecked():
            jp = j.split('\n')
            kr = k.split('\n')

            new_k = ""
            for jap, kor in zip(jp, kr):
                new_k += jap+'\n'+kor + "\n\n"

        else:
            new_k = k

        new_k = f'소제목: {self.novel_idx.currentItem().text()}\n{"-"*75}\n\n\n{new_k}'
        self.syosetuBrowser.setPlainText(new_k)

        self.sec.setText(f"{round(time()-start_time, 3)}초")
        self.show_status.setText('소설 번역 완료')

        self.btnSetting(setNum=1)

            



    def load_prev_content(self):
        self.novel_idx.setCurrentRow(int(self.novel_idx.currentRow()) - 1)

    def load_next_content(self):
        self.novel_idx.setCurrentRow(int(self.novel_idx.currentRow()) + 1)

    


    def btnSetting(self, setNum):
        if setNum == 0:
            self.show_trans_btn.setDisabled(True)
            self.show_ori_btn.setDisabled(True)
            self.go_dev_page.setDisabled(True)
            self.adviceSubmitBtn.setDisabled(True)
            self.file_select_btn.setDisabled(True)
            self.file_translate_btn.setDisabled(True)
            self.normalTransBtn.setDisabled(True)
            self.loadSyosetu.setDisabled(True)
            self.file_translate_stop_btn.setDisabled(False)
            self.stop_trans_btn.setDisabled(False)
            

        if setNum == 1:
            self.show_trans_btn.setDisabled(False)
            self.show_ori_btn.setDisabled(False)
            self.go_dev_page.setDisabled(False)
            self.adviceSubmitBtn.setDisabled(False)
            self.file_select_btn.setDisabled(False)
            self.file_translate_btn.setDisabled(False)
            self.normalTransBtn.setDisabled(False)
            self.loadSyosetu.setDisabled(False)
            self.file_translate_stop_btn.setDisabled(True)
            self.stop_trans_btn.setDisabled(True)




def checkUpdate(currentVer: int):
    lastVer = get("https://github.com/kdrkdrkdr/EhndWebTranslate/releases/latest").url.split('/')[-1]
    if int(lastVer) > currentVer:
        open_new("https://github.com/kdrkdrkdr/EhndWebTranslate/releases/latest")
        return False
    else:
        return True

    


if __name__ in '__main__':
    import sys, ctypes
    currentVersion = 211020

    ctypes.windll.user32.SetProcessDPIAware()
    QtWidgets.QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

    # DeleteFileInTEMP() # 사진 파일 한 번 다 지워주고~

    app = QApplication(sys.argv)
    et = EhndTrans()

    # Ehnd 한 번 실행하는걸로 초반 속도 감소 제거 => Initializing
    t_j2k(codecs.open('./utils/initialize_text.txt', 'r', encoding='utf-8').read())

    if not checkUpdate(currentVersion):
        QMessageBox.information(et, '업데이트 공지', '최신 버전이 아닙니다. 업데이트 해주세요.', QMessageBox.Yes)
        et.setWindowTitle(f"Ehnd 웹 번역 {currentVersion} - 최신 버전이 아닙니다. 업데이트 해주세요.")
    else:
        et.setWindowTitle(f"Ehnd 웹 번역 {currentVersion} - 최신 버전입니다.")

    app.exec_()
    et.driver.quit()
    et.lvr.driver.quit()
    # os.system('taskkill /f /im server32-windows.exe') x64 인 경우
    os.system('taskkill /f /im chromedriver.exe')
    os.system('taskkill /f /im python.exe')
    sys.exit()
    