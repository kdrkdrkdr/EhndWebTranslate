pyside2-uic.exe .\UI_MAIN.ui -o .\UI_MAIN.py



@REM echo if __name__ == "__main__": >> UI_MAIN.py
@REM echo     import sys >> UI_MAIN.py
@REM echo     app = QApplication(sys.argv) >> UI_MAIN.py
@REM echo     form = QMainWindow() >> UI_MAIN.py
@REM echo     ui = Ui_MainWindow() >> UI_MAIN.py
@REM echo     ui.setupUi(form) >> UI_MAIN.py
@REM echo     form.show() >> UI_MAIN.py
@REM echo     sys.exit(app.exec_()) >> UI_MAIN.py
