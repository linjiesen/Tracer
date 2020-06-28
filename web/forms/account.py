from django import forms
from django.core.validators import RegexValidator

from web import models


class RegisterModelForm(forms.ModelForm):
    mobile_phone = forms.CharField(label='手机号码',
                                   validators=[RegexValidator(r'^((\\+86)|(86))?[1][3456789][0-9]{9}$', '手機號碼格式錯誤'), ])
    password = forms.CharField(label='密码', widget=forms.PasswordInput())

    confirm_password = forms.CharField(label='重复密码', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': '请输入密码'}))
    code = forms.CharField(label='验证码')

    class Meta:
        model = models.UserInfo
        fields = ['username', 'email', 'password', 'confirm_password', 'mobile_phone', 'code']  # 設置注冊界面表格輸入順序

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = '请输入{}'.format(field.label, )
