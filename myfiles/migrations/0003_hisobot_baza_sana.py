# Generated by Django 5.1.1 on 2024-09-12 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myfiles', '0002_baza_jami_narxi_baza_max_kg_baza_max_ol_narx_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='hisobot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_ismi', models.CharField(max_length=30)),
                ('max_ol_narx', models.IntegerField(default=0)),
                ('max_sol_narx', models.IntegerField(default=0)),
                ('max_kg', models.IntegerField(default=0)),
                ('jami_narxi', models.IntegerField(default=0)),
                ('sana', models.CharField(max_length=30)),
                ('klient', models.CharField(blank=True, max_length=30, null=True)),
                ('sol_narx', models.IntegerField(blank=True, default=0, null=True)),
                ('sol_kg', models.IntegerField(blank=True, default=0, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='baza',
            name='sana',
            field=models.CharField(default=1, max_length=30),
            preserve_default=False,
        ),
    ]
