#!/usr/bin/env python
# encoding:utf-8
import unittest
import logging
import os.path
import at.vision.template_match

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger()

root = os.path.join(os.path.dirname(__file__), "images")


class AtTestBase(unittest.TestCase):
    def test_match(self):
        source_path = os.path.join(root, "image.jpg")
        in_path = os.path.join(root, "2.jpg")
        r = at.vision.template_match.search(in_path, source_path)
        print(r)
