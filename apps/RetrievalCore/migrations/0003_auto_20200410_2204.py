# Generated by Django 2.0 on 2020-04-10 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RetrievalCore', '0002_auto_20200409_2223'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='D_vector',
            field=models.TextField(blank=True, null=True, verbose_name='D向量'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='P_vector',
            field=models.TextField(blank=True, null=True, verbose_name='P向量'),
        ),
    ]
