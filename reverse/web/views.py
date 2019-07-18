from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import FileSystemStorage
from web.models import *
from .forms import UploadFileForm
from .reverse import *


# Create your views here.
# 首页
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if username and password:
            # 数据库查询
            try:
                is_user = User.objects.get(username=username)
            except ObjectDoesNotExist:
                print('no such user!')
                return render(request, 'web/login.html')
            print(is_user)
            # return render(request, 'web/login.html')
            return JsonResponse({
                'success': True,
                'redirect': 'upload',
            })
        else:
            print('No such user')
    return render(request, 'web/login.html')


# 注册
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if username and password:
            # 数据库添加
            user = User(username=username, password=password, filename='')
            user.save()
            return JsonResponse({
                'success': True,
                'redirect': '/web',
            })
        else:
            print('No such user')
    return render(request, 'web/signup.html')


# 上传
def upload(request):
    if request.method == 'POST':
        filename = request.FILES['filename']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return JsonResponse({
                'success': True,
                'redirect': 'show',
            })
    else: 
        form = UploadFileForm()
        return render(request, 'web/upload.html', {
        'form': form
    })


# 展示
def show(request):
    return render(request, 'web/show.html')