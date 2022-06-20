from rest_framework import serializers
from .models import User as UserModel
from .models import UserProfile as UserProfileModel
from blog.models import Article as ArticleModel
from blog.models import Comment as CommentModel


class CommentSerializer(serializers.ModelSerializer):

    user = serializers.SerializerMethodField()
    def get_user(self, obj):
        return obj.user.email

    class Meta:
        model = CommentModel
        fields = ["content", "user"]


class ArticleSerializer(serializers.ModelSerializer):

    comment_set = CommentSerializer(many=True)
    category = serializers.SerializerMethodField()
    def get_category(self, obj):
        print(obj.category.all())
        categorys = []
        for category in obj.category.all():
            categorys.append(category.category)
        return categorys

    class Meta:
        model = ArticleModel
        fields = ["title", "content", "comment_set", "category"]


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfileModel
        fields = ["introduction", "birthday", "age", "hobby"]


class UserSerializer(serializers.ModelSerializer):

    userprofile = UserProfileSerializer()
    article_set = ArticleSerializer(many=True)

    class Meta:
        model = UserModel
        fields = ["username", "email", "fullname", "join_date", "userprofile", "article_set"]