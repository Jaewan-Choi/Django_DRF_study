# Generated by Django 4.0.5 on 2022-06-20 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_article_end_view_alter_article_start_view'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='end_view',
            field=models.DateTimeField(null=True, verbose_name='노출 종료 일자'),
        ),
        migrations.AlterField(
            model_name='article',
            name='start_view',
            field=models.DateTimeField(null=True, verbose_name='노출 시작 일자'),
        ),
    ]
