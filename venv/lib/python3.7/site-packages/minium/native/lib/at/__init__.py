# encoding:utf-8
import os.path
import json
from at.apkapi import AppApi
from at.core.uixml import UiView
from at.core.adbwrap import AdbWrap
from at.core.stf.minitouch import MiniTouch
from at.core import config
from at.core import element, accesshelper, javadriver, uidevice
from at.core import accesshelper
from at.utils import decorator
from at.eventmonitor import EventMonitor
from at.jlogcat import JLogCat


uiautomator_version = config.UIAUTOMATOR2


def build_info():
    config_path = os.path.join(os.path.dirname(__file__), "build_info.json")
    if not os.path.exists(config_path):
        return {}
    else:
        with open(config_path, "rb") as f:
            version = json.load(f)
            return version


class At(object):
    at_cache = {}
    device_status = {}

    def __init__(self, serial=None, display_id=None, event_path=None):
        if serial is None:
            serial = AdbWrap.get_default_serial()

        self.serial = serial
        self.adb = AdbWrap.apply_adb(serial)
        self.apkapi = AppApi(self.adb)
        self.java_driver = core.javadriver.JavaDriver.apply_driver(
            serial, uiautomator_version
        )
        element.Element.bind_java_driver(self.java_driver)
        self._logcat = None
        self.device = uidevice.PyUiDevice(self.java_driver)
        self.access_helper = accesshelper.AccessHelper(self.java_driver)
        self.event_monitor = EventMonitor(self.java_driver)
        At.at_cache[serial] = self
        if event_path:
            minitouch = MiniTouch(self.serial, event_path, display_id)
            self.device.set_input_interceptor(minitouch)
            self.input_interceptor = minitouch
        else:
            self.input_interceptor = None

    @property
    def logcat(self):
        if not self._logcat:
            self._logcat = JLogCat(self.adb)
            self._logcat.setDaemon(True)
            self._logcat.start()
        return self._logcat

    @classmethod
    def set_uiautomator_version(cls, version):
        logger.info("set uiautomator_version=%s", version)
        cls.uiautomator_version = version

    def register_hook(self, hook):
        self.java_driver.hook_list.clear()
        self.java_driver.register(hook)

    @property
    def e(self):
        elem = element.Element(jd_instance=self.java_driver)
        if self.input_interceptor:
            elem.use_custom()
            elem.set_input_interceptor(self.input_interceptor)
        return elem

    def release(self):
        core.javadriver.JavaDriver.release_driver(self.serial)
        if self._logcat:
            self._logcat.stop()

    def click_image(self, image_path):
        import at.vision.template_match

        temp_path = "temp.png"
        source_path = self.device.screen_shot(temp_path)
        r = at.vision.template_match.search(image_path, source_path)
        if not r:
            raise RuntimeError("search %s failed" % image_path)
        else:
            self.device.click_on_point(r["results"][0], r["results"][1])


if __name__ == "__main__":
    import logging
    import logging.config

    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger()
    uiautomator_version = config.UIAUTOMATOR2
    a = At()

    try:
        a.apkapi.add_gallery("/Users/mmtest/Downloads/222.png")
        # print a.e.text(u"消息免打扰").parent().instance(2).child().rid("com.tencent.mm:id/k2").get_desc()
    finally:
        a.release()
