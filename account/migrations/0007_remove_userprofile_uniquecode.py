# Generated by Django 4.1.4 on 2023-01-10 09:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_rename_companay_userprofile_company'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='uniqueCode',
        ),
    ]