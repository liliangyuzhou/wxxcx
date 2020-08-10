#!/usr/bin/env python3
# Created by xiazeng on 2019/3/12
import base64
import socket
import sys


def base64_to_file(base64_str, path):
    image_data = base64.b64decode(base64_str)
    open(path, "wb").write(image_data)


def pick_unuse_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("localhost", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def get_std_encoding(stream):
    return getattr(stream, "encoding", None) or sys.getfilesystemencoding()
