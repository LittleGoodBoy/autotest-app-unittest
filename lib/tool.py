import json
import os
from lib.path import APPPATH
from lib.path import APPPICTUREPATH, APPERROR
import threading
import yaml
from lib.logger import logger


'''
    错误截图工具类
'''
class Tool(object):
    @property
    def app_data(self):
        with open(APPPATH, 'rb') as f:
            data = yaml.load(f)
        return data

    def app_error_picture(self):
        app_list = os.listdir(APPPICTUREPATH)
        app_picture = []
        for item in app_list:
            if item.endswith('.jpg'):
                app_picture.append((APPERROR + item,))
        return app_picture

    @staticmethod
    def app_clear():
        app_list = os.listdir(APPPICTUREPATH)
        logger.debug('上次执行的未删除的图片：%s' % app_list)
        for p in app_list:
            if p.endswith('jpg') or p.endswith('png'):
                os.remove(os.path.join(APPPICTUREPATH, p))

if __name__ == '__main__':
    Tool().app_clear()
