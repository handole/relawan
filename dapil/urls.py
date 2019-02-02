from django.conf.urls import url
from .views import *

urlpatterns =[
	url(r'^kelurahan/$', list_kelurahan, name='kelurahan'),
	url(r'^tps/$', TPSView.as_view(), name='tps-list'),
	url(r'^tps/add/$', TPSCreate.as_view(), name='tps-add'),
	# url(r'^add-tps/$', tps_add, name='tps-add'),
	url(r'^rtrw/$', RTRWview.as_view(), name='rtrw'),
	url(r'^rtrw/create/$', RTRWcreate.as_view(), name='rtrw-create'),
	url(r'^rtrw/(?P<pk>\d+)/edit/$', edit_rtrw, name='rtrw-edit'),
	url(r'^rtrw/(?P<pk>\d+)/delete/$', delete_rtrw, name='rtrw-delete'),

	url(r'^', dapil, name='dapil'),
	url(r'^ajax/load-kelurahan/', load_kelurahan, name='ajax_load_kelurahan'),
]