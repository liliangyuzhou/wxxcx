# -*- coding: utf-8 -*-
# Created by xiazeng on 2020/3/10
# refer: https://github.com/openstf/minicap
import os.path
from at.core.adbwrap import AdbWrap
from at.core.config import STF_LIB_PATH


class MiniCap:
    CMD = "LD_LIBRARY_PATH=/data/local/tmp /data/local/tmp/minicap"

    def __init__(self, serial=None, display_id=None):
        self.adb = AdbWrap.apply_adb(serial)
        self.display_id = display_id
        self.minicap_path = "/data/local/tmp/minicap"
        self.minicap_so_path = "/data/local/tmp/minicap.so"
        self._check_push()

    def _check_push(self):
        abi = self.adb.get_property("ro.product.cpu.abi")
        minicap_pc_path = os.path.join(STF_LIB_PATH, abi, "minicap").replace(
            "\\", r"\\"
        )
        minicap_so_pc_path = os.path.join(STF_LIB_PATH, abi, "minicap.so").replace(
            "\\", r"\\"
        )

        self.adb.compare_push(minicap_so_pc_path, self.minicap_so_path)
        if self.adb.compare_push(minicap_pc_path, self.minicap_path):
            self.adb.run_shell("chmod 755 %s" % self.minicap_path)

    def get_frame(self):
        w, h = self.adb.screen_size
        projection = "%dx%d@%dx%d/%d" % (h, w, h, w, 0)
        if self.display_id:
            raw_data = self.adb.run_shell(
                self.CMD
                + " -d "
                + str(self.display_id)
                + " -n 'airtest_minicap' -P %s -s" % projection
            )
        else:
            raw_data = self.adb.run_shell(
                self.CMD + " -n 'airtest_minicap' -P %s -s" % projection
            )
        jpg_data = raw_data.split(b"for JPG encoder" + self.adb.line_breaker)[-1]
        jpg_data = jpg_data.replace(self.adb.line_breaker, b"\n")
        return jpg_data
