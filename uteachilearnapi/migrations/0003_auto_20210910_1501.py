# Generated by Django 3.2.7 on 2021-09-10 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uteachilearnapi', '0002_auto_20210910_1455'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='app_user',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='message',
            name='timestamp',
            field=models.ImageField(upload_to=''),
        ),
    ]