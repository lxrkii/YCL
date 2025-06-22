import sys
from PyQt5.QtWidgets import QApplication
from diary_app import DiaryApp

if __name__ == '__main__':
    app = QApplication(sys.argv)
    diary = DiaryApp()
    diary.show()
    sys.exit(app.exec_())
