# Generated by Django 4.1.5 on 2024-12-11 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chess', '0006_alter_lichessconfigmodel_script_name_unzst'),
    ]

    operations = [
        migrations.AddField(
            model_name='lichessconfigmodel',
            name='script_name_concat',
            field=models.CharField(default='concat_pgn.sh', max_length=255),
        ),
        migrations.AlterField(
            model_name='lichessconfigmodel',
            name='script_name_unzst',
            field=models.CharField(default='lichess_unzst.sh', max_length=255),
        ),
    ]
