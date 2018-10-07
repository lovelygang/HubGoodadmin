#!/usr/bin/env python
# -*-coding:utf-8 -*-
__author__ = "gatsby"

from django.template import Library
from django.utils.safestring import mark_safe
import datetime,time
register = Library()

@register.simple_tag
def bulid_filter (filter_column ,admin_class):

    column_obj = admin_class.model._meta.get_field(filter_column)
    try:
        filter_ele = "<select name='%s'>" % filter_column
        for choice in column_obj.get_choices():
            selected = ''
            if filter_column in admin_class.filter_conditions: #当前自动被过滤了

                if str(choice[0]) == admin_class.filter_conditions.get(filter_column):#当前值被选中
                     selected = 'selected'

                ####low###
                #         option = "<option value='%s' selected>%s</option>" % choice
                #     else:
                #         option = "<option value='%s'>%s</option>" % choice
                #
                # else:
                #     option = "<option value='%s'>%s</option>" % choice

            option = "<option value='%s' %s>%s</option>"%(choice[0],selected,choice[1])
            filter_ele += option
    except AttributeError  as e:
        print('err',e)
        filter_ele = "<select name='%s__gte'>" % filter_column
        if column_obj.get_internal_type() in ('DateField','DateTimeField'):
            time_obj = datetime.datetime.now()
            time_list = [
                ['','------------'],
                [time_obj,'today'],
                [time_obj-datetime.timedelta(7),'七天内'],
                [time_obj.replace(day=1),'本月'],
                [time_obj-datetime.timedelta(90),'三个月内'],
                [time_obj.replace(month=1,day=1),'本年'],
                ['','all']
            ]
            for i in time_list:
                selected = ''
                time_str = ''if not i[0] else "%s-%s-%s"%(i[0].year,i[0].month,i[0].day)

                if "%s__gte"% filter_column in admin_class.filter_conditions:  # 当前自动被过滤了

                    if time_str == admin_class.filter_conditions.get("%s__gte"% filter_column ):  # 当前值被选中
                        selected = 'selected'

                option = "<option value='%s' %s>%s</option>" %(time_str,selected,i[1])
                filter_ele += option

    filter_ele += '</select>'
    return mark_safe(filter_ele)

@register.simple_tag
def build_table_row(obj,admin_class):
    """生成一条记录的html element"""
    #admin_class.model._meta.verbose_name
    ele = ""
    # print("OBJ>>>>>>>>>>>",obj)
    # print("admin_class>>>>>>>>>>>",admin_class)
    if admin_class.list_display:
        for index,column_name in enumerate(admin_class.list_display):

            column_obj = admin_class.model._meta.get_field(column_name)

            if column_obj.choices: #get_xxx_display
                column_data = getattr(obj,"get_%s_display"%column_name)()
            else:
                column_data = getattr(obj,column_name)

                # <span>{{ row.ctime|date:"Y-m-d H:i:s" }}</span>
            if column_obj.get_internal_type() in ('DateField','DateTimeField'):
                column_data = column_data.strftime("%Y-%m-%d %H:%M")

            td_ele = "<td>%s</td>" % column_data
            if index == 0 :
                print('index==',index)
                td_ele = "<td><a href='%s/change'>%s</a></td>"%(obj.id,column_data)

            ele += td_ele
    else:
        td_ele="<td><a href='%s/change'>%s</a></td>" %(obj.id,obj)
        ele += td_ele
    return mark_safe(ele)





@register.simple_tag
def  get_sorted_column(column,sorted_column,forloop):
    #sorted_column = {'name','0'}
    if column in sorted_column:#这一列被排序
        #判断上一次的排序是什么顺序本次取反
        last_sort_index = sorted_column[column]
        if last_sort_index.startswith('-'):
            this_time_sort_index = last_sort_index.strip('-')

        else:
            this_time_sort_index = '-%s' %last_sort_index


        return this_time_sort_index

    else:
        return forloop


@register.simple_tag
def render_sorted_arrow (column ,sorted_column):
    if column in sorted_column:  # 这一列被排序
        last_sort_index = sorted_column[column]
        if last_sort_index.startswith('-'):
            arrow_direction = 'bottom'
        else:
            arrow_direction = 'top'
        ele = """<span class="glyphicon glyphicon-triangle-%s" aria-hidden="true"></span>"""%arrow_direction
        return mark_safe(ele)
    return ''

@register.simple_tag
def  render_filtered_args(admin_class,render_html = True):
    '''拼接筛选的字段'''

    if admin_class.filter_conditions:
        ele = ''
        for k,v in admin_class.filter_conditions.items():
            ele += '&%s=%s' %(k,v)
        if render_html:
            return mark_safe(ele)
        else:
            return ele
    else:
        return ''


@register.simple_tag
def render_paginator(querysets,admin_class,sorted_column):
    ele = '''
         <ul class="pagination">
       '''
    for i in querysets.paginator.page_range:
        if abs(querysets.number - i) < 2:  # display btn
            active = ''
            if querysets.number == i:  # current page
                active = 'active'
            filter_ele = render_filtered_args(admin_class)

            sorted_ele = ''
            if sorted_column:
                sorted_ele = '&_o=%s' % list(sorted_column.values())[0]

            p_ele = '''<li class="%s"><a href="?_page=%s%s%s">%s</a></li>''' % (active, i,filter_ele,sorted_ele, i)

            ele += p_ele

    ele += "</ul>"

    return mark_safe(ele)

@register.simple_tag
def get_current_sorted_column_index(sorted_column):

    return list(sorted_column.values())[0] if sorted_column else ''


@register.simple_tag
def get_obj_field_val(form_obj,field):
    '''返回model obj 具体字段值'''

    # for column_name in form_obj:
    #
    #
    #     if column_name.choices:  # get_xxx_display
    #         column_data = getattr(form_obj, "get_%s_display" % field)()
    # td_ele = "<p>%s</p>" % column_data

    # print('>>>>>>form_obj',form_obj)
    # print('>>>>>>field',field)

    # --------------
    # if admin_class.list_display:
    #     for index, column_name in enumerate(admin_class.list_display):
    #
    #         column_obj = admin_class.model._meta.get_field(column_name)
    #
    #         if column_obj.choices:  # get_xxx_display
    #             column_data = getattr(obj, "get_%s_display" % column_name)()
    #         else:
    #             column_data = getattr(obj, column_name)
    # ele = ""
    # if admin_class.readonly_fields:
    #     for column_name in admin_class.readonly_fields:
    #         column_obj = admin_class.model._meta.get_field(column_name)
    #         if column_obj.choices:
    #             column_data  = getattr(form_obj.instance,"get_%s_display" % column_name)()
    #         else:
    #             column_data = getattr(form_obj.instance, column_name)
    #         td_ele = "<p>%s</p>" % column_data
    #
    #         ele += td_ele
    # print(ele)
    if field == 'status':
          column_data = getattr(form_obj.instance,"get_%s_display" % field)()
    else:
          column_data = getattr(form_obj.instance, field)
    return  mark_safe(column_data)

@register.simple_tag
def get_available_mtm_data(field_name,form_obj,admin_class):
    '''返回的是M2M字段关联表的所有数据'''
    field_obj = admin_class.model._meta.get_field(field_name)
    obj_list = set(field_obj.related_model.objects.all())
    if form_obj.instance.id:
        selected_data = set(getattr(form_obj.instance, field_name).all())

        return  obj_list-selected_data
    else:
        return obj_list

@register.simple_tag
def get_selected_mtm_data(field_name,form_obj,admin_class):
    '''返回已选数据'''
    if form_obj.instance.id:
        selected = getattr(form_obj.instance,field_name).all()
        return  selected
    else:
        return []


@register.simple_tag
def display_all_related_objs(obj):

    """显示要被删除的所有管理对象"""

    ele = "<ul>"

    for reversed_fk_obj in obj._meta.related_objects:
        related_table_name = reversed_fk_obj.name
        related_lookup_key = "%s_set" %related_table_name
        related_objs = getattr(obj,related_lookup_key).all()#反向查找管理的所有数据
        ele += "<li>%s<ul>"%related_table_name

        if reversed_fk_obj.get_internal_type() == "ManyToManyField":# 不需要深入查找
            for i in related_objs:
                ele += "<li><a href='/goodadmin/%s/%s/%s/change/'>%s</a> 记录里与[%s]相关的的数据将被删除</li>"\
                        %(i._meta.app_label,i._meta.model_name,i.id,i,obj)

        else:
            for i in related_objs:
                ele += "<li><a href='/goodadmin/%s/%s/%s/change/'>%s</a></li>" \
                         % (i._meta.app_label, i._meta.model_name, i.id, i)

                ele += display_all_related_objs(i)

        ele +="</ul></li>"

    ele +="</ul>"
    return ele


@register.simple_tag
def get_model_name(admin_class):
    return admin_class.model._meta.model_name.upper()

@register.simple_tag
def get_model_verbose_name(admin_class):
    return admin_class.model._meta.verbose_name



@register.simple_tag
def get_ver_ch(app_name,model_name):
    print(app_name)
    from goodadmin.site import site
    admin_class = site.enabled_admins[app_name][model_name]

    return admin_class.model._meta.verbose_name

@register.simple_tag
def get_app_name(admin_class):
    app_name = admin_class.model._meta.app_label

    return app_name

@register.simple_tag
def get_model_name_min(admin_class):
    return admin_class.model._meta.model_name