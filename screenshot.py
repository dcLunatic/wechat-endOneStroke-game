# -*- coding: utf-8 -*-
"""
手机屏幕截图的代码
"""
import subprocess
import os
import sys
from PIL import Image
from io import StringIO

try:
    from common.auto_adb import auto_adb
except Exception as ex:
    print(ex)
    print('请将脚本放在项目根目录中运行')
    print('请检查项目根目录中的 common 文件夹是否存在')
    exit(1)
adb = auto_adb()


def pull_screenshot():
    adb.run('shell screencap -p /sdcard/shot.png')
    adb.run('pull /sdcard/shot.png .')
    return Image.open('./autojump.png')

