from django.db import models
from user.models import User as UserModel
from django.core.validators import MaxValueValidator, MinValueValidator


class Product(models.Model):
    creator = models.ForeignKey(UserModel, verbose_name="작성자", on_delete=models.CASCADE)
    title = models.CharField("제목", max_length=20)
    thumbnail = models.FileField("썸네일", upload_to='product/')
    desc = models.TextField("상품 설명", max_length=256)
    created_time = models.DateTimeField("등록 일자", auto_now_add=True)
    start_view = models.DateTimeField("노출 시작일", null=True)
    end_view = models.DateTimeField("노출 종료일")
    price = models.IntegerField("가격")
    edit_date = models.DateTimeField("수정일", auto_now=True, null=True)
    is_active = models.BooleanField("활성화 여부", default=True)

    def __str__(self):
        return f"[제품]🔸id : {self.id} / 제목 : {self.title} / 작성자 : {self.creator.email}🔸"


class Review(models.Model):
    author = models.ForeignKey(UserModel, verbose_name="작성자", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name="상품", on_delete=models.CASCADE)
    desc = models.TextField("내용", max_length=256)
    rating = models.IntegerField("평점", default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_time = models.DateTimeField("작성일", auto_now_add=True)

    def __str__(self):
        return f"[리뷰]🔸id : {self.id} / 상품 : {self.product.title} / 작성자 : {self.author.email}🔸"