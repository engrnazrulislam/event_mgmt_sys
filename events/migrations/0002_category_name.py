# Generated by Django 5.2.4 on 2025-07-04 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='name',
            field=models.CharField(default='General', max_length=200),
        ),
    ]
