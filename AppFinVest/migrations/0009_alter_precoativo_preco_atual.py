# Generated by Django 5.1.4 on 2025-01-08 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppFinVest', '0008_precoativo_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='precoativo',
            name='preco_atual',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
    ]
