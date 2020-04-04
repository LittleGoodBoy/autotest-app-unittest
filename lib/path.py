import os

'''
    定义相关路径变量
'''
# 根路径
BASEPATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# app测试配置信息yaml文件路径
APPPATH = os.path.join(BASEPATH, 'conf', 'appController.yaml')

# 日志输出文件的绝对路径
LOGPATH = os.path.join(BASEPATH, 'log')
SYSTEMPATH = os.path.join(LOGPATH, 'server.log')

# 测试报告路径
APPREPORT = os.path.join(BASEPATH, 'report', '{}')

# 错误截图目录路径
APPPICTUREPATH = BASEPATH + os.path.sep + 'report' + os.path.sep + 'app_picture' + os.path.sep

# 测试用例存放目录路径
APPCASE = os.path.join(BASEPATH, 'test_case')

# 生成报告时的地址
APPERROR = '../report/app_picture/'