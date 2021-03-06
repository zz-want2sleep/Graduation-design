# Generated by Django 2.2.7 on 2020-01-07 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0013_auto_20200107_1429'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='pic',
            field=models.ImageField(blank=True, default='defaultImage/404.png', help_text='上传相应的图片。', null=True, unique=True, upload_to='BookImage', verbose_name='picture'),
        ),
    ]
