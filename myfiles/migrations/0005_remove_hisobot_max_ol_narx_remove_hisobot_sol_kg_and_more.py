# Generated by Django 4.2.15 on 2024-09-18 11:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myfiles', '0004_baza_hisobot'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hisobot',
            name='max_ol_narx',
        ),
        migrations.RemoveField(
            model_name='hisobot',
            name='sol_kg',
        ),
        migrations.RemoveField(
            model_name='hisobot',
            name='sol_narx',
        ),
    ]
