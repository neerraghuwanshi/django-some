# Generated by Django 3.1 on 2021-01-31 07:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0016_comment_created'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-id']},
        ),
    ]
