from django.shortcuts import render
from rest_framework.views import APIView

import random, logging
from django_redis import get_redis_connection
from rest_framework.response import Response

from meiduo_mall.libs.yuntongxun.sms import CCP
from . import constants
# Create your views here.

# 创建日志输出器
logger = logging.getLogger('django')

# url(r'^sms_codes/(?P<mobile>1[3-9]\d{9})/$',views.SMSCodeView.as_view())
class SMSCodeView(APIView): # 没有序列化器的、没有查询集的选择APIView
    """
    短信验证码
    """
    def get(self,request,mobile):
        # 生成短信验证码
        sms_code = '%06d' % random.randint(0,999999)
        logger.info(sms_code)

        # 创建链接导redis的对象
        redis_conn = get_redis_connection('verify_codes')

        # 保存短信验证码导Redis
        # redis_conn.setex('key','expire_time','value')
        # redis_conn.setex('sms_%s' % mobile,300, sms_code)
        redis_conn.setex('sms_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        
        # 集成容联云通讯发送短信验证码
        CCP().send_template_sms(mobile,[sms_code,constants.SMS_CODE_REDIS_EXPIRES // 60],1)

        # 响应结果
        return Response({'message':'OK'})