# Generated by Django 3.2.7 on 2021-09-22 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uteachilearnapi', '0013_alter_meeting_connection'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='image_url',
            field=models.ImageField(null=True, upload_to='images'),
        ),
    ]
