# Generated by Django 4.1.4 on 2023-02-08 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0004_alter_candidatesapplied_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='jobType',
            field=models.CharField(choices=[('Permanent', 'Permanent'), ('Temporary', 'Temporary'), ('Internship', 'Internship')], default='Permanent', max_length=10),
        ),
    ]
