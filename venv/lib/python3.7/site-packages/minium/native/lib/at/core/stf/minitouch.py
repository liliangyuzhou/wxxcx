# -*- coding: utf-8 -*-
# Created by xiazeng on 2020/3/10
# refer: https://github.com/openstf/minitouch
import os.path
import logging
import os
import sys
import re
import socket
import time
from at.core.config import STF_LIB_PATH
from at.core.adbwrap import AdbWrap
from at.utils.commonhelper import pick_unuse_port, get_std_encoding
from at.utils.nbsp import NonBlockingStreamReader

logger = logging.getLogger()


class MiniTouch:
    sock = None  # type: socket.socket

    def __init__(self, serial=None, input_event=None, display_id=None):
        self.input_event = input_event
        self.display_id = display_id
        self.adb = AdbWrap.apply_adb(serial)
        self.path_in_android = "/data/local/tmp/minitouch"
        self.pc_port = pick_unuse_port()
        self.socket_name = "minitouch_%s" % self.pc_port
        self.max_x, self.max_y = None, None
        self.sock = None
        self._check_push()
        self._start_server()
        self._start_client()
        self.nbsp = None

    def _check_push(self):
        abi = self.adb.get_property("ro.product.cpu.abi")
        path = os.path.join(STF_LIB_PATH, abi, "minitouch").replace("\\", r"\\")
        if self.adb.compare_push(path, self.path_in_android):
            self.adb.run_shell("chmod 755 %s" % self.path_in_android)

    def _start_server(self):
        self.adb.forward_name(
            "tcp:%s" % self.pc_port, "localabstract:" + self.socket_name
        )
        if self.input_event:
            p = self.adb.run_shell(
                "/data/local/tmp/minitouch -n '{0}' -d '{1}' 2>&1".format(
                    self.socket_name, self.input_event
                ),
                False,
            )
        else:
            p = self.adb.run_shell(
                "/data/local/tmp/minitouch -n '{0}' 2>&1".format(self.socket_name),
                False,
            )
        nbsp = NonBlockingStreamReader(p.stdout, name="minitouch_output")
        while True:
            line = nbsp.readline(timeout=5.0)
            if line is None:
                raise RuntimeError("minitouch setup timeout")

            line = line.decode(get_std_encoding(sys.stdout))

            # 识别出setup成功的log，并匹配出max_x, max_y
            m = re.match(
                "Type \w touch device .+ \((\d+)x(\d+) with \d+ contacts\) detected on .+ \(.+\)",
                line,
            )
            if m:
                self.max_x, self.max_y = int(m.group(1)), int(m.group(2))
                break
        self.nbsp = nbsp
        self.server_proc = p
        if self.server_proc.poll() is not None:
            raise RuntimeError("minitouch not running")
        # reg_cleanup(self.server_proc.kill)
        return p

    def _start_client(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("127.0.0.1", self.pc_port))
        sock.settimeout(2)
        header = b""
        while True:
            try:
                header += sock.recv(4096)  # size is not strict, so use raw socket.recv
            except socket.timeout:
                # raise RuntimeError("minitouch setup client error")
                logger.warn("minitouch header not recved")
                break
            if header.count(b"\n") >= 3:
                break
        logger.debug("minitouch header:%s", repr(header))
        self.sock = sock

    def release(self):
        if self.nbsp:
            self.nbsp.kill()
        s = time.time()
        if not self.server_proc:
            return
        self.server_proc.kill()
        if self.server_proc.poll() is not None:
            self.adb.kill_pid(self.server_proc.pid)

    def ensure_running(self):
        if self.server_proc.poll() is not None:
            raise RuntimeError("minitouch not running")
        if not self.sock:
            raise RuntimeError("client not connected")

    def send(self, data):
        logger.debug(data)
        self.sock.send(data)

    def touch_down(self, x, y, contract_id=0):
        self.ensure_running()
        cmd = b"d %d %d %d 50\nc\n" % (contract_id, x, y)
        self.send(cmd)

    def touch_move(self, x, y, contract_id=0):
        self.ensure_running()
        cmd = b"m %d %d %d 50\nc\n" % (contract_id, x, y)
        self.send(cmd)

    def touch_up(self, contract_id=0):
        self.ensure_running()
        cmd = b"u %d\nc\n" % contract_id
        self.send(cmd)

    def click(self, x, y, sleep_time=0.01):
        self.ensure_running()
        self.touch_down(x, y)
        time.sleep(sleep_time)
        self.touch_up()

    def long_click(self, x, y, sleep_time=3):
        self.click(x, y, sleep_time)

    def double_click(self, x, y):
        self.click(x, y)
        time.sleep(0.05)
        self.click(x, y)

    def swipe(self, x, y, dst_x, dst_y, steps=20, time_costs=0.5):
        self.touch_down(x, y)
        delta_x = (dst_x - x) / steps
        delta_y = (dst_y - y) / steps
        delta_time = time_costs / steps
        for i in range(steps - 1):
            self.touch_move(x + delta_x * (i + 1), y + delta_y * (y + 1))
            time.sleep(delta_time)
        self.touch_move(dst_x, dst_y)
        self.touch_up()
