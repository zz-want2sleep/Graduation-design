# Generated by Django 2.2.7 on 2019-12-21 06:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0008_history'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoryByManager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('books', models.CharField(help_text='Enter some book titles', max_length=200)),
                ('rent_time', models.DateField(blank=True, help_text='时间格式：2019/12/11', null=True)),
                ('master', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['rent_time'],
            },
        ),
    ]
