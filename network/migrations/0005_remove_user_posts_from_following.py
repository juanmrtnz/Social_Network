# Generated by Django 4.1.6 on 2023-03-09 15:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_user_posts_from_following_alter_user_followers_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='posts_from_following',
        ),
    ]
