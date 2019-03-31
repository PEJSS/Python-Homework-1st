from PyQt5.QtWidgets import QApplication
from webofscience import getData, readData, App
import sys

#getData() getData()用来爬取webofscience网站上的论文数据并存为csv文件，由于爬取时间很长，在此注释掉，直接运行GUI界面
#          具体函数见webofscience.py
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App(readData())
    app.exit(app.exec_())