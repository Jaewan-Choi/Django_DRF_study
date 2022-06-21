from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import permissions
from .models import User as UserModel
from .serializers import UserSerializer
from django.contrib.auth import login, logout, authenticate


class UserView(APIView): # CBV 방식
    # permission_classes = [permissions.AllowAny] # 누구나 view 조회 가능 (설정하지 않았을 때 기본값)
    # permission_classes = [permissions.IsAdminUser] # admin만 view 조회 가능
    permission_classes = [permissions.IsAuthenticated] # 로그인 된 사용자만 view 조회 가능

    # 사용자 정보 조회
    def get(self, request):
        user = request.user
        user_serialize = UserSerializer(user).data

        return Response({'user_serialize': user_serialize}, status=status.HTTP_200_OK)
    
    # 회원가입
    def post(self, request):
        user_serializer = UserSerializer(data=request.data, context={'request': request})

        if user_serializer.is_valid():
            user_serializer.save()
            user_serializer = user_serializer.data
            return Response({'User_Serializer': user_serializer}, status=status.HTTP_200_OK)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 로그인 사용자의 회원 정보 수정
    def put(self, request):
        user_id = request.user.id
        user = UserModel.objects.get(id=user_id)
        user_serializer = UserSerializer(user, data=request.data, context={'request': request}, partial=True)
        
        if user_serializer.is_valid():
            user_serializer.save()
            user_serializer = user_serializer.data
            return Response({'User_Serializer': user_serializer}, status=status.HTTP_200_OK)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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