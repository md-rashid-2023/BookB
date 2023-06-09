# Generated by Django 3.2 on 2023-05-09 20:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book_store_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSiteSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dark_theme', models.BooleanField(default=False)),
                ('fk_user', models.ForeignKey(db_column='fk_user', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
