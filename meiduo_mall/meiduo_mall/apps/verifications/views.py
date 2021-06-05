from django.shortcuts import render
from rest_framework.views import APIView

# Create your views here.

# url(r'^sms_codes/(?P<mobile>1[3-9]\d{9})/$',views.SMSCodeView.as_view())
class SMSCodeView(APIView): # 没有序列化器的、没有查询集的选择APIView
    """
    短信验证码
    """
    def get(self,request,mobile):
        pass