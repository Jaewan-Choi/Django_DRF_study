from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import permissions
from .serializers import UserSerializer
from django.contrib.auth import login, logout, authenticate

class UserView(APIView): # CBV 방식
    # permission_classes = [permissions.AllowAny] # 누구나 view 조회 가능 (설정하지 않았을 때 기본값)
    # permission_classes = [permissions.IsAdminUser] # admin만 view 조회 가능
    permission_classes = [permissions.IsAuthenticated] # 로그인 된 사용자만 view 조회 가능

    # 사용자 정보 조회
    def get(self, request):
        user = request.user
        userserialize = UserSerializer(user).data
        return Response({'userserialize': userserialize})
    
    # 회원가입
    def post(self, request):
        return Response({'message': 'post method!!'})

    # 회원 정보 수정
    def put(self, request):
        return Response({'message': 'put method!!'})

    # 회원 탈퇴
    def delete(self, request):
        return Response({'message': 'delete method!!'})


class UserApiView(APIView):
    permission_classes = [permissions.AllowAny]

    # 로그인
    def post(self, request):
        email = request.data.get('email', '')
        password = request.data.get('password', '')

        user = authenticate(request, email=email, password=password)

        # 인증 실패시
        if not user:
            return Response({"error": "존재하지 않는 계정이거나 패스워드가 일치하지 않습니다."})

        login(request, user)
        return Response({"message": "로그인 성공!!"})

    # 로그아웃
    def delete(self, request):
        logout(request)
        return Response({"message": "로그아웃 성공"})