# Generated by Django 3.2.12 on 2022-11-16 05:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Items',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=16, unique=True, verbose_name='项目名')),
            ],
            options={
                'verbose_name': '项目',
            },
        ),
        migrations.CreateModel(
            name='ItemPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan_name', models.CharField(max_length=16, unique=True, verbose_name='计划名')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='item.items')),
            ],
            options={
                'verbose_name': '项目计划',
            },
        ),
    ]
