# Generated by Django 2.2 on 2022-01-17 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subjects', '0004_commentvote_postvote'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentvote',
            name='vote',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='postvote',
            name='vote',
            field=models.IntegerField(),
        ),
    ]
