#!/usr/bin/env python
# -*-coding:utf-8 -*-
__author__ = "gatsby"


from django.forms import ModelForm


def create_dynamic_model_form(admin_class,form_add=False):
    '''动态生成modelform
    form_add : False 默认是修改的表单，ture时为新增的表单
    '''

    class Meta:
        model = admin_class.model
        fields = '__all__'
        if not form_add: #change
            exclude = admin_class.readonly_fields
            admin_class.form_add = False #这是因为admin_class的form_add tag都是同一个，所以上一次操作为修改tag就要改为false否则不显示了
        else: #add
            admin_class.form_add= True
    def __new__(cls,*args,**kwargs):

        for field_name in cls.base_fields:
            field_obj = cls.base_fields[field_name]
            field_obj.widget.attrs.update({'class':'form-control'})
            # if field_name in admin_class.readonly_fields:
            #     field_obj.widget.attrs.update({'disabled':'true'})

        return ModelForm.__new__(cls)

    dynamic_form = type('DynamicModelForm',(ModelForm,),{'Meta':Meta,'__new__':__new__})

    return dynamic_form
