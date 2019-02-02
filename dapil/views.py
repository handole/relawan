from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required
from .models import Kelurahan, Kecamatan, Kabupaten, TPS, RTRW
from .forms import TPSForm, RTRWForm
from post.models import Korcam, Relawan, Targetcapem

# Create your views here

class TPSView(ListView):
	model = TPS
	context_object_name = 'name_tps'

class TPSCreate(CreateView):
	model = TPS
	form_class = TPSForm
	success_url = reverse_lazy('dapil:kelurahan')


def load_kelurahan(request):
	kecamatan_id = request.GET.get('kecamatan')
	kelurahan = Kelurahan.objects.filter(kecamatan_id=kecamatan_id).order_by('name')
	return render(request, 'dapil/kelurahan_dropdown_list_options.html', {'kelurahan':kelurahan})


class RTRWview(ListView):
	model = RTRW
	context_object_name = 'name_rtrw'

class RTRWcreate(CreateView):
	model = RTRW
	form_class = RTRWForm
	success_url = reverse_lazy('dapil:rtrw')


@login_required
def edit_rtrw(request, pk):
	rtrw = get_object_or_404(RTRW, pk=pk)
	form = RTRWForm(request.POST or None, instance=rtrw)
	if form.is_valid():
		rtrw = form.save(commit=False)
		rtrw.save()
		return redirect('dapil:rtrw')

	context = {
		'rtrw':rtrw,
		'form':form,
	}
	return render(request, 'dapil/editrtrw.html', context)

@login_required
def delete_rtrw(request, pk=None):
	rtrw = get_object_or_404(RTRW, pk=pk)
	rtrw.delete()
	return redirect('dapil:rtrw')


@login_required
def dapil(request):
	hit_camat = Kabupaten.objects.all()
	hit_relawan = Kecamatan.objects.all()

	page = request.GET.get('page', 1)
	query = request.GET.get('q')
	if query:
		hit_relawan = hit_relawan.filter(
			Q(kabupaten__name__icontains=query) |
			Q(name__icontains=query) 
			)

	paginator = Paginator(hit_relawan, 10)
	try:
		camat = paginator.page(page)
	except PageNotAnInteger:
		camat = paginator.page(1)
	except EmptyPage:
		camat = paginator.page(paginator.num_pages)

	context = {
		'hit_camat':hit_camat,
		'hit_relawan':hit_relawan,
		'query':query,
		'paginator':paginator
	}
	return render(request, 'dapil/dapil.html', context)


def search_relawan(request, *args, **kwargs):
	data = dict()
	data['target_kelurahan'] = Relawan.objects.get(id=request['id']).target_kelurahan
	return JsonResponse(data)



@login_required
def list_kelurahan(request):
	kelurahan = Kelurahan.objects.all()
	page = request.GET.get('page', 1)
	query = request.GET.get('q')
	if query:
		kelurahan = kelurahan.filter(
			Q(id__icontains=query) |
			Q(kecamatan__kabupaten__name__icontains=query) |
			Q(kecamatan__name__icontains=query) |
			Q(name__icontains=query) |
			Q(jenis__icontains=query)
			)

	paginator = Paginator(kelurahan, 30)
	try:
		lurah = paginator.page(page)
	except PageNotAnInteger:
		lurah = paginator.page(1)
	except EmptyPage:
		lurah = paginator.page(paginator.num_pages)

	context = {
		'kelurahan':kelurahan,
		'lurah':lurah,
		'query':query,
	}

	return render(request, 'dapil/kelurahan.html', context)
