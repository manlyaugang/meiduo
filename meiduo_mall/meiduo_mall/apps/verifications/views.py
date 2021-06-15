from django.shortcuts import render
from rest_framework.views import APIView

import random, logging
from django_redis import get_redis_connection
from rest_framework.response import Response
from rest_framework import status

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
        # 创建链接到redis的对象
        redis_conn = get_redis_connection('verify_codes')

        # 再次点击时读取redis中存储的标记
        send_flag = redis_conn.get('send_flag%s' % mobile)
        if send_flag:
            return Response({'message':'频繁发送短信验证码'},status=status.HTTP_400_BAD_REQUEST)

        # 生成短信验证码
        sms_code = '%06d' % random.randint(0,999999)
        logger.info(sms_code)



        # 保存短信验证码导Redis
        # redis_conn.setex('key','expire_time','value')
        # redis_conn.setex('sms_%s' % mobile,300, sms_code)
        redis_conn.setex('sms_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)

        # 向redis中添加一个标记，数据。该标记的有效期是60秒
        redis_conn.setex('send_flag_%s' % mobile,constants.SEND_SMS_CODE_INTERVAL,1)

        # 集成容联云通讯发送短信验证码
        CCP().send_template_sms(mobile,[sms_code,constants.SMS_CODE_REDIS_EXPIRES // 60],1)

        # 响应结果
        return Response({'message':'OK'})