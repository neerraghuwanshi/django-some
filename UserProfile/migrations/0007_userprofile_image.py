# Generated by Django 3.0.5 on 2020-06-06 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserProfile', '0006_remove_userprofile_posts'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
    ]
