#!/usr/bin/env python
# -*-coding:utf-8 -*-
__author__ = "gatsby"


print('my goodadmin setting in Student ..................')


from  goodadmin.site import site
from student import models

class testAdmin(object):
    list_display = ['name']


site.register(models.Test,testAdmin)