# Generated by Django 4.1.3 on 2022-12-21 12:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_filaoperacao_peso'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='filaoperacao',
            name='quantidade',
        ),
    ]
