# Generated by Django 3.2.11 on 2022-01-14 21:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('image', models.TextField()),
                ('author', models.TextField()),
                ('publisher', models.TextField()),
                ('pubdate', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='LikedBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_detail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book_app.bookdetail')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_app.user')),
            ],
        ),
    ]