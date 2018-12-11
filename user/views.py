from django.shortcuts import render
from rest_framework.response import Response
from django.views import View

# Create your views here.


from django.shortcuts import render, redirect
from rest_framework import viewsets, mixins,status
from rest_framework.views import APIView


class UserLoginView(APIView):
    """
        post:

        > 登录

    """
    def post(request):
        if request.method == "POST":
            username = request.POST.get('userName')
            password = request.POST.get('password')
            print(username)
            print(password)
        return Response(data=123, status=status.HTTP_200_OK)


class UserLogoutView(APIView):
    """
        get:

        > 退出
    """
    def get(request):
        pass
        return Response(data=123, status=status.HTTP_200_OK)