# Generated by Django 3.2.12 on 2022-02-22 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userpage', '0005_post_poster_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.CharField(default=0, max_length=32),
            preserve_default=False,
        ),
    ]
