from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
from UI import Ui_Form
from PyQt5.QtWidgets import QApplication, QWidget
from cloud_api import CloudApi
import matplotlib.pyplot as plt


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.tempvalue = []
        self.x_time = []
        self.ui = Ui_Form()
        self.ui.setupUi(self)  # 调用setup来加载界面

        # 初始化云平台
        self.cloudapi = CloudApi()
        self.cloudapi.resp_access_token('19912345638', '123456')

        # 初始化定时器
        self.timer = QTimer(self)  # 传递 self 作为父对象
        self.timer.timeout.connect(self.get_value)  # 正确地连接 timeout 信号

        # 获取数据
        self.get_value()
        # 数据更新
        self.refresh_data()

        # 控制灯的开关
        self.light_flag = 0  # 默认为零，设置灯的状态
        self.ui.button.clicked.connect(self.control_light)

    def get_value(self):
        """
        获取云平台数据
        :return:
        """
        data = self.cloudapi.resp_get_device(devids=1074613)
        print(data)
        for item in data:
            if item['ApiTag'] == 'wd':
                self.ui.temp_value.setText(str(item['Value']) + '℃')
                self.tempvalue.append(item['RecordTime'][-5])
                self.x_time.append(item['Value'])
            if item['ApiTag'] == 'SD':
                self.ui.humi_value.setText(str(item['Value']) + 'rh')
            if item['ApiTag'] == 'jiguang':
                if item['Value'] == 0:  # 激光，没人把light_flag = 0打开灯
                    self.ui.people.setPixmap(QPixmap("images/people_gray.png"))
                    self.light_flag = 0
                    self.control_light()
                else:  # 激光，有人吧light_flag = 1 灯关闭
                    self.ui.people.setPixmap(QPixmap("images/people_green.png"))
                    self.light_flag = 1
                    self.control_light()

        # 获取完后更新折线图
        self.draw_char()

    def control_light(self):
        if self.light_flag == 0:
            # 打开灯
            self.ui.light.setPixmap(QPixmap("images/lampon.png"))
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("images/switch_on.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.button.setIcon(icon)  # 设置按钮图标
            self.light_flag = 1
        else:
            # 关闭灯
            self.ui.light.setPixmap(QPixmap("images/lampoff.png"))
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("images/switch_off.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.button.setIcon(icon)  # 设置按钮图标
            self.light_flag = 0
        # 控制云平台的打开与关闭
        self.cloudapi.resp_cmd_device(1074613, 'LED', self.light_flag)

    def refresh_data(self):
        self.timer.setInterval(5000)  # 设置定时器的间隔时间为 5000 毫秒（5 秒）
        self.timer.timeout.connect(self.get_value)  # 正确地连接 timeout 信号
        self.timer.start()  # 启动定时器

    def draw_char(self):
        plt.figure(1, (3.9, 2.8))
        plt.title("温度-时间折线图")
        plt.xlabel('时间')
        plt.ylabel('值')

        plt.plot(self.x_time, self.tempvalue, linestyle='-', color='b')
        plt.rcParams['font.sans-serif'] = ['FangSong']
        plt.rcParams['axes.unicode_minus'] = False
        plt.savefig("temp_char,png", dpi=300, transparent=True)

        self.ui.chart.setPixmap(QPixmap("temp_char,png"))


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
