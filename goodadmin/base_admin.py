#!/usr/bin/env python
# -*-coding:utf-8 -*-
__author__ = "gatsby"

from django.shortcuts import render
import json
class BaseGoodAdmin(object):
    def __init__(self):
        self.actions.extend(self.default_actions)

    list_display = []
    list_filter =[]
    search_fields =[]
    readonly_fields = []
    filter_horizontal = []
    list_per_page = 20

    default_actions = ['delete_selected_objs']
    actions = []

    def delete_selected_objs(self, request, querysets):
        querysets_ids = json.dumps([i.id for i in querysets])

        for row in querysets:
            print('self',row)

        return render(request, 'goodadmin/table_obj_delete.html',
                      {'admin_class':self,
                       'objs':querysets,
                       'querysets_ids':querysets_ids
                       })