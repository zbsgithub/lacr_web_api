from rest_framework.response import Response
from django.views import View

# Create your views here.

from rest_framework import viewsets, mixins,status
from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny

class UserLoginView(APIView):
    """
        post:

        > 登录接口

    """

    def post(self, request, *args, **kwargs):
        user_name = request.data.get("userName")
        pwd = request.data.get("password")
        res = {"state_code": 200, "msg": None}
        print(user_name)
        if user_name == 'super_admin':
            res['msg'] = "success"
            res["state_code"] = 200
            res['token'] = "super_admin"
        else:
            res["msg"] = "用户名或者密码错误"
            res["state_code"] = 110

        return Response(data=res, status=status.HTTP_200_OK)

class UserLogoutView(APIView):
    """
        get:

        > 退出
    """
    def post(self, request, *args, **kwargs):
        token = request.data.get("token")
        return Response(data=123, status=status.HTTP_200_OK)


class UserGetInfo(APIView):
    permission_classes = [AllowAny]

    """
        get:

        > 获取用户信息

    """

    def get(self, request, *args, **kwargs):
        token = request.GET.get("token")
        res = {"state_code": 200, "msg": None}
        if token == "super_admin":
            res['msg'] = "success"
            res["state_code"] = 200

            res['token'] = "super_admin"
            res['name'] = "super_admin"
            res['user_id'] = "1"
            res['access'] = ['super_admin', 'admin'],
            res['avator'] = 'https://file.iviewui.com/dist/a0e88e83800f138b94d2414621bd9704.png'

        else:
            res['msg'] = "get user info faild"
            res["state_code"] = 201
            res['token'] = None

        return Response(data=res, status=status.HTTP_200_OK)

    def perform_authentication(self, request):
        """
        重写父类的用户验证方法,不在进入视图以前检查JWT
        保证用户未登录也可以进入下面的请求方法,不让它执行request.user
        """
        pass