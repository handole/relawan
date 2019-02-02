# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-11-10 03:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Kabupaten',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jenis', models.CharField(choices=[(1, 'kota'), (2, 'kabupaten')], max_length=20)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Kecamatan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('kabupaten', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dapil.Kabupaten')),
            ],
        ),
        migrations.CreateModel(
            name='Kelurahan',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jenis', models.CharField(choices=[(3, 'kelurahan'), (4, 'desa')], max_length=20)),
                ('name', models.CharField(max_length=50)),
                ('jumlah_tps', models.PositiveIntegerField(default=0, null=True)),
                ('kecamatan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dapil.Kecamatan')),
            ],
        ),
        migrations.CreateModel(
            name='Provinsi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='RTRW',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rt', models.CharField(max_length=30)),
                ('rw', models.CharField(max_length=30)),
                ('jum_rt', models.PositiveIntegerField(default=0, null=True)),
                ('jum_rw', models.PositiveIntegerField(default=0, null=True)),
                ('kelurahan', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dapil.Kelurahan')),
            ],
        ),
        migrations.CreateModel(
            name='TPS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('kecamatan', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dapil.Kecamatan')),
                ('kelurahan', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dapil.Kelurahan')),
            ],
        ),
        migrations.AddField(
            model_name='kabupaten',
            name='provinsi',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dapil.Provinsi'),
        ),
    ]