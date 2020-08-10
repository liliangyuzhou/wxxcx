#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by xiazeng on 2017/8/28
import airtest.aircv.template_matching
import airtest.aircv.aircv


def search(im_path, source_path):

    im_search = airtest.aircv.aircv.imread(im_path)
    im_source = airtest.aircv.aircv.imread(source_path)
    return airtest.aircv.template_matching.TemplateMatching(
        im_search, im_source
    ).find_best_result()
