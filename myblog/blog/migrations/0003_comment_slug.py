# Generated by Django 4.2.4 on 2023-08-18 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_entry_options_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='slug',
            field=models.SlugField(default=''),
        ),
    ]
