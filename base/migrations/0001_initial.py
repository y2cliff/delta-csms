# Generated by Django 5.1.7 on 2025-07-10 03:54

import base.models
import django.db.models.deletion
import django_currentuser.db.models.fields
import django_currentuser.middleware
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_updated', models.DateTimeField(auto_now=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('code', models.CharField(blank=True, max_length=60, null=True)),
                ('name', models.CharField(blank=True, max_length=60, null=True)),
                ('created_by', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL)),
                ('updated_by', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, on_update=True, related_name='%(class)s_updated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Department',
            },
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_updated', models.DateTimeField(auto_now=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('code', models.CharField(blank=True, max_length=8, null=True)),
                ('module', models.CharField(blank=True, max_length=60, null=True)),
                ('menu_type', models.CharField(choices=[('Module', 'Module'), ('Parent', 'Parent'), ('Menu', 'Menu'), ('Label', 'Label')], default='Module', max_length=10)),
                ('name', models.CharField(blank=True, max_length=60, null=True)),
                ('url_name', models.CharField(blank=True, max_length=60, null=True)),
                ('icon_class', models.CharField(blank=True, max_length=60, null=True)),
                ('created_by', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL)),
                ('updated_by', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, on_update=True, related_name='%(class)s_updated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='GroupProfile',
            fields=[
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_updated', models.DateTimeField(auto_now=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('group', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='profile', serialize=False, to='auth.group')),
                ('name', models.CharField(blank=True, max_length=60, null=True)),
                ('created_by', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL)),
                ('updated_by', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, on_update=True, related_name='%(class)s_updated', to=settings.AUTH_USER_MODEL)),
                ('menu', models.ManyToManyField(blank=True, related_name='groups', to='base.menu')),
            ],
            options={
                'verbose_name': 'Group Profile',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_updated', models.DateTimeField(auto_now=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='profile', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('about', models.TextField(blank=True, default='')),
                ('company', models.CharField(blank=True, max_length=60, null=True)),
                ('job', models.CharField(blank=True, max_length=60, null=True)),
                ('country', models.CharField(blank=True, max_length=60, null=True)),
                ('address', models.CharField(blank=True, max_length=60, null=True)),
                ('phone', models.CharField(blank=True, max_length=60, null=True)),
                ('image_file', models.ImageField(blank=True, height_field='image_height', null=True, upload_to=base.models.image_upload, verbose_name='image', width_field='image_width')),
                ('image_width', models.IntegerField(blank=True, null=True)),
                ('image_height', models.IntegerField(blank=True, null=True)),
                ('twitter', models.CharField(blank=True, max_length=60, null=True)),
                ('facebook', models.CharField(blank=True, max_length=60, null=True)),
                ('instagram', models.CharField(blank=True, max_length=60, null=True)),
                ('linkedin', models.CharField(blank=True, max_length=60, null=True)),
                ('created_by', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL)),
                ('menu', models.ManyToManyField(blank=True, related_name='users', to='base.menu')),
                ('updated_by', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, on_update=True, related_name='%(class)s_updated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Profile',
            },
        ),
    ]
