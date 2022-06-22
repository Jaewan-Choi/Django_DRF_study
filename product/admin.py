from django.contrib import admin
from .models import Product as ProductModel
from .models import Review as ReviewModel


admin.site.register(ProductModel)
admin.site.register(ReviewModel)