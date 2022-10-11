# Generated by Django 2.2.16 on 2022-05-15 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0018_follow'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='follow',
            options={},
        ),
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.UniqueConstraint(fields=('user', 'author'), name='uniq_follow'),
        ),
    ]