# Generated by Django 3.2.18 on 2023-03-16 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_rename_image_post_featured_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='Featured_image',
            new_name='featured_image',
        ),
        migrations.AddField(
            model_name='post',
            name='thumbnail_image',
            field=models.ImageField(blank=True, null=True, upload_to='thumbnail_image/%Y/%m/%d/'),
        ),
    ]