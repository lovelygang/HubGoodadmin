from goodadmin import permission_hook

perm_dic= {

    #'crm_table_index': ['table_index', 'GET', [], {'source':'qq'}, ],  # 可以查看CRM APP里所有数据库表
    'MyCRM_table_list': ['table_obj_list', 'GET', [], {},permission_hook.view_all],  # 可以查看每张表里所有的数据
    'MyCRM_table_list_view': ['table_obj_change', 'GET', [], {},permission_hook.chane_self],  # 可以访问表里每条数据的修改页
    'MyCRM_table_list_change': ['table_obj_change', 'POST', [], {},permission_hook.view_all],  # 可以对表里的每条数据进行修改
    'MyCRM_table_obj_add_view': ['table_obj_add', 'GET', [], {},permission_hook.view_all],  # 可以访问数据增加页
    'MyCRM_table_obj_add': ['table_obj_add', 'POST', [], {},permission_hook.view_all],  # 可以创建表里的数据

}



