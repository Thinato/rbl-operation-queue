# Generated by Django 4.1.3 on 2022-12-20 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_remove_pedidopeca_quantidade_feita_filaoperacao'),
    ]

    operations = [
        migrations.AddField(
            model_name='filaoperacao',
            name='peso',
            field=models.IntegerField(default=0, verbose_name='Peso'),
            preserve_default=False,
        ),
    ]