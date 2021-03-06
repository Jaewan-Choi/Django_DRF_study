from rest_framework import status
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import APIException
from datetime import datetime, timedelta


class GenericAPIException(APIException):
    def __init__(self, status_code, detail=None, code=None):
        self.status_code=status_code
        super().__init__(detail=detail, code=code)


class IsAdminOrIsAuthenticatedReadOnly(BasePermission):
    SAFE_METHODS = ('GET', )
    message = '접근 권한이 없습니다.'

    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            response ={
                    "detail": "서비스를 이용하기 위해 로그인 해주세요.",
                }
            raise GenericAPIException(status_code=status.HTTP_401_UNAUTHORIZED, detail=response)

        if user.is_authenticated and user.join_date < (datetime.now() - timedelta(minutes=3)):
            return True
            
        elif user.is_admin:
            return True
            
        elif user.is_authenticated and request.method in self.SAFE_METHODS:
            return True
        
        return False


class IsAdminOr3DaysAuthenticatedOrReadOnly(BasePermission):
    NEED_AUTH_METHODS = ['POST', 'PUT', 'DELETE']
    message = '접근 권한이 없습니다.'

    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated and request.method == 'GET':
            return True
        
        elif not user.is_authenticated and request.method in self.NEED_AUTH_METHODS:
            response ={
                    "detail": "서비스를 이용하기 위해 로그인 해주세요.",
                }
            raise GenericAPIException(status_code=status.HTTP_401_UNAUTHORIZED, detail=response)

        elif user.is_authenticated and user.join_date < (datetime.now() - timedelta(minutes=3)):
            return True
            
        elif user.is_admin:
            return True
        
        return False