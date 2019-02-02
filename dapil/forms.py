from django import forms
from .models import TPS, Kelurahan, RTRW

class TPSForm(forms.ModelForm):
	class Meta:
		model = TPS
		fields = ('kecamatan', 'kelurahan', 'name')

	def __init__(self, *args, **kwargs):
		super(TPSForm, self).__init__(*args, **kwargs)
		self.fields['kelurahan'].queryset = Kelurahan.objects.none()

		if 'kecamatan' in self.data:
			try:
				kecamatan_id = int(self.data.get('kecamatan'))
				self.fields['kelurahan'].queryset = Kelurahan.objects.filter(kecamatan_id=kecamatan_id).order_by('name')
			except (ValueError, TypeError):
				pass
		elif self.instance.pk:
			self.fields['kelurahan'].queryset = self.instance.kelurahan_set.order_by('name')


class RTRWForm(forms.ModelForm):
	rt = forms.CharField(max_length=10, label="RT")
	rw = forms.CharField(max_length=10, label="RW")

	class Meta:
		model = RTRW
		fields = ('kelurahan', 'rt', 'rw')

