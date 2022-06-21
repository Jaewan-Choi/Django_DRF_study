from rest_framework import serializers
from .models import Product as ProductModel


class ProductSerializer(serializers.ModelSerializer):

    def validate(self, data):
        if self.context.get("request").method == 'POST':
            return data
        
        elif self.context.get("request").method == 'PUT':
            return data

    def create(self, validated_data):
        ProductModel.objects.create(**validated_data)
        return validated_data

    def update(self, product, validated_data):
        for key, value in validated_data.items():
            setattr(product, key, value)
        product.save()

        return product

    class Meta:
        model = ProductModel
        fields = "__all__"