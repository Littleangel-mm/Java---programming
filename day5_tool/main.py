from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5 import QtCore
from ui import Ui_Form  # 替换成你的模块名称
from threading import Thread
from threading import Event
from tool import download
import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtCore import QPoint, Qt
from qfluentwidgets import InfoBarIcon, InfoBar, PushButton, setTheme, Theme, FluentIcon, InfoBarPosition, InfoBarManager
import requests

class MyForm(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.max.setText("")
        self.ui.small.setText("")
        
        # 连接按钮的点击事件到相应的处理方法
        self.ui.xz.clicked.connect(lambda:self.on_pushButton_clicked(self.ui))
        self.ui.qk.clicked.connect(lambda:self.clear_clicked(self.ui))
    

    def download_clicked(self,ui):
        Thread(target=download, args=(ui,)).start()
            


    # 下载按钮事件
    def on_pushButton_clicked(self,ui):
        url = ui.LineEdit.text()
        try:
            the_filesize = requests.get(url, stream=True).headers['Content-Length']
            the_filepath = os.getcwd() + "/" + url.split("/")[-1]
            the_fileobj = open(the_filepath, 'wb')
            #### 创建下载线程
            self.downloadThread = downloadThread(url, the_filesize, the_fileobj, buffer=10240)
            self.downloadThread.download_proess_signal.connect(self.set_progressbar_value)
            self.downloadThread.start()
        except Exception as e:
            self.cw("提示", f"下载地址错误！{e}")

    # 设置进度条
    def set_progressbar_value(self, value):
        self.ui.jdt.setValue(value)
        if value == 100:
            self.ts("提示", "下载完成！")
            #QMessageBox.information(self, "提示", "下载成功！")
            return


    def clear_clicked(self,ui):
        event = Event()
        event.set()
        ui.LineEdit.clear()
        ui.jdt.setValue(0)
        self.ts("提示","清空完成")


    def ts(self, title, text):
        # convenient class mothod
        InfoBar.success(
            title=title,
            content=text,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            # position='Custom',   # NOTE: use custom info bar manager
            duration=2000,
            parent=self
        )
    
    def cw(self, title, text):
        InfoBar.error(
            title=title,
            content=text,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM_RIGHT,
            duration=-1,    # won't disappear automatically
            parent=self
        )


##################################################################
#下载线程
##################################################################
class downloadThread(QThread):
    download_proess_signal = pyqtSignal(int)                        #创建信号

    def __init__(self, url, filesize, fileobj, buffer):
        super(downloadThread, self).__init__()
        self.url = url
        self.filesize = filesize
        self.fileobj = fileobj
        self.buffer = buffer


    def run(self):
        try:
            rsp = requests.get(self.url, stream=True)                #流下载模式
            offset = 0
            for chunk in rsp.iter_content(chunk_size=self.buffer):
                if not chunk: break
                self.fileobj.seek(offset)                            #设置指针位置
                self.fileobj.write(chunk)                            #写入文件
                offset = offset + len(chunk)
                proess = offset / int(self.filesize) * 100
                self.download_proess_signal.emit(int(proess))        #发送信号
            #######################################################################
            self.fileobj.close()    #关闭文件
            self.exit(0)            #关闭线程


        except Exception as e:
            print(e)



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MyForm()
    window.show()
    window.setFixedSize(window.width(), window.height())
    sys.exit(app.exec_())