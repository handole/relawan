# from datetime import datetime
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db.models import Q, Count, Func, F
from django.contrib.auth.models import User
from dapil.models import Kelurahan, RTRW, Kecamatan

# Create your models here.

STATUS_CHOICES = (
			('struktural', 'Struktural'),
			('non_struktural', 'Non Struktural'),
		)

GENDER_CHOICES = (
			('Laki-laki', 'Laki-laki'),
			('Perempuan', 'Perempuan'),
		)


class Korcam(models.Model):
	nama = models.CharField(max_length=100)
	nik = models.CharField(max_length=100, blank=True)
	gender = models.CharField(choices=GENDER_CHOICES, max_length=20)
	mobile = models.CharField(max_length=15)
	status_relawan = models.CharField(choices=STATUS_CHOICES, max_length=20)
	wilayah = models.ForeignKey(Kecamatan, related_name='korcam', blank=True)
	create_by = models.ForeignKey(User)
	
	def __str__(self):
		return self.nama

	def count_relawan(self):
		relawan = Relawan.objects.filter(korcam_id=self.id).count()
		return relawan

class Relawan(models.Model):

	JABATAN_CHOICES = (
			('korcam', 'KORCAM'),
			('asisten_kordes', 'ASISTEN KORDES'),
			('asisten_korRTRW', 'ASISTEN KOR RT/RW'),
		)

	nama = models.CharField(max_length=100)
	nik = models.CharField(max_length=100, blank=True)
	gender = models.CharField(choices=GENDER_CHOICES, max_length=20)
	mobile = models.CharField(max_length=15)
	target = models.IntegerField()
	count_target = models.PositiveIntegerField(null=True, default=0)
	sisa_target = models.IntegerField(null=True, default=0)
	status_relawan = models.CharField(choices=STATUS_CHOICES, max_length=20)
	jabatan = models.CharField(choices=JABATAN_CHOICES, max_length=100, blank=True)
	target_kelurahan = models.ForeignKey(Kelurahan, related_name='kelurahan_asisten', blank=True, null=True)
	target_rtrw = models.ForeignKey(RTRW, related_name='wilayah_asisten', blank=True, null=True)
	korcam = models.ForeignKey(Korcam, related_name='korcamnya')
	create_by = models.ForeignKey(User, related_name='user_relawan')
	created = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.nama

	def count_target(self):
		target = Targetcapem.objects.filter(relawan_id=self.id).count()
		return target

	def sisa_target(self, realisasi): 
		target = self.target
		realisasi = Targetcapem.objects.filter(relawan_id=self.id).count()
		sisa = int(target - realisasi)
		return sisa


class Targetcapem(models.Model):

	nama = models.CharField(max_length=100)
	nik = models.CharField(max_length=100, blank=True)
	gender = models.CharField(choices=GENDER_CHOICES, max_length=20)
	mobile = models.CharField(max_length=15)
	# tps = models.IntegerField()
	wilayah = models.ForeignKey(Kelurahan, blank=True, null=True)
	rtrw = models.ForeignKey(RTRW, blank=True, null=True)
	relawan = models.ForeignKey(Relawan, related_name='from_relawan')
	create_by = models.ForeignKey(User)
	created = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.nama

	def count_relawan(self, *args, **kwargs):
		c_relawan = Targetcapem.objects.filter(pk=self.relawan_id).annotate(Count(self.relawan))

	# def save(self, *args, **kwargs):
	# 	if not self.pk:
	# 		Relawan.objects.filter(pk=self.relawan_id).update(count_target=F('count_target')+1)
	# 	super().save(*args, **kwargs)


@receiver(pre_save, sender=Targetcapem, dispatch_uid="update_target_count")
def update_target_count(sender, **kwargs):
	c_target = kwargs['instance']
	if c_target.pk:
		Relawan.objects.filter(pk=c_target.relawan_id).update(count_target=F('count_target')+1)

