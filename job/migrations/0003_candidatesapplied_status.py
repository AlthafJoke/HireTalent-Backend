# Generated by Django 4.1.4 on 2023-02-07 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0002_candidatesapplied_is_approved_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidatesapplied',
            name='status',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
