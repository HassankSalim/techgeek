# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-05 15:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Options',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qns', models.TextField()),
                ('ansId', models.IntegerField()),
                ('day', models.IntegerField()),
                ('selected_ans', models.CharField(default='select', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('user_id', models.CharField(max_length=200)),
                ('image_url', models.URLField()),
                ('score', models.IntegerField()),
                ('totalTime', models.IntegerField()),
                ('today_score', models.IntegerField()),
                ('start_time', models.IntegerField()),
                ('next_answered_qn', models.IntegerField()),
                ('today_total_time', models.IntegerField()),
            ],
            options={
                'ordering': ('score', 'totalTime'),
            },
        ),
        migrations.AddField(
            model_name='options',
            name='qn',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='techgeek.Questions'),
        ),
    ]
