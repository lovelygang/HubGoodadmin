#!/usr/bin/env python
# -*-coding:utf-8 -*-
__author__ = "gatsby"

from goodadmin.base_admin import BaseGoodAdmin

class AdminSite(object):
    def __init__(self):
        self.enabled_admins = {}


    def register(self,model_class,admin_class = None):
        # print(model_class._meta.app_label,admin_class)

        app_name = model_class._meta.app_label
        model_name = model_class._meta.model_name



        #为了避免多个model共享一个实例对象
        if not admin_class:
            admin_class=BaseGoodAdmin()
        else:
            admin_class=admin_class()

        admin_class.model = model_class #把model_class赋值给了admin_class

        if app_name not in self.enabled_admins:
           self.enabled_admins[app_name]={}
        self.enabled_admins[app_name][model_name]= admin_class

site = AdminSite()