import csv
import xlwt
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Count
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from .models import Korcam, Relawan, Targetcapem
from .forms import KorcamForm, RelawanForm, TargetForm
from dapil.models import Kelurahan, Kecamatan

# Create your views here.
@login_required
def create_korcam(request):
	form = KorcamForm()
	if request.method == 'POST':
		form = KorcamForm(request.POST or None)
		if form.is_valid():
			korcam = form.save(commit=False)
			korcam.create_by = request.user
			korcam.save()
			return redirect('post:list-korcam')

	return render(request, 'post/createkorcam.html', {'form':form})

@login_required
def list_korcam(request):
	korcam = Korcam.objects.all()
	page = request.GET.get('page', 1)
	query = request.GET.get('q')

	if query:
		korcam = korcam.filter(
			Q(nama__icontains=query) |
			Q(nik__icontains=query) |
			Q(status_korcam__icontains=query) |
			Q(wilayah__icontains=query) |
			Q(create_by__username__icontains=query)
			)

	paginator = Paginator(korcam, 10)
	try:
		koor = paginator.page(page)
	except PageNotAnInteger:
		koor = paginator.page(1)
	except EmptyPage:
		koor = paginator.page(paginator.num_pages)

	context = {
		'korcam':korcam,
		'koor':koor,
		'query':query,
	}

	return render(request, 'post/listkorcam.html', context)
			

@login_required
def detail_korcam(request, pk):
	korcam = get_object_or_404(Korcam, pk=pk)

	try:
		rela = Relawan.objects.filter(korcam=korcam)
	except rela.DoesNotExist:
		rela = None

	context = {
		'korcam':korcam,
		'rela':rela,
	}

	return render(request, 'post/detailkorcam.html', context)

@login_required
def export_korcam_csv(request):
	response = HttpResponse(content_type='text/csv')
	response['Conten-Dispositioin'] = 'attachment; filename="list-korcam.csv"'

	writer = csv.writer(response)
	writer.writerow(['nama', 'nik', 'mobile', 'wilayah'])

	korcam = Korcam.objects.all().values_list('nama', 'nik', 'mobile', 'wilayah')
	for rela in korcam:
		writer.writerow(rela)

	return response

@login_required
def edit_korcam(request, pk):
	korcam = get_object_or_404(Korcam, pk=pk)
	form = KorcamForm(request.POST or None, instance=korcam)
	if form.is_valid():
		korcam = form.save(commit=False)
		korcam.create_by = request.user
		korcam.save()
		return redirect('post:list-korcam')

	context = {
		'korcam':korcam,
		'form':form,
	}
	return render(request, 'post/editkorcam.html', context)

@login_required
def delete_korcam(request, pk=None):
	korcam = get_object_or_404(Korcam, pk=pk)
	korcam.delete()
	return redirect('post:list-korcam')

@login_required
def create_relawan(request, pk):
	kordi = get_object_or_404(Korcam, pk=pk)
	form = RelawanForm()
	if request.method == 'POST':
		form = RelawanForm(request.POST or None)
		if form.is_valid():
			relawan = form.save(commit=False)
			relawan.korcam = kordi
			kordi.relawan = kordi.wilayah
			relawan.create_by = request.user
			relawan.save()
			return HttpResponseRedirect(reverse('post:detail-korcam', args=[kordi.pk]))

	context = {
		'form':form,
		'kordi':kordi
	}
	return render(request, 'post/createrelawan.html', context)

def load_kelurahan(request):
	kecamatan_id = request.GET.get('kecamatan')
	kelurahan = Kelurahan.objects.filter(kecamatan_id=kecamatan_id).order_by('name')
	return render(request, 'dapil/kelurahan_dropdown_list_options.html', {'kelurahan':kelurahan})

@login_required
def list_relawan(request):
	relawan = Relawan.objects.all()
	page = request.GET.get('page', 1)
	query = request.GET.get('q')

	if query:
		relawan = relawan.filter(
			Q(nama__icontains=query) |
			Q(nik__icontains=query) |
			Q(status_relawan__icontains=query) |
			Q(jabatan__icontains=query) |
			Q(create_by__username__icontains=query)
			)

	paginator = Paginator(relawan, 10)
	try:
		rela = paginator.page(page)
	except PageNotAnInteger:
		rela = paginator.page(1)
	except EmptyPage:
		rela = paginator.page(paginator.num_pages)

	context = {
		'relawan':relawan,
		'rela':rela,
		'query':query,
	}

	return render(request, 'post/listrelawan.html', context)


@login_required
def detail_relawan(request, pk):
	relawan = get_object_or_404(Relawan, pk=pk)

	try:
		target = Targetcapem.objects.filter(relawan_id=relawan.pk)
	except target.DoesNotExist:
		target = None

	context = {
		'relawan':relawan,
		'target':target,
	}

	return render(request, 'post/detailrelawan.html', context)

@login_required
def export_relawan_csv(request):
	response = HttpResponse(content_type='text/csv')
	response['Conten-Dispositioin'] = 'attachment; filename="list-relawan.csv"'

	writer = csv.writer(response)
	writer.writerow(['nama', 'nik', 'mobile', 'target', 'status_relawan', 'jabatan', 'create_by'])

	relawan = Relawan.objects.all().values_list('nama', 'nik', 'mobile', 'target', 'status_relawan', 'jabatan', 'create_by')
	for rela in relawan:
		writer.writerow(rela)

	return response

@login_required
def edit_relawan(request,id):
	# kordi = get_object_or_404(Korcam, pk=pk)
	relawan = get_object_or_404(Relawan, id=id)
	form = RelawanForm(request.POST or None, instance=relawan)
	if form.is_valid():
		instance = form.save(commit=False) 
		instance.create_by = request.user
		instance.save()
		return HttpResponseRedirect(reverse('post:list-relawan'))

	context = {
		'relawan':relawan,
		'form':form,
	}
	return render(request, 'post/editrelawan.html', context)

@login_required
def delete_relawan(request, id=None):
	relawan = get_object_or_404(Relawan, id=id)
	relawan.delete()
	return HttpResponseRedirect(reverse('post:list-relawan'))

@login_required
def create_capem(request, pk):
	rel = get_object_or_404(Relawan, pk=pk)
	# nik_target = Targetcapem.objects.all()
	# nik_qs = request.GET.get('q')

	form = TargetForm()
	if request.method == 'POST':
		form = TargetForm(request.POST or None)
		if form.is_valid():
			capem = form.save(commit=False)
			capem.relawan = rel
			capem.create_by = request.user
			capem.save()
			return HttpResponseRedirect(reverse('post:detail-relawan', args=[rel.pk]))

	context = {
		'form':form,
		'rel':rel,
	}
	return render(request, 'post/createcapim.html', context)

@login_required
def list_capem(request):
	capem = Targetcapem.objects.all()
	page = request.GET.get('page', 1)
	query = request.GET.get('q')
	if query:
		capem = capem.filter(
			Q(nama__icontains=query) |
			Q(nik__icontains=query) |
			Q(gender__icontains=query) |
			Q(tps__icontains=query) |
			Q(relawan__nama__icontains=query)
			)
	paginator = Paginator(capem, 10)
	try:
		target = paginator.page(page)
	except PageNotAnInteger:
		target = paginator.page(1)
	except EmptyPage:
		target = paginator.page(paginator.num_pages)

	context = {
		'capem':capem,
		'target':target,
		'query':query,
	}
	return render(request, 'post/listcapim.html', context)

@login_required
def detail_capem(request, pk):
	capem = get_object_or_404(Targetcapem, pk=pk)

	context = {
		'capem':capem,
	}
	return render(request, 'post/detailcapim.html', context)

@login_required
def export_target_csv(request):
	response = HttpResponse(content_type='text/csv')
	response['Conten-Dispositioin'] = 'attachment; filename="list-capem.csv"'

	writer = csv.writer(response)
	writer.writerow(['nama', 'nik', 'gender', 'mobile', 'tps', 'wilayah', 'create_by'])

	target = Targetcapem.objects.all().values_list('nama', 'nik', 'gender', 'mobile', 'tps', 'wilayah', 'create_by')
	for capem in target:
		writer.writerow(capem)

	return response

@login_required
def edit_capem(request,id):
	# relawan = get_object_or_404(Relawan, pk=pk)
	capem = get_object_or_404(Targetcapem, id=id)
	form = TargetForm(request.POST or None, instance=capem)
	if form.is_valid():
		instance = form.save(commit=False)
		# instance.relawan = relawan
		instance.create_by = request.user
		instance.save()

		return HttpResponseRedirect(reverse('post:list-capem'))

	context = {
		'capem':capem,
		'form':form,
	}
	return render(request, 'post/editcapim.html', context)

@login_required
def delete_capem(request, id=None):
	capem = get_object_or_404(Targetcapem, id=id)
	capem.delete()
	return HttpResponseRedirect(reverse('post:list-capem'))

def export_capem(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="export-capem.xlsx"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users')

    # sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Nama', 'NIK', 'Jenis Kelamin', 'No HP', 'Wilayah', 'RTRW', 'By Relawan']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Targetcapem.objects.all().values_list('nama', 'nik', 'gender', 'mobile', 'wilayah', 'rtrw', 'relawan')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response