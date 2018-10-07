
from django.contrib import admin
from django.urls import path ,include,re_path

from goodadmin import views

urlpatterns = [

    path('login/', views.acc_login),
    path('logout/', views.acc_logout,name='logout'),


    path('', views.app_index,name='app_index'),


    re_path(r'(\w+)/(\w+)/$', views.table_obj_list, name='table_obj_list'),

    re_path(r'(\w+)/(\w+)/(\d+)/change$', views.table_obj_change, name='table_obj_change'),

    re_path(r'(\w+)/(\w+)/(\d+)/delete$', views.table_obj_delete, name='obj_delete'),

    re_path(r'(\w+)/(\w+)/add$', views.table_obj_add, name='table_obj_add'),

    re_path(r'(\w+)/$', views.app_table_list ,name='app_table_list'),

]
