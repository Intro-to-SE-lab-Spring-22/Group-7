# Generated by Django 3.2.12 on 2022-02-21 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userpage', '0004_alter_comment_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='poster_id',
            field=models.IntegerField(default=1),
        ),
    ]