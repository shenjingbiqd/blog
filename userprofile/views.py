from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import User_Login_Form, User_Register_Form
from django.contrib.auth.decorators import login_required


def user_login(request):
    if request.method == 'POST':
        user_login_form = User_Login_Form(request.POST)
        if user_login_form.is_valid():
            data = user_login_form.cleaned_data
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                login(request, user)
                return redirect('jimblog:home')
            else:
                return HttpResponse("用户名密码错误")
        else:
            return HttpResponse("输入的数据不合法")
    elif request.method == 'GET':
        user_login_form = User_Login_Form()
        return render(request, 'userprofile/login.html', {'form': user_login_form})
    else:
        return HttpResponse("请适用GET或POST方法")


@login_required(login_url='/user/login/')
def user_logout(request):
    logout(request)
    return redirect('jimblog:home')


@login_required(login_url='/user/login/')
def user_delete(request, id):
    if request.method == 'POST':
        user = User.objects.get(id=id)
        if request.user == user:
            logout(request)
            user.delete()
            return redirect('jimblog:home')
        else:
            return HttpResponse('登录用户与删除用户不一致')
    else:
        return HttpResponse('请使用POST方法')


def register(request):
    if request.method == 'POST':
        user_register_form = User_Register_Form(data=request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.save()
            login(request, new_user)
            return redirect('jimblog:home')
        else:
            return HttpResponse('注册表单有误')
    elif request.method == 'GET':
        user_register_form = User_Register_Form()
        return render(request, 'userprofile/register.html', {'form': user_register_form})
    else:
        return HttpResponse('请使用GET/POST方法')

