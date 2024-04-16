import jwt
from rest_framework import status
from rest_framework.response import Response

from Todo.settings import SECRET_KEY
from accounts.models import User


def login_check(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.COOKIES.get('access')
            payload = jwt.decode(access_token, SECRET_KEY, algorithms='HS256')
            user = User.objects.get(id=payload['user_id'])
            request.user = user
        except jwt.exceptions.DecodeError:
            return Response({'message': '유효하지 않은 토큰입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'message': '존재하지 않는 사용자 입니다. '}, status=status.HTTP_400_BAD_REQUEST)
        return func(self, request, *args, **kwargs)
    return wrapper