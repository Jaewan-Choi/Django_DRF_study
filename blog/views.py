from rest_framework.response import Response
from rest_framework.views import APIView
from DRF.permissions import IsAdminOrIsAuthenticatedReadOnly
from user.serializers import ArticleSerializer
from user.models import User as UserModel
from .models import Article as ArticleModel
from .models import Category as CategoryModel
from datetime import datetime, timedelta
from rest_framework import status


class Article(APIView):
    permission_classes = [IsAdminOrIsAuthenticatedReadOnly]

    # 게시글 조회
    def get(self, request):
        user = request.user
        articles = ArticleModel.objects.filter(user=user, start_view__lt=datetime.now(), end_view__gt=datetime.now()).order_by('-id').values()
        return Response({'articles': articles})

    # 게시글 작성
    def post(self, request):
        user = request.user
        if user.join_date > (datetime.now() - timedelta(minutes=3)):
            return Response({'message': '가입일이 3일이상인 유저만 작성가능합니다'})

        title = request.data.get('title', '')
        category = request.data.get('category', '')
        content = request.data.get('content', '')

        if len(title) > 5:
            return Response({'message': '제목은 5글자를 이하하여야합니다'})

        elif len(content) > 20:
            return Response({'message': '내용은 20글자를 이하여야 합니다'})

        elif not category:
            return Response({'message': '카테고리를 선택해주세요'})

        user = UserModel.objects.get(email=user.email)

        if ',' in category:
            categorys = category.split(',')
            
            category_list = []
            for category in categorys:
                if not CategoryModel.objects.filter(category=category):
                    return Response({'message': '존재하지않는 카테고리입니다'})
                
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

            return Response({'message': '게시글 작성 완료'})

        else:
            if not CategoryModel.objects.filter(category=category):
                return Response({'message': '존재하지않는 카테고리입니다'})

            category = CategoryModel.objects.get(category=category)

            article = ArticleModel(
                user = user,
                title = title,
                content = content
            )
            article.save()
            article.category.add(category)

            return Response({'message': '게시글 작성 완료'})

    # 게시글 수정
    def put(self, request, obj_id):
        article = ArticleModel.objects.get(id=obj_id)
        if article.user.pk != request.user.id:
            return Response({'message': '본인 게시글만 수정 가능합니다'}, status=status.HTTP_400_BAD_REQUEST)

        article_serializer = ArticleSerializer(article, data=request.data, context={"request": request}, partial=True)
        if article_serializer.is_valid():
            article_serializer.save()
            print(article_serializer.data)
            return Response(article_serializer.data, status=status.HTTP_200_OK)
        
        return Response(article_serializer.errors, status=status.HTTP_400_BAD_REQUEST)