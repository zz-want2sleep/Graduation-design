# Generated by Django 2.2.7 on 2020-01-04 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userextension1',
            name='school',
            field=models.CharField(blank=True, default='中南林业科技大学涉外学院', max_length=100, null=True),
        ),
    ]
