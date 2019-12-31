# Generated by Django 2.2.7 on 2019-12-29 11:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0009_historybymanager'),
    ]

    operations = [
        migrations.CreateModel(
            name='Visitor1',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_key', models.CharField(max_length=40)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='visitor1', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
