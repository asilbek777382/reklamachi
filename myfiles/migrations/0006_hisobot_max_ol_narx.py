# Generated by Django 4.2.15 on 2024-09-18 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myfiles', '0005_remove_hisobot_max_ol_narx_remove_hisobot_sol_kg_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='hisobot',
            name='max_ol_narx',
            field=models.IntegerField(default=0),
        ),
    ]