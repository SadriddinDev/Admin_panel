# Generated by Django 4.0.5 on 2022-06-22 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edu_app', '0002_bolimqoshish'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bolimqoshish',
            name='url_manzil',
            field=models.CharField(max_length=200),
        ),
    ]