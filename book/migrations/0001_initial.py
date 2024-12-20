# Generated by Django 5.1.3 on 2024-12-11 20:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isbn', models.CharField(blank=True, max_length=13, null=True)),
                ('title', models.CharField(max_length=255)),
                ('publication_date', models.DateField()),
                ('page_count', models.PositiveIntegerField()),
                ('tags', models.JSONField(default=list)),
                ('description', models.TextField(blank=True, max_length=800, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='book_images/')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books', to='book.author')),
                ('genres', models.ManyToManyField(related_name='books', to='book.genre')),
                ('publisher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books', to='book.publisher')),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField()),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserLibrary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('read', 'Прочитано'), ('planned', 'Хочу прочитать')], max_length=10)),
                ('last_change_date', models.DateField(auto_now_add=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
