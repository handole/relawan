from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from .models import Korcam, Relawan, Targetcapem
from dapil.models import Kecamatan, Kelurahan, Kabupaten


class KorcamForm(forms.ModelForm):
	nik = forms.CharField(max_length=100, label='NIK')

	class Meta:
		model = Korcam
		fields = ('nama', 'nik', 'gender', 'mobile', 'wilayah')

	def clean_nik(self):
		nik_baru = self.cleaned_data.get('nik')
		try:
			nik_lama = Korcam.objects.get(nik=self.cleaned_data.get('nik'))
		except Korcam.DoesNotExist:
			return nik_baru

		if nik_baru :
			if not self.instance.id:
				raise forms.ValidationError(_('NIK yang anda masukan sudah didata'))
		return nik_baru


class RelawanForm(forms.ModelForm):
	nik = forms.CharField(max_length=100, label='NIK')

	class Meta:
		model = Relawan
		fields = ('nama', 'nik', 'gender', 'mobile', 'target', 
			'status_relawan', 'jabatan', 'target_kelurahan')

	def clean_nik(self):
		nik_baru = self.cleaned_data.get('nik')
		try:
			nik_lama = Relawan.objects.get(nik=self.cleaned_data.get('nik'))
		except Relawan.DoesNotExist:
			return nik_baru

		if nik_baru :
			if not self.instance.id:
				raise forms.ValidationError(_('NIK yang anda masukan sudah didata'))
		return nik_baru



class TargetForm(forms.ModelForm):
	nik = forms.CharField(max_length=100, label='NIK')

	class Meta:
		model = Targetcapem
		fields = ('nama', 'nik', 'gender', 'mobile', 
			'wilayah', 'rtrw')

	def clean_nik(self):
		nik_baru = self.cleaned_data.get('nik')
	
		try:
			nik_lama = Targetcapem.objects.get(nik=self.cleaned_data.get('nik'))
		except Targetcapem.DoesNotExist:
			return nik_baru

		if nik_baru :
			# get name relawan inputer if target was unable in db
			if not self.instance.id:
				raise forms.ValidationError(_('NIK yang anda masukan sudah didata oleh {}'.format(nik_lama.relawan)))
		return nik_baru

