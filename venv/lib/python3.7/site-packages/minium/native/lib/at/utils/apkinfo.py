#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by xiazeng on 2017/8/28

import logging
import zipfile
import sys
import hashlib
import os.path

if sys.version_info[0] < 3:
    from .axmlparser import AXMLPrinter
else:
    from .axmlparser3 import AXMLPrinter

logger = logging.getLogger()


class ApkInfo(object):
    def __init__(self, apk_path):
        logger.debug("parse apk:%s", apk_path)
        self._md5 = None
        self.apk_path = apk_path
        self.size = os.path.getsize(apk_path)
        zf = zipfile.ZipFile(open(apk_path, "rb"), mode="r")
        self.xml_bytes = None
        for i in zf.namelist():
            if i == "AndroidManifest.xml":
                self.xml_bytes = zf.read(i)
                printer = AXMLPrinter(self.xml_bytes)
                self.xml_obj = printer.get_xml_obj()
                break
        else:
            raise RuntimeError("AndroidManifest.xml not found in %s", apk_path)

        node = self.xml_obj.getElementsByTagName("manifest")[0]
        self.version_code = node.getAttribute("android:versionCode")
        self.version_name = node.getAttribute("android:versionName")
        self.platformBuildVersionCode = node.getAttribute("platformBuildVersionCode")
        self.platformBuildVersionName = node.getAttribute("platformBuildVersionName")
        self.pkg = node.getAttribute("package")
        manifest_doms = self.xml_obj.getElementsByTagName("manifest")
        self.pkg_name = manifest_doms[0].getAttribute("package")
        meta_datas = self.xml_obj.getElementsByTagName("meta-data")
        for meta in meta_datas:
            name = meta.getAttribute("android:name")
            if name == "com.tencent.mm.BuildInfo.BUILD_TAG":
                self.build_tag = meta.getAttribute("android:value").encode()
            elif name == "com.tencent.mm.BuildInfo.CLIENT_VERSION":
                self.client_version = meta.getAttribute("android:value").encode()
            elif name == "com.tencent.mm.BuildInfo.BUILD_SVNPATH":
                self.git_path = meta.getAttribute("android:value").encode()
            elif name == "com.tencent.mm.BuildInfo.BUILD_REV":
                self.revision = meta.getAttribute("android:value").encode()
            elif name == "com.tencent.mm.BuildInfo.BUILD_TIME":
                self.built_time = meta.getAttribute("android:value").encode()
            elif name == "com.tencent.mm.BuildInfo.BUILD_OWNER":
                self.built_owner = meta.getAttribute("android:value").encode()
        for node in self.xml_obj.getElementsByTagName("manifest"):
            if node.getAttribute("android:versionCode"):
                self.version_code = int(node.getAttribute("android:versionCode"))
            else:
                self.version_code = 0
            self.version_name = node.getAttribute("android:versionName")

    @property
    def md5(self):
        if self._md5:
            return self._md5
        hash_md5 = hashlib.md5()
        with open(self.apk_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        self._md5 = hash_md5.hexdigest()
        return hash_md5.hexdigest()

    @property
    def activities(self):
        return self.get_names("activity")

    @property
    def permissions(self):
        return self.get_names("uses-permission")

    def get_attribute(self, tag_name, attr_name):
        node = self.xml_obj.getElementsByTagName(tag_name)[0]
        return node.getAttribute(attr_name)

    def get_names(self, tag_name):
        ps = []
        nodes = self.xml_obj.getElementsByTagName(tag_name)
        for node in nodes:
            name = node.getAttribute("android:name")
            ps.append(name)
        return ps

    def __eq__(self, other):
        if self.size != other.size:
            logger.info("size not equal")
            return False
        if self.md5 != other.md5:
            logger.info("md5 not equal")
            return False
        return True

    def to_dict(self):
        return {
            "version": self.client_version,
            "build_tag": self.build_tag,
            "branch": self.git_path,
            "time": self.built_time,
            "owner": self.built_owner,
            "revision": self.revision,
            "version_code": self.version_code,
            "version_name": self.version_name,
            "md5": self.md5,
            "pkg_name": self.pkg_name,
        }

    def print(self):
        for k, v in self.to_dict().items():
            print("%s=%s" % (k, v))


if __name__ == "__main__":
    # AppBuildInfo.get_activity(ur'D:\cov973.apk')

    a = ApkInfo("/Users/xiazeng/Downloads/temp_test.apk")
    print(a.activities)
