# Generated by Django 4.1.5 on 2024-12-11 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chess', '0004_remove_lichessfolderconfigmodel_script_folder_path_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='lichessfolderconfigmodel',
            name='eco_complete_folder_path',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='lichessfolderconfigmodel',
            name='evaluated_complete_folder_path',
            field=models.CharField(default='', max_length=255),
        ),
    ]
