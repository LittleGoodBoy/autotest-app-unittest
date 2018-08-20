import unittest
import os,sys

BASEPATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,BASEPATH)

from lib.appController import AppController
from lib.path import APPCASE, APPREPORT  # 测试用例及报告路径
from lib.HTMLTestAppRunner import HTMLTestRunner # 用于执行测试套件,生成测试用例


'''
    主函数
'''
class Main(object):
    def __init__(self):
        # 实例化AppController 初始化相关配置信息
        self.controller = AppController()
        # 获取配置信息中的设备名称  即通过adb devices查看到的设备id
        self.deviceName = self.controller.deviceName

    def run(self):
        # 开启一个进程来执行appium server的启动命令
        self.controller.start_server()

        # 判断appium server是否启动成功
        if self.controller.test_server():
            # 如果成功则获取设备连接对象driver并放到队列中
            self.controller.start_driver()
            # 实例化一个测试套件
            suit = unittest.TestSuite()
            '''
                discover方法里面有三个参数：
                    -case_dir:      这个是待执行用例的目录。
                    -pattern：      这个是匹配脚本名称的规则，test*.py意思是匹配test开头的所有脚本。
                    -top_level_dir：这个是顶层目录的名称，一般默认等于None就行了。
            '''
            # 获取指定路径下的所有测试用例
            cases = unittest.defaultTestLoader.discover(APPCASE)
            # 遍历测试用例,放到测试套件中
            for case in cases:
                suit.addTest(case)
            # 以二进制只写的方式打开指定路径下的文件(文件不存在则自动创建)
            f = open(APPREPORT.format('{}.html'.format(self.deviceName)), 'wb')
            # 实例化HTMLTestRunner对象(生成的报告的title,和描述description)
            runner = HTMLTestRunner(f, verbosity=1, title=u'测试报告', description=u'用例执行情况：')
            # 运行测试套件中的所有测试用例
            runner.run(suit)
            # 刷新数据到文件
            f.flush()
            # 关闭文件流
            f.close()

if __name__ == '__main__':
    Main().run()
