# Generated by Django 4.1.7 on 2023-04-13 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_alter_studentdata_assingto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(default='', max_length=10, unique=True),
        ),
    ]
