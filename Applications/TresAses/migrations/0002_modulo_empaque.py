# Generated by Django 3.0.6 on 2023-09-18 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TresAses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Modulo_Empaque',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': [('Permitir', 'Ingreso')],
            },
        ),
    ]