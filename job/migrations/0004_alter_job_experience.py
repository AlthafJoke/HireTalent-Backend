# Generated by Django 4.1.4 on 2022-12-22 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0003_alter_job_experience'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='experience',
            field=models.CharField(choices=[('No_Expirence', 'No Expirience'), ('1-Year', 'One Year'), ('2-years', 'Two Year'), ('3-Year&above', 'Three Year Plus')], default='No_Expirence', max_length=20),
        ),
    ]
