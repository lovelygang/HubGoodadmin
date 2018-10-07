from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout

from django import conf #其他项目也可以用
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
import importlib
from django.contrib.auth.decorators import  login_required
from goodadmin import app_setup
from django.db.models import Q
import json
from goodadmin import good_forms
from goodadmin import permissions


app_setup.auto_discover()

from goodadmin.site import site
# print('site:>>>',type(site.enabled_admins))

# Create your views here.
# for k,v in site.enabled_admins.items():
#     for app_name,admin_class in v.items():
#         print(app_name,admin_class,id(admin_class))

def get_filter_result(request,querysets):
    filter_conditions = {}

    for key,val in request.GET.items():
        if key in ('_page','_o','_q'):continue
        if val:
            filter_conditions[key]=val

    print("filter_conditions",filter_conditions)
    return querysets.filter(**filter_conditions),filter_conditions


def get_orderby_result(request,querysets,admin_class):
    """排序"""
    orderby_index = request.GET.get('_o')

    current_ordered_column = {}

    if orderby_index:
        orderby_key = admin_class.list_display[abs(int(orderby_index))]

        #让前端知道当前排序的列
        current_ordered_column[orderby_key] = orderby_index

        if orderby_index.startswith('-'):
            orderby_key = '-' + orderby_key

        return querysets.order_by(orderby_key),current_ordered_column

    else:
        return querysets,current_ordered_column

def get_searched_result(request,querysets,admin_class):

    search_key = request.GET.get('_q')

    if search_key:
        q = Q()
        q.connector = 'OR'

        for search_field in admin_class.search_fields:
            q.children.append(("%s__contains"%search_field,search_key))

        return querysets.filter(q)
    return querysets

@permissions.check_permission
@login_required
def table_obj_change(request,app_name,model_name,obj_id):
    """kingadmin 数据库修改页"""
    # from MyCRM import forms

    admin_class = site.enabled_admins[app_name][model_name]
    model_form = good_forms.create_dynamic_model_form(admin_class)
    obj = admin_class.model.objects.get(id=obj_id)


    if request.method =="GET":
        form_obj = model_form(instance=obj)
    if request.method == "POST":
        form_obj = model_form(instance=obj,data=request.POST)

        if form_obj.is_valid():
            form_obj.save()
            return redirect('/goodadmin/%s/%s/'%(app_name,model_name))

    return render(request,'goodadmin/table_obj_change.html',locals())

@permissions.check_permission
@login_required
def table_obj_add(request,app_name,model_name):
    '''增加表数据'''
    admin_class = site.enabled_admins[app_name][model_name]
    model_form = good_forms.create_dynamic_model_form(admin_class,form_add=True)

    if request.method == "GET":
        form_obj = model_form()
    if request.method == "POST":
        form_obj = model_form(data=request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect('/goodadmin/%s/%s/' % (app_name, model_name))


    return render(request,'goodadmin/table_obj_add.html',locals())


@permissions.check_permission
@login_required
def table_obj_delete(request,app_name,model_name,obj_id):
    admin_class = site.enabled_admins[app_name][model_name]
    obj  = admin_class.model.objects.get(id=obj_id)

    if request.method == "POST":
        obj.delete()
        return redirect("/goodadmin/{app_name}/{model_name}/".format(app_name=app_name,model_name=model_name))
    return render(request,'goodadmin/table_obj_delete.html',locals())

@permissions.check_permission
@login_required
def app_table_list(request,app_name):
    table_list = site.enabled_admins[app_name]
    # ver_name=[]
    # for row in table_list:
    #     model_name = row
    #     name = site.enabled_admins[app_name][model_name]
    #     ver_name.append(name)


    # table_list = table_list.model._meta.verbose_name
    # print('>>>>>',table_list)
    return render(request,'goodadmin/app_table_list.html',locals())

@permissions.check_permission
@login_required
def table_obj_list(request, app_name, model_name):
    """取出指定model里的数据返回给前端"""
    # print(">>>>",site.enabled_admins[app_name][model_name])
    admin_class = site.enabled_admins[app_name][model_name]
    # print('admin_class:>>>',admin_class)
    menus_list = []

    for role in request.user.role.all():
        for meun in role.menus.all():
            menus_list.append(meun)

    menus_list = set(menus_list)

    if request.method=="POST":
        print('批量删除！！！！！！！')
        selected_action = request.POST.get('sel_action')
        selected_ids = json.loads(request.POST.get('selected_ids'))

        if not selected_action: #如果有action参数，走正常action，如果没有可能是一个删除动作
            if selected_ids:#删除选中的数据
                admin_class.model.objects.filter(id__in=selected_ids).delete()

        else:

            selected_objs = admin_class.model.objects.filter(id__in=selected_ids)
            admin_action_func = getattr(admin_class,selected_action)
            response = admin_action_func(request,selected_objs)
            if response:
                return response


    querysets = admin_class.model.objects.all().order_by('-id')

    querysets,filter_conditions= get_filter_result(request,querysets)
    admin_class.filter_conditions = filter_conditions

    #search querysets result
    querysets = get_searched_result(request,querysets,admin_class)
    #前端显示上次搜索内容
    admin_class.search_key = request.GET.get('_q','')


    #sorted querysets
    querysets,sorted_column = get_orderby_result(request, querysets, admin_class)

    #Django分页功能
    paginator = Paginator(querysets, admin_class.list_per_page)  # Show 25 contacts per page

    page = request.GET.get('_page')
    try:
        #可迭代的
        querysets = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        querysets = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        querysets = paginator.page(paginator.num_pages)




    return render(request,'goodadmin/table_obj_list.html',
                   locals())



def app_index(request):
    # print(conf.settings.INSTALLED_APPS)
    # res = admin_class.model._meta.verbose_name
    # admin_class = site.enabled_admins[app_name][model_name]
    # role = request.user.role.select_related.
    # # for r in role:
    # print('角色是：>?',role)
    # for role in request.user.role.select_related:
    #     for meun in role.menus.select_related:
    #         print(meun)



    menus_list = []


    for role in request.user.role.all():
         for meun in role.menus.all():
              menus_list.append(meun)

    menus_list = set(menus_list)



    return render(request,'goodadmin/app_index.html',{"site":site,"menus_list":menus_list})





def acc_login(request):
    error_message = ''
    if request.method =="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password) #验证
        if user:
            print("登入成功",user)

            login(request,user)  #登入

            print(request.session)


            return redirect(request.GET.get('next', '/goodadmin/'))

            # return redirect('/crm/')
        else:
            error_message = '用户名或者密码错误'


    return render(request,'goodadmin/login.html',{'error_message':error_message})





def acc_logout(request):
    logout(request)
    return redirect("/goodadmin/login/")


