# Generated by Django 3.2.7 on 2021-09-13 18:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uteachilearnapi', '0007_alter_message_read'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='read',
        ),
    ]
