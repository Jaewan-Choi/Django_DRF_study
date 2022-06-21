from django.db import models
from user.models import User as UserModel


class Product(models.Model):
    creator = models.ForeignKey(UserModel, verbose_name="작성자", on_delete=models.CASCADE)
    title = models.CharField("제목", max_length=20)
    thumbnail = models.FileField("썸네일", upload_to='product/', max_length=256)
    desc = models.TextField("설명", max_length=256)
    created_time = models.DateTimeField("등록 일자", auto_now_add=True)
    start_view = models.DateTimeField("노출 시작일", null=True)
    end_view = models.DateTimeField("노출 종료일", null=True)

    def __str__(self):
        return f"[제품] {self.title} / {self.creator.email}"