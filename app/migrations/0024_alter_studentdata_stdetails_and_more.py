# Generated by Django 4.1.7 on 2023-05-03 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0023_studentdata_stdetails_studentdata_stfeedback'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentdata',
            name='stDetails',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='studentdata',
            name='stFeedBack',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
    ]
