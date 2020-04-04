# 实现 代码启动服务

# 等服务启动成功后  启动driver
from appium import webdriver
from lib.tool import Tool
from lib.path import LOGPATH
import os
import subprocess
from lib.logger import logger
import time
import queue

# 设备操作对象的一个队列
driver_queue = queue.Queue()
class AppController(object):
    def __init__(self):
        self.tool = Tool()
        # 获取所有配置信息 字典格式
        self.yml = self.tool.app_data
        self.device_type = self.yml.get('device_type')
        self.tester = self.yml.get('tester')
        self.devices = self.yml.get('devices')
        self.deviceName = self.devices.get(self.device_type)[0].get('deviceName')
        self.ports = []

    # 每次启动前都要kill掉所有的进程
    # 启动appium server
    def start_server(self):
        "appium -a {ip} -p {port} -U {deviceName} -g {log}"
        # 获取一个手机的信息
        device = self.devices.get(self.device_type)[0]
        # 添加端口号ports中 为校验服务是否启动成功做准备
        self.ports.append(device.get('port'))
        # 拼接log路径
        log_path = os.path.join(LOGPATH,device.get('name')+'.log')
        # 拼接启动命令
        command = "appium -a {ip} -p {port} -U {deviceName} -g {log}".format(
            ip=device.get('ip'),
            port=device.get('port'),
            deviceName=device.get('deviceName'),
            log=log_path
        )
        logger.debug('启动服务的命令：%s'%command)
        # 多进程的方式执行命令
        subprocess.Popen(command, stdout=open(log_path, 'a+'), stderr=subprocess.PIPE, shell=True)

    # 校验appium服务是否启动
    def test_server(self):
        # 通过命令 一遍一遍的查找 如果有返回值则代表成功启动 没有返回值代表启动失败
        "netstat -ano | findstr 9001"
        while True:
            c = subprocess.getoutput('netstat -ano | findstr %s'%self.ports[0])
            if c:
                logger.debug('端口：【%s】 启动成功'%self.ports[0])
                break
            else:
                logger.debug('端口：【%s】 启动失败   5秒后重试' % self.ports[0])
                time.sleep(5)
        return True

    # 启动driver
    def start_driver(self):
        # 1、拿到初始化app的信息(tester)
        # 2、拿到手机信息
        # 3、拼我们的url 和参数

        # 获取手机信息
        device = self.devices.get(self.device_type)[0]
        # 合并手机信息和tester信息
        self.tester.update(device)
        # 连接appium服务,实例化一个设备操作对象
        driver = webdriver.Remote('http://{ip}:{port}/wd/hub'.format(
            ip=device.get('ip'),
            port=device.get('port')
        ), self.tester)  # self.tester为appium连接参数
        # 将driver放到队列中
        driver_queue.put(driver)

if __name__ == '__main__':
    controller = AppController()
    # 先启动服务
    controller.start_server()
    # 如果服务启动成功在启动drvier
    if controller.test_server():
        # 启动driver
        controller.start_driver()
