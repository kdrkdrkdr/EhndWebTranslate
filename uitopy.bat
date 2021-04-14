pyside2-uic.exe .\UI_MAIN.ui -o .\UI_MAIN.py



echo if __name__ == "__main__": >> UI_MAIN.py
echo     import sys >> UI_MAIN.py
echo     app = QApplication(sys.argv) >> UI_MAIN.py
echo     form = QMainWindow() >> UI_MAIN.py
echo     ui = Ui_MainWindow() >> UI_MAIN.py
echo     ui.setupUi(form) >> UI_MAIN.py
echo     form.show() >> UI_MAIN.py
echo     sys.exit(app.exec_()) >> UI_MAIN.py
