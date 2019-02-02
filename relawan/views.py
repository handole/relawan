from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from dapil.models import Kelurahan, Kecamatan, Kabupaten
from post.models import Targetcapem, Relawan, Korcam
from dapil.forms import TPSForm
from dapil.serializers import KabupatenSerializer, KecamatanSerializer, KelurahanSerializer
from post.forms import RelawanForm
from post.serializers import KorcamSerializer, RelawanSerializer, UserSerializer

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

User = get_user_model()

def load_kelurahan(request):
	kecamatan_id = request.GET.get('kecamatan')
	kelurahan = Kelurahan.objects.filter(kecamatan_id=kecamatan_id).order_by('name')
	return render(request, 'dapil/kelurahan_dropdown_list_options.html', {'kelurahan':kelurahan})

def index(request):
	relawan = Relawan.objects.all()
	return render(request, 'index.html', {'relawan':relawan})	


class UserDeactivated(APIView):
    
    def post(self, request, format=None):

        user = request.user
        if user.is_anonymous==False:
            user.is_active = False
            user.is_superuser = False
            user.is_staff = False
            user.save()
            msg = _('User was deactivated')
            #todo send email
            return Response({'msg': msg}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(status=status.HTTP_200_OK)


def get_data(request, *args, **kwargs):
	data = {
		"sales": 100,
		"customer": 10,
	}
	return JsonResponse(data)

class ListKorcam(generics.ListCreateAPIView):
	queryset = Korcam.objects.all()
	serializer_class = KorcamSerializer

class DetailKorcam(generics.RetrieveUpdateDestroyAPIView):
	queryset = Korcam.objects.all()
	serializer_class = KorcamSerializer

class ListRelawan(generics.ListCreateAPIView):
	queryset = Relawan.objects.all()
	serializer_class = RelawanSerializer

class DetailRelawan(generics.RetrieveUpdateDestroyAPIView):
	queryset = Relawan.objects.all()
	serializer_class = RelawanSerializer

class ListKabupaten(generics.ListAPIView):
	queryset = Kabupaten.objects.all()
	serializer_class = KabupatenSerializer

class DetailKabupaten(generics.RetrieveAPIView):
	queryset = Kabupaten.objects.all()
	serializer_class = KabupatenSerializer

class ListKecamatan(generics.ListAPIView):
	queryset = Kecamatan.objects.all()
	serializer_class = KecamatanSerializer

class DetailKecamatan(generics.RetrieveAPIView):
	queryset = Kecamatan.objects.all()
	serializer_class = KecamatanSerializer

class ListKelurahan(generics.ListAPIView):
	queryset = Kelurahan.objects.all()
	serializer_class = KelurahanSerializer

class DetailKelurahan(generics.RetrieveAPIView):
	queryset = Kelurahan.objects.all()
	serializer_class = KelurahanSerializer