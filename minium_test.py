# coding=utf-8
# @Time    : 2020/6/21 11:54 下午
# @Author  : liliang
# @File    : minium_test.py

import minium

class FirstTest(minium.MiniTest):
    # def test_get_system_info(self):
    #     sys_info = self.app.call_wx_method("getSystemInfo")
    #     print(sys_info)
    #     self.assertIn("SDKVersion", sys_info.result.result)

    # def test_get_app(self):
    #     mini = minium.WXMinium()
    #     tiny_app = mini.app
    #     print(tiny_app)
    #
    # def test_enable_log(self):
    #     self.app.enable_log()

    # def test_screen_shot(self):
    #     """路径最前面要加/"""
    #     self.app.switch_tab("/pages/Mine/Mine")
    #     self.app.get_current_page()
    #     # self.app.screen_shot("apiIndexPage")
    #     self.app.go_home()
    #     # self.app.navigate_to("/pages/MerchandiseDetail/MerchandiseDetail")
    #     self.app.redirect_to("/pages/MerchandiseDetail/MerchandiseDetail?uid=80a6e88ad8554d2f8eeb7ba9186d50ea&__key_=15937738125212")
    #     # self.app.enable_log()
    #     # self.app.get_perf_time(entry_types=['navigation'])
    #     # self.app.stop_get_perf_time()
    #     element = self.page.get_element("button", inner_text=u"立即购买")
    #     print(element)



    # def test_exit(self):
    #     # self.app.get_all_pages_path()
    #     self.app.navigate_to("/pages/ShoppingCart/ShoppingCart")


    # def test_element_is_exists(self):
    #     self.app.switch_tab("/pages/Mine/Mine")
    #     contain_button = self.page.element_is_exists("button")
    #     print(contain_button)
    #     contain_textarea = self.page.element_is_exists("textarea")
    #     print(contain_textarea)

    def test_scroll_to(self):

        # self.app.redirect_to("/pages/Index/Index")
        # 500ms内页面滚动到高度为300px的位置
        self.page.scroll_to(3000, 500)
