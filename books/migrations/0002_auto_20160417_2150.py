# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-18 02:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='award',
            name='award_name',
            field=models.CharField(default='winner', max_length=300),
        ),
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='books.Author'),
        ),
        migrations.AlterField(
            model_name='book',
            name='have_read',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='book',
            name='pub_year',
            field=models.DateField(blank=True, null=True, verbose_name='year published'),
        ),
        migrations.AlterField(
            model_name='book',
            name='status',
            field=models.SmallIntegerField(choices=[(0, 'not reading'), (1, 'reading'), (2, 'dormant')], default=0),
        ),
        migrations.AlterField(
            model_name='reading',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='end date'),
        ),
        migrations.AlterField(
            model_name='reading',
            name='focus',
            field=models.SmallIntegerField(choices=[(0, 'low'), (1, 'medium'), (2, 'high')], default=1),
        ),
        migrations.AlterField(
            model_name='reading',
            name='format',
            field=models.SmallIntegerField(choices=[(0, 'paper'), (1, 'ebook'), (2, 'audiobook')], default=2),
        ),
        migrations.AlterField(
            model_name='reading',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reading',
            name='start_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='start date'),
        ),
        migrations.AlterField(
            model_name='reading',
            name='user_rating',
            field=models.IntegerField(blank=True, default=-1, null=True),
        ),
    ]
