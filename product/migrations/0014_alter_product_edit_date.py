# Generated by Django 4.0.5 on 2022-06-22 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0013_alter_product_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='edit_date',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='수정일'),
        ),
    ]
