from django.shortcuts import render, HttpResponse
from django.conf import settings
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


import random

from utils.tencent.sms import send_sms_single
from SMS import models


# Create your views here.

def send_sms(request):
    """
    send sms
        ?tpl=login -> 641422
        ?tpl=register -> 641424
    :param request:
    :return:
    """
    tpl = request.GET.get('tpl')
    template_id = settings.TENCENT_SMS_TEMPLATE.get(tpl)
    if not template_id:
        return HttpResponse('Template is not Exist!')

    code = random.randrange(1000, 9999)
    res = send_sms_single('18395583854', template_id, [code, ])
    print(res)
    if res['result'] == 0:
        return HttpResponse('Success~')
    else:
        return HttpResponse(res['errmsg'])


class RegisterModelForm(forms.ModelForm):

    mobile_phone = forms.CharField(label='手機號碼', validators=[RegexValidator(r'^((\\+86)|(86))?[1][3456789][0-9]{9}$', '手機號碼格式錯誤'), ])
    password = forms.CharField(label='密碼', widget=forms.PasswordInput())

    confirm_password = forms.CharField(label='重復密碼', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '請輸入密碼'}))
    code = forms.CharField(label='驗證碼')

    class Meta:
        model = models.UserInfo
        fields = ['username', 'email', 'password', 'confirm_password', 'mobile_phone', 'code']      #設置注冊界面表格輸入順序

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = '請輸入{}'.format(field.label,)


def register(request):
    form = RegisterModelForm()
    return render(request, 'register.html', {'form': form})
