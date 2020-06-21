from django.shortcuts import render, HttpResponse
from django.conf import settings

import random

from utils.tencent.sms import send_sms_single


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
