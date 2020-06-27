from django.db import models


# Create your models here.

class UserInfo(models.Model):
    username = models.CharField(verbose_name='用戶名', max_length=32)
    email = models.EmailField(verbose_name='郵箱', max_length=32)
    mobile_phone = models.CharField(verbose_name='電話號碼', max_length=32)
    password = models.CharField(verbose_name='密碼', max_length=32)
