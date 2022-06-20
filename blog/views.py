from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import APIException
from user.models import User as UserModel
from .models import Article as ArticleModel
from .models import Category as CategoryModel
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

        if user.is_authenticated and user.join_date < (datetime.now() - timedelta(days=7)):
            return True
            
        elif user.is_admin:
            return True
            
        elif user.is_authenticated and request.method in self.SAFE_METHODS:
            return True
        
        return False


class Article(APIView):
    permission_classes = [IsAdminOrIsAuthenticatedReadOnly]

    def get(self, request):
        user = request.user
        articles = ArticleModel.objects.filter(user=user, start_view__lt=datetime.now(), end_view__gt=datetime.now()).order_by('-id').values()
        return Response({'articles': articles})


    def post(self, request):
        user = request.user
        if user.join_date > (datetime.now() - timedelta(minutes=3)):
            return Response({'message': '가입일이 3일이상인 유저만 작성가능합니다'})

        title = request.data.get('title', '')
        category = request.data.get('category', '')
        content = request.data.get('content', '')

        if len(title) <= 5:
            return Response({'message': '제목은 5글자를 초과하여야합니다'})

        elif len(content) <= 20:
            return Response({'message': '내용은 20글자를 초과하여야 합니다'})

        elif not category:
            return Response({'message': '카테고리를 선택해주세요'})

        user = UserModel.objects.get(email=user.email)

        if ',' in category:
            categorys = category.split(',')
            category_list = []
            for category in categorys:
                category = CategoryModel.objects.get(category=category)
                category_list.append(category)

            article = ArticleModel(
                user = user,
                title = title,
                content = content
            )
            article.save()
            for category in category_list:
                article.category.add(category)

        else:
            category = CategoryModel.objects.get(category=category)

            article = ArticleModel(
                user = user,
                title = title,
                content = content
            )
            article.save()
            article.category.add(category)

        return Response({'message': '게시글 작성 완료'})