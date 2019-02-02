from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db.models import F
# from post.models import Korcam

# Create your models here.

class Provinsi(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name

class Kabupaten(models.Model):
	KOTA = 1
	KABUPATEN = 2

	JENIS_CHOICES = (
			(KOTA, 'kota'),
			(KABUPATEN, 'kabupaten'),
		)

	provinsi = models.ForeignKey(Provinsi)
	jenis = models.CharField(choices=JENIS_CHOICES, max_length=20)
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name

	def get_kecamatan(self):
		camat = Kecamatan.objects.filter(kabupaten_id=self.id).count()
		return camat

	def count_korcam(self):
		from post.models import Korcam
		korcam = Korcam.objects.filter(wilayah_id__kabupaten_id=self.id).count()
		return korcam

class Kecamatan(models.Model):
	kabupaten = models.ForeignKey(Kabupaten)
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name

	def count_desa(self):
		desa = Kelurahan.objects.filter(kecamatan_id=self.id).count()
		return desa
	
	def count_asisten(self):
		from post.models import Relawan
		asisten = Relawan.objects.filter(target_kelurahan_id__kecamatan_id=self.id).count()
		return asisten

class Kelurahan(models.Model):
	KELURAHAN = 3
	DESA = 4

	JENIS_DESA = (
			(KELURAHAN, 'kelurahan'),
			(DESA, 'desa'),
		)

	id = models.BigIntegerField(primary_key=True, auto_created=True, verbose_name='ID')
	kecamatan = models.ForeignKey(Kecamatan, on_delete=models.CASCADE)
	jenis = models.CharField(choices=JENIS_DESA, max_length=20)
	name = models.CharField(max_length=50)
	jumlah_tps = models.PositiveIntegerField(null=True, default=0)

	def __str__(self):
		return self.name

	def count_desa(self):
		desa = Kelurahan.objects.filter(kecamatan_id=self.kecamatan.id).count()
		return desa

	def count_asisten(self):
		from post.models import Relawan
		asisten = Relawan.objects.filter(target_kelurahan_id=self.id).count()
		return asisten

	def save(self, *args, **kwargs):
		if not self.id:
			cursor = connection.cursor();
			cursor.execute("SELECT NEXTVAL('myapp_seq')")
			id = cursor.fetchone()
			sel.id = id[0]

		Model(Kelurahan, self).save(*args, **kwargs)

class TPS(models.Model):
	kecamatan = models.ForeignKey(Kecamatan, on_delete=models.SET_NULL, null=True)
	kelurahan = models.ForeignKey(Kelurahan, on_delete=models.SET_NULL, null=True)
	name = models.CharField(max_length=20)

	def __str__(self):
		return self.name

class RTRW(models.Model):
	kelurahan = models.ForeignKey(Kelurahan, on_delete=models.SET_NULL, null=True)
	rt = models.CharField(max_length=30)
	rw = models.CharField(max_length=30)
	jum_rt = models.PositiveIntegerField(null=True, default=0)
	jum_rw = models.PositiveIntegerField(null=True, default=0)

	def __str__(self):
		return self.rt

	def get_name(self):
		return "RT %s, RW %s" % (self.rt, self.rw)
