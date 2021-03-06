# Generated by Django 4.0.5 on 2022-06-22 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_alter_product_thumbnail'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='edit_date',
            field=models.DateField(auto_now=True, null=True, verbose_name='수정일'),
        ),
        migrations.AddField(
            model_name='product',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='활성화 여부'),
        ),
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.IntegerField(null=True, verbose_name='가격'),
        ),
        migrations.AlterField(
            model_name='product',
            name='desc',
            field=models.TextField(max_length=256, verbose_name='상품 설명'),
        ),
    ]
