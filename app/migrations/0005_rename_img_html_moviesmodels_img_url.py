# Generated by Django 4.2.6 on 2023-10-09 14:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_rename_image_url_moviesmodels_img_html'),
    ]

    operations = [
        migrations.RenameField(
            model_name='moviesmodels',
            old_name='img_html',
            new_name='img_url',
        ),
    ]
