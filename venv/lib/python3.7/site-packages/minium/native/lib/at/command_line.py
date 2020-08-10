# -*- coding: utf-8 -*-
# Created by xiazeng on 2020/4/7
import logging
import at
import time
import sys
import at.core.adbwrap
from at.core.config import *


def get_adb(serial):
    return at.core.adbwrap.AdbWrap.apply_adb(serial)


def check_at_env(serial=None):
    warning_list = []
    adb = get_adb(serial)
    if not adb.check_installed_apk(TEST_APP_PKG, TEST_APK_PATH, True):
        warning_list.append(u"请手动安装: %s" % TEST_APK_PATH)
    if not adb.check_installed_apk(TEST_STUB_APP_PKG, STUB_APK_PATH, True):
        warning_list.append(u"请手动安装: %s" % STUB_APK_PATH)
    if not warning_list:
        logging.info("环境检查OK!")
    else:
        logging.info("运行环境有问题:")
        for warning_line in warning_list:
            logging.info(warning_line)


def install(serial, path):
    a = at.At(serial)  # at会检测弹框
    if not a.adb.install(path):
        logging.info("install failed:%s", path)
        sys.exit(-1)


def main():
    logging.basicConfig(level=logging.DEBUG, format="%(message)s")
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v",
        "--version",
        dest="version",
        default=None,
        help="print build info",
        action="store_true",
    )
    parser.add_argument(
        "-s", "--serial", dest="serial", default=None, help="android test helper"
    )
    parser.add_argument(
        "-i", "--install", dest="install", default=None, help="install apk"
    )
    parser.add_argument(
        "--check", dest="check_env", help="check wechat-at env", action="store_true"
    )
    parser.add_argument("-e", dest="event", help="logcat输出点击事件", action="store_true")
    args = parser.parse_args()

    try:
        import argcomplete

        argcomplete.autocomplete(parser)
    except ImportError:
        logging.error("failed import argcomplete")
    serial = args.serial
    if args.check_env:
        check_at_env(serial)
    elif args.version:
        logging.info(at.build_info())
        sys.exit(0)
    elif args.event:
        a = at.At(serial)
        try:
            print("monitor...")
            time.sleep(10 * 60 * 60)
        except Exception:
            a.release()
    elif args.install:
        install(serial, args.install)


if __name__ == "__main__":
    main()
