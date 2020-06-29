# -*-coding:utf-8-*-
"""
用户账户相关功能：注册、短信、登录、注销
"""
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from web.forms.account import RegisterModelForm, SendSmsForm
from web import models


def register(request):
    if request.method == 'GET':
        form = RegisterModelForm()
        return render(request, 'register.html', {'form': form})

    form = RegisterModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': True, 'data': '/login/'})

    return JsonResponse({'status': False, 'error': form.errors})


def send_sms(request):
    form = SendSmsForm(request, data=request.GET)
    # 只是校验手机号码：不能为空，格式是否正确
    if form.is_valid():
        # 发短信，写redis
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})
