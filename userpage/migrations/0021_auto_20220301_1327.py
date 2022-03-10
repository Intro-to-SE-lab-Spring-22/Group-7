# Generated by Django 3.2.12 on 2022-03-01 19:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userpage', '0020_alter_like_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='comment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='userpage.comment'),
        ),
        migrations.AlterField(
            model_name='like',
            name='post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='userpage.post'),
        ),
    ]