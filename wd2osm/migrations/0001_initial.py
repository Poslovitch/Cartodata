# Generated by Django 3.2.6 on 2021-08-11 21:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Catalog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=128)),
                ('description', models.TextField()),
                ('wd_p31', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Alignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wd_item', models.IntegerField()),
                ('catalog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wd2osm.catalog')),
            ],
        ),
    ]
