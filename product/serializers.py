from rest_framework import serializers
from .models import Product as ProductModel, Review
from .models import Review as ReviewModel
from user.models import User as UserModel
from datetime import datetime


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReviewModel
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):

    creator_email = serializers.SerializerMethodField()
    is_active = serializers.BooleanField(default=True)
    avg_rating = serializers.SerializerMethodField()
    recent_review = serializers.SerializerMethodField()

    def get_creator_email(self, obj):
        creator_email = obj.creator.email
        return creator_email

    def get_recent_review(self, obj):
        if not obj.review_set.values():
            return '리뷰가 없습니다'
        reviews = list(obj.review_set.values())[-1]
        author_id = reviews['author_id']

        author = UserModel.objects.get(id=author_id).email
        desc = reviews['desc']
        review = {'작성자': author, '내용': desc}
        return review

    def get_avg_rating(self, obj):
        if not obj.review_set.values():
            return '평점이 없습니다'
        reviews = list(obj.review_set.values())
        ratings = []
        for review in reviews:
            rating = review['rating']
            ratings.append(rating)
        avg_rating = round(sum(ratings) / len(ratings), 1)
        return avg_rating

    def validate(self, data):
        if self.context.get("request").method == 'POST':
            return data
        
        elif self.context.get("request").method == 'PUT':
            return data

    def create(self, validated_data):
        validated_data['desc'] = f"{validated_data['desc']} \n <{datetime.now()}에 등록된 상품입니다>"
        validated_data = ProductModel.objects.create(**validated_data)
        return validated_data

    def update(self, product, validated_data):
        for key, value in validated_data.items():
            setattr(product, key, value)

        if product.created_time == product.edit_date:
            product.save()
            product.desc = f"<{product.edit_date}에 수정됨> \n {product.desc}"
            product.save()
            return product

        split_desc_list = product.desc.split("\n")
        split_desc ="\n".join(split_desc_list[1:])
        edited_desc = f"<{product.edit_date}에 수정됨> \n {split_desc}"
        product.desc = edited_desc
        product.save()
        return product

    class Meta:
        model = ProductModel
        fields = ["pk", "creator", "creator_email", "title", "thumbnail", "desc", "created_time", "start_view",
                    "end_view", "price", "edit_date", "is_active", "avg_rating", "recent_review"]
        extra_kwargs = {
            'creator': {'write_only': True}
        }