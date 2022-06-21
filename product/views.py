from rest_framework.views import APIView
from .serializers import ProductSerializer
from rest_framework.response import Response
from rest_framework import status
from product.models import Product as ProductModel
from django.db.models.query_utils import Q
from datetime import datetime
from rest_framework import permissions


class Product(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user.id

        serch = Q(start_view__lt=datetime.now(), end_view__gt=datetime.now())
        products = ProductModel.objects.filter(serch, creator=user)

        product_serializer = ProductSerializer(products, many=True).data
        return Response({'product_serializer': product_serializer}, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user.id
        request.data['creator'] = user
        product_serializer = ProductSerializer(data=request.data, context={"request": request})

        if product_serializer.is_valid():
            product_serializer.save()
            product_serializer = product_serializer.data
            return Response({'product_serializer': product_serializer}, status=status.HTTP_200_OK)

        return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, obj_id):
        user = request.user.id
        request.data['creator'] = user
        product = ProductModel.objects.get(id=obj_id)
        product_serializer = ProductSerializer(product, data=request.data, context={"request": request}, partial=True)

        if product_serializer.is_valid():
            product_serializer.save()
            product_serializer = product_serializer.data
            return Response({'product_serializer': product_serializer}, status=status.HTTP_200_OK)

        return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)