# Generated by Django 3.2.19 on 2023-07-28 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_alter_admodel_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='admodel',
            name='active',
            field=models.BooleanField(default=False, unique=True),
        ),
        migrations.AddField(
            model_name='admodel',
            name='link',
            field=models.URLField(blank=True, null=True),
        ),
    ]