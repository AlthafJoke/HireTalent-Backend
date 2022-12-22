# Generated by Django 4.1.4 on 2022-12-22 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0007_alter_job_experience'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='experience',
            field=models.CharField(choices=[('No Experience', 'No Expirience'), ('1 Year', 'One Year'), ('2 Years', 'Two Year'), ('3 Years above', 'Three Year Plus')], default='No Experience', max_length=20),
        ),
    ]
