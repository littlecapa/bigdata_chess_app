# Generated by Django 4.1.5 on 2024-11-24 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LichessConfigModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('download_base_url', models.CharField(default='https://database.lichess.org/', max_length=255)),
                ('download_month_pattern', models.CharField(default='standard/lichess_db_standard_rated_<<year>>-<<month>>.pgn.zst', max_length=255)),
                ('script_name_unzst', models.CharField(default='lichess_unzst.sh', max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LichessFolderConfigModel',
            fields=[
                ('ip', models.GenericIPAddressField(primary_key=True, serialize=False)),
                ('download_folder_path', models.CharField(max_length=255)),
                ('eco_split_folder_path', models.CharField(max_length=255)),
                ('reduced_folder_path', models.CharField(max_length=255)),
                ('evaluated_folder_path', models.CharField(max_length=255)),
                ('script_folder_path', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LichessStatusModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.PositiveIntegerField()),
                ('month', models.PositiveIntegerField()),
                ('status', models.PositiveIntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]