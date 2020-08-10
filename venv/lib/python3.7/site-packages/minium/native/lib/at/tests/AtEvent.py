#!/usr/bin/env python3
# Created by xiazeng on 2020/4/13
import logging
from attestbase import AtTestBase

logger = logging.getLogger()


class AtEvent(AtTestBase):
    def test_a(self):
        self.at.event_monitor.add_selector_filter(
            "test", self.at.e.text("测试"), self.at.e.text("测试")
        )
