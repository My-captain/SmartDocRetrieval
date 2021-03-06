# Generated by Django 2.0 on 2020-04-07 20:59

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=2048, verbose_name='文献标题')),
                ('publish_year', models.IntegerField(default=2019, verbose_name='发布年份')),
                ('authors', models.TextField(verbose_name='作者列表')),
                ('abstract', models.TextField(verbose_name='文献摘要')),
                ('doi_url', models.TextField(verbose_name='原文详情页链接')),
                ('references', models.TextField(verbose_name='引用列表')),
                ('publication', models.TextField(verbose_name='文献发表信息')),
                ('classification', models.IntegerField(blank=True, default=-1, null=True, verbose_name='所属类别')),
                ('feature_vector', models.TextField(blank=True, null=True, verbose_name='特征向量')),
            ],
            options={
                'verbose_name': '文献',
                'verbose_name_plural': '文献',
            },
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('D_vector', models.TextField(verbose_name='D向量')),
                ('P_vector', models.TextField(verbose_name='P向量')),
                ('precision', models.FloatField(verbose_name='此此session的准确率')),
                ('documents', models.ManyToManyField(to='RetrievalCore.Document', verbose_name='会话文档')),
            ],
            options={
                'verbose_name': '会话',
                'verbose_name_plural': '会话',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(default='', max_length=50, unique=True, verbose_name='昵称')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': '用户信息',
                'db_table': 'user_profile',
                'verbose_name_plural': '用户信息',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='session',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='会话用户'),
        ),
    ]
