from django.db import models
from user.models import User as UserModel


# 카테고리 테이블
class Category(models.Model):
    category = models.CharField("카테고리", max_length=10)
    desc = models.TextField("설명", max_length=256, blank=True)

    def __str__(self):
        return f"[카테고리] {self.category}"


# 게시글 테이블
class Article(models.Model):
    user = models.ForeignKey(UserModel, verbose_name="작성자", on_delete=models.CASCADE)
    title = models.CharField("제목", max_length=5)
    category = models.ManyToManyField(Category, verbose_name="카테고리")
    content = models.TextField("내용", max_length=20)
    start_view = models.DateTimeField("노출 시작 일자", null=True)
    end_view = models.DateTimeField("노출 종료 일자", null=True)

    def __str__(self):
        return f"[게시글] {self.title} / {self.user.email}"


# 코멘트 테이블
class Comment(models.Model):
    article = models.ForeignKey(Article, verbose_name="게시글", on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(UserModel, verbose_name="작성자", on_delete=models.SET_NULL, null=True)
    content = models.TextField("내용")

    def __str__(self):
        return f"[코멘트] {self.content} / {self.user.email}"