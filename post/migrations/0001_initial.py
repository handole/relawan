# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-11-10 03:17
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dapil', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Korcam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=100)),
                ('nik', models.CharField(blank=True, max_length=100)),
                ('gender', models.CharField(choices=[('Laki-laki', 'Laki-laki'), ('Perempuan', 'Perempuan')], max_length=20)),
                ('mobile', models.CharField(max_length=15)),
                ('status_relawan', models.CharField(choices=[('struktural', 'Struktural'), ('non_struktural', 'Non Struktural')], max_length=20)),
                ('create_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('wilayah', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='korcam', to='dapil.Kecamatan')),
            ],
        ),
        migrations.CreateModel(
            name='Relawan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=100)),
                ('nik', models.CharField(blank=True, max_length=100)),
                ('gender', models.CharField(choices=[('Laki-laki', 'Laki-laki'), ('Perempuan', 'Perempuan')], max_length=20)),
                ('mobile', models.CharField(max_length=15)),
                ('target', models.IntegerField()),
                ('count_target', models.PositiveIntegerField(default=0, null=True)),
                ('sisa_target', models.IntegerField(default=0, null=True)),
                ('status_relawan', models.CharField(choices=[('struktural', 'Struktural'), ('non_struktural', 'Non Struktural')], max_length=20)),
                ('jabatan', models.CharField(blank=True, choices=[('korcam', 'KORCAM'), ('asisten_kordes', 'ASISTEN KORDES'), ('asisten_korRTRW', 'ASISTEN KOR RT/RW')], max_length=100)),
                ('created', models.DateTimeField(auto_now=True)),
                ('create_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_relawan', to=settings.AUTH_USER_MODEL)),
                ('korcam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='korcamnya', to='post.Korcam')),
                ('target_kelurahan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='kelurahan_asisten', to='dapil.Kelurahan')),
                ('target_rtrw', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='wilayah_asisten', to='dapil.RTRW')),
            ],
        ),
        migrations.CreateModel(
            name='Targetcapem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=100)),
                ('nik', models.CharField(blank=True, max_length=100)),
                ('gender', models.CharField(choices=[('Laki-laki', 'Laki-laki'), ('Perempuan', 'Perempuan')], max_length=20)),
                ('mobile', models.CharField(max_length=15)),
                ('created', models.DateTimeField(auto_now=True)),
                ('create_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('relawan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_relawan', to='post.Relawan')),
                ('rtrw', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dapil.RTRW')),
                ('wilayah', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dapil.Kelurahan')),
            ],
        ),
    ]
