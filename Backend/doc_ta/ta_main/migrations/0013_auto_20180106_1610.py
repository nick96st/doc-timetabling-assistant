# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-06 16:10
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ta_main', '0012_merge_20171129_1536'),
    ]

    operations = [
        migrations.CreateModel(
            name='SlotBlocker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.IntegerField()),
                ('end', models.IntegerField()),
                ('day', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ta_main.DayDef')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ta_main.Subject')),
            ],
        ),
        migrations.AlterField(
            model_name='tablesizedef',
            name='title',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
