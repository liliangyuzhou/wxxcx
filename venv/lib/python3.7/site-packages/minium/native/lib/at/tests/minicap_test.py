# -*- coding: utf-8 -*-
# Created by xiazeng on 2020/3/10
import time
import logging
from attestbase import AtTestBase
from at.core.stf.mincap import MiniCap

logger = logging.getLogger()


class MiniCapTest(AtTestBase):
    def setUp(self):
        self.front = MiniCap(display_id=1)
        self.back = MiniCap(display_id=0)

    def test_screenshot(self):
        open("front.jpg", "wb").write(self.front.get_frame())
        open("back.jpg", "wb").write(self.back.get_frame())
