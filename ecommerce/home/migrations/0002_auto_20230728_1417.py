# Generated by Django 3.2.19 on 2023-07-28 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='amodel',
            options={'verbose_name': 'bigger ad'},
        ),
        migrations.AlterModelOptions(
            name='bmodel',
            options={'verbose_name': 'middle ad'},
        ),
        migrations.AddField(
            model_name='admodel',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]