# Generated by Django 3.0.5 on 2020-06-15 16:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20200609_1339'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={'ordering': ['-created']},
        ),
        migrations.RenameField(
            model_name='blog',
            old_name='created_at',
            new_name='created',
        ),
    ]
