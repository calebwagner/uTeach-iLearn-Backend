# Generated by Django 3.2.7 on 2021-09-16 11:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('uteachilearnapi', '0011_alter_meeting_scheduled_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='connection',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='connection', to='uteachilearnapi.appuser'),
        ),
    ]