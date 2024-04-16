import jwt
import rest_framework_simplejwt.exceptions
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

from Todo.settings import SECRET_KEY
from accounts.models import User
from accounts.serializers import UserSerializer


class SignUpAPIView(APIView):
    # 회원가입
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            response = Response({"user": serializer.data, "message": "Signup success",
                                 "token": {"access": access_token, "refresh": refresh_token}},
                                status=status.HTTP_200_OK)
            response.set_cookie("access", access_token, httponly=True)
            response.set_cookie("refresh", refresh_token, httponly=True)

            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthAPIView(APIView):
    # token에 따른 user 정보 가져오기
    def get(self, request):
        try:
            access_token = request.COOKIES.get('access')
            payload = jwt.decode(access_token, SECRET_KEY, algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)
            serializer = UserSerializer(instance=user)
            response = Response(serializer.data, status=status.HTTP_200_OK)
            response.set_cookie('access', access_token)
            response.set_cookie('refresh', request.COOKIES.get('refresh'))
            return response
        # access toekn이 만료되었을 때
        except jwt.exceptions.ExpiredSignatureError:
            try:
                data = {'refresh': request.COOKIES.get('refresh', None)}
                serializer = TokenRefreshSerializer(data=data)
                if serializer.is_valid(raise_exception=True):
                    access_token = serializer.validated_data.get('access', None)
                    refresh_token = serializer.validated_data.get('refresh', None)
                    payload = jwt.decode(access_token, SECRET_KEY, algorithms=['HS256'])
                    pk = payload.get('user_id')
                    user = get_object_or_404(User, pk=pk)
                    serializer = UserSerializer(instance=user)
                    response = Response(serializer.data, status=status.HTTP_200_OK)
                    response.set_cookie('access', access_token)
                    response.set_cookie('refresh', refresh_token)
                    return response
            except rest_framework_simplejwt.exceptions.TokenError:
                return Response({"message": "로그인이 만료되었습니다."}, status=status.HTTP_200_OK)
            raise jwt.exceptions.InvalidTokenError
        except jwt.exceptions.InvalidTokenError:
            return Response({"message": "사용 불가능한 토큰입니다."}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"message": "존지하지 않는 사용자입니다."}, status=status.HTTP_400_BAD_REQUEST)

    # 로그인
    def post(self, request):
        user = authenticate(username=request.data.get('email'), password=request.data.get('password'))

        if user is not None:
            serializer = UserSerializer(user)
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            response = Response({"user": serializer.data, "message": "Login Success",
                                 "token": {"access": access_token, "refresh": refresh_token}},
                                status=status.HTTP_200_OK)
            response.set_cookie('access', access_token, httponly=True)
            response.set_cookie('refresh', refresh_token, httponly=True)
            return response
        else:
            return Response({"message": "존재하지 않는 사용자입니다."}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        response = Response({"message": "Logout Success"}, status=status.HTTP_200_OK)
        response.delete_cookie('access')
        response.delete_cookie('refresh')
        return response
