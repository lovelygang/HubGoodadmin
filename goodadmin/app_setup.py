#!/usr/bin/env python
# -*-coding:utf-8 -*-
__author__ = "gatsby"

from django import  conf

def auto_discover():
    for app_name in conf.settings.INSTALLED_APPS:
        try:
            # mode = importlib.import_module(app_name,"goodadmin")
            mode = __import__("%s.goodadmin" % app_name)
            print(mode.goodadmin)
        except ModuleNotFoundError as e:
            print('错误信息', e)