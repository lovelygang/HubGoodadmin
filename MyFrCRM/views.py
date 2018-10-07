from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from MyCRM import models
# Create your views here.

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


            return redirect(request.GET.get('next', '/'))

            # return redirect('/crm/')
        else:
            error_message = '用户名或者密码错误'


    return render(request,'login.html',{'error_message':error_message})



def acc_logout(request):
    logout(request)
    return redirect("/login/")
