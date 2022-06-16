from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from user.models import User as UserModel
from .models import Article as ArticleModel


# 내 게시글 보기
class Mypost (APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user_id = request.user.id
        posts = ArticleModel.objects.filter(user=user_id).values()
        
        for post in posts:
            title = post.get('title')
            print(title)
        return Response({'message': 'get 요청 받았습니다'})