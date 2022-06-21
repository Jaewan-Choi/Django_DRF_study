from rest_framework import serializers
from .models import User as UserModel
from .models import UserProfile as UserProfileModel
from blog.models import Article as ArticleModel
from blog.models import Comment as CommentModel
from django.contrib.auth.hashers import make_password


class CommentSerializer(serializers.ModelSerializer):

    user = serializers.SerializerMethodField()
    def get_user(self, obj):
        return obj.user.email

    class Meta:
        model = CommentModel
        fields = ["content", "user"]


class ArticleSerializer(serializers.ModelSerializer):

    def validate(self, data):
        if self.context.get("request").method == 'PUT':
            return data

    def update(self, article, validated_data):
        for key, value in validated_data.items():
            setattr(article, key, value)
        article.save()
        # 카테고리 저장안됨
        # article.category.add()

        return article

    class Meta:
        model = ArticleModel
        fields = ["title", "content", "comment_set", "category"]

    comment_set = CommentSerializer(many=True)
    category = serializers.SerializerMethodField()
    def get_category(self, obj):
        categorys = []
        for category in obj.category.all():
            categorys.append(category.category)
        return categorys


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfileModel
        fields = ["introduction", "birthday", "age", "hobby"]


class UserSerializer(serializers.ModelSerializer):

    def validate(self, data):
        if self.context.get("request").method == 'POST':
            return data

        if self.context.get("request").method == 'PUT':
            return data

    def create(self, validation_data):
        password = validation_data.pop('password')
        password = make_password(password)
        validation_data['password'] = password

        UserModel.objects.create(**validation_data)

        return validation_data

    def update(self, user, validation_data):
        password = validation_data.pop('password')
        password = make_password(password)
        validation_data['password'] = password

        for key, value in validation_data.items():
            setattr(user, key, value)
        user.save()

        return user

    userprofile = UserProfileSerializer(read_only=True)
    article_set = ArticleSerializer(many=True, read_only=True)

    class Meta:
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'read_only': True}
        }
        model = UserModel
        fields = ["username", "email", "fullname", "join_date", "userprofile", "article_set", "password"]