from rest_framework.views import APIView
from .serializers import ProductSerializer
from rest_framework.response import Response
from rest_framework import status
from product.models import Product as ProductModel
from django.db.models.query_utils import Q
from datetime import datetime
from DRF.permissions import IsAdminOr3DaysAuthenticatedOrReadOnly


class Product(APIView):
    permission_classes = [IsAdminOr3DaysAuthenticatedOrReadOnly]

    # 상품 조회
    def get(self, request):
        if request.user.id:
            user = request.user.id

            serch = Q(start_view__lt=datetime.now(), end_view__gt=datetime.now(), is_active=True)
            products = ProductModel.objects.filter(serch, creator=user)

            product_serializer = ProductSerializer(products, many=True).data
            return Response({'product_serializer': product_serializer}, status=status.HTTP_200_OK)

        serch = Q(start_view__lt=datetime.now(), end_view__gt=datetime.now(), is_active=True)
        products = ProductModel.objects.filter(serch)

        product_serializer = ProductSerializer(products, many=True).data
        return Response({'product_serializer': product_serializer}, status=status.HTTP_200_OK)

    # 상품 등록
    def post(self, request):
        end_view = datetime.strptime(request.data['end_view'], '%Y-%m-%d %H:%M:%S')
        if end_view < datetime.now():
            return Response({'message': '노출 종료 일자는 현재 시점보다 이후 시점이어야합니다'})

        user = request.user.id
        request.data['creator'] = user
        product_serializer = ProductSerializer(data=request.data, context={"request": request})

        if product_serializer.is_valid():
            product_serializer.save()
            return Response(product_serializer.data, status=status.HTTP_200_OK)

        return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 상품 수정
    def put(self, request, obj_id):
        user = request.user.id
        product = ProductModel.objects.get(id=obj_id)
        if not user == product.creator.pk:
            return Response({'message': '본인의 상품만 수정할 수 있습니다'}, status=status.HTTP_400_BAD_REQUEST)

        request.data['creator'] = user
        product_serializer = ProductSerializer(product, data=request.data, context={"request": request}, partial=True)

        if product_serializer.is_valid():
            product_serializer.save()
            return Response(product_serializer.data, status=status.HTTP_200_OK)

        return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)