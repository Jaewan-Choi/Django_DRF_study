from django.db import models
from user.models import User as UserModel

# 카테고리 테이블
class Category(models.Model):
    category = models.CharField("카테고리", max_length=10, unique=True)
    desc = models.TextField("설명", max_length=256)

    def __str__(self):
        return f"{self.category}"


# 게시글 테이블
class Article(models.Model):
    user = models.ForeignKey(UserModel, verbose_name="작성자", on_delete=models.CASCADE)
    title = models.CharField("제목", max_length=20)
    category = models.ManyToManyField(Category, verbose_name="카테고리")
    content = models.TextField("내용")

    def __str__(self):
        return f"{self.title} / {self.user.username}"