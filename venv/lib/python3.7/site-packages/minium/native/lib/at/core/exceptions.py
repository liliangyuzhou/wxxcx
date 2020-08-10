# -*- coding: utf-8 -*-
# Created by xiazeng on 2019/12/27


class AtError(Exception):
    pass


class AtUnknownError(AtError):
    pass


class FailedConnectAtServer(AtError):
    pass


class AdbException(AtError):
    pass


class AdbDisconnectedError(AdbException):
    pass


class CanNotAccessToPackageManager(AtError):
    pass


class RemoteError(AtError):
    pass


class UiUnExpectError(RemoteError):
    pass


class UiNotFoundError(RemoteError):
    pass


class NoSuchMethodError(RemoteError):
    pass


class ParamError(RemoteError):
    pass


class ClickPermissionError(RemoteError):
    pass


class UiAutomatorDisconnectError(RemoteError):
    pass
