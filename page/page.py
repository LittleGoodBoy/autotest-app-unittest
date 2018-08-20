from lib.appController import driver_queue
from lib.pyapp import Pyapp


# 这里封装了 app的所有页面定位元素
# 提供一些共有功能
class BasePage(object):
    def __init__(self):
        # 通过对列 取drvier
        driver = driver_queue.get()
        # 实例化pyapp 并且获取到 pyapp的实例对象
        self.pyapp = Pyapp(driver)

    def quit(self):
        self.pyapp.quit()


class UrlPage(BasePage):
    def url(self):
        css = 'id=>url'
        self.pyapp.type(css, 'http://ui.imdsx.cn')


class Page(UrlPage):
    pass
