# Generated by Django 4.2.15 on 2024-09-19 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myfiles', '0009_mymodel_set_message_gurux_id_set_message_users_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='set_message',
            name='vaqt_minut',
        ),
        migrations.RemoveField(
            model_name='set_message',
            name='vaqt_soat',
        ),
        migrations.AddField(
            model_name='set_message',
            name='vaqt',
            field=models.CharField(default=1, max_length=30),
            preserve_default=False,
        ),
    ]
