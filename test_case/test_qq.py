# case 基于什么? unittest
import unittest
# 还要用到page
from page.page import Page


class QQDemo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.page= Page()

    @classmethod
    def tearDownClass(cls):
        cls.page.quit()

    def test_a_url(self):
        self.page.url()
