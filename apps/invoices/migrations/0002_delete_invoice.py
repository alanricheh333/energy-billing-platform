# Generated by Django 5.1.1 on 2024-09-22 21:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Invoice',
        ),
    ]