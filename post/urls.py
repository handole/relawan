from django.conf.urls import url
from .views import *

urlpatterns =[
	url(r'^korcam/add/$', create_korcam, name='add-korcam'),
	url(r'^korcam/$', list_korcam, name='list-korcam'),
	url(r'^korcam/(?P<pk>\d+)/$', detail_korcam, name='detail-korcam'),
	url(r'^korcam/(?P<pk>\d+)/edit/$', edit_korcam, name='edit-korcam'),
	url(r'^korcam/(?P<pk>\d+)/delete/$', delete_korcam, name='delete-korcam'),		
	url(r'^korcam/(?P<pk>\d+)/asisten/add/$', create_relawan, name='add-asisten'),
	# url(r'^korcam/(?P<pk>\d+)/asisten/(?P<id>\d+)/edit/$', edit_relawan, name='edit-asisten'),
	# url(r'^korcam/(?P<pk>\d+)/asisten/(?P<id>\d+)/delete/$', delete_relawan, name='delete-asisten'),

	# url(r'^relawan/add/$', create_relawan, name='add-relawan'),
	url(r'^relawan/$', list_relawan, name='list-relawan'),
	url(r'^relawan/(?P<pk>\d+)/$', detail_relawan, name='detail-relawan'),
	url(r'^relawan/(?P<pk>\d+)/target/add/$', create_capem, name='add-target'),
	url(r'^relawan/(?P<id>\d+)/edit/$', edit_relawan, name='edit-asisten'),
	url(r'^relawan/(?P<id>\d+)/delete/$', delete_relawan, name='delete-asisten'),
	url(r'^relawan/export/$', export_relawan_csv, name='export-relawan'),

	# url(r'^target/add/$', create_capem, name='add-capem'),
	url(r'^target/$', list_capem, name='list-capem'),
	# url(r'^target/(?P<id>\d+)/$', detail_capem, name='detail-capem'),
	url(r'^target/(?P<id>\d+)/edit/$', edit_capem, name='edit-target'),
	url(r'^target/(?P<id>\d+)/delete/$', delete_capem, name='delete-target'),
	url(r'^target/export/$', export_capem, name='export-target'),
]