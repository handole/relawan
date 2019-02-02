from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from .views import *


urlpatterns = [
	url(r'^login/$', auth_views.login, name='login'),
	url(r'^logout/$', auth_views.logout, name='logout'),
	url(r'^admin/', admin.site.urls),

	url(r'', include('post.urls', namespace='post')),
	url(r'^$', index, name='home'),
	url(r'^dapil/', include('dapil.urls', namespace='dapil')),
	url(r'^api/data/$', get_data, name="getdata"),

	url(r'^api/user/(?P<pk>\d+)/$', UserDeactivated.as_view()),
	url(r'^api/korcam/$', ListKorcam.as_view()),
	url(r'^api/korcam/(?P<pk>\d+)/$', DetailKorcam.as_view()),
	url(r'^api/relawan/$', ListRelawan.as_view()),
	url(r'^api/relawan/(?P<pk>\d+)/$', DetailRelawan.as_view()),
	url(r'^api/kabupaten/$', ListKabupaten.as_view()),
	url(r'^api/kabupaten/(?P<pk>\d+)/$', DetailKabupaten.as_view()),
	url(r'^api/kecamatan/$', ListKecamatan.as_view()),
	url(r'^api/kecamatan/(?P<pk>\d+)/$', DetailKecamatan.as_view()),
	url(r'^api/kelurahan/$', ListKelurahan.as_view()),
	url(r'^api/kelurahan/(?P<pk>\d+)/$', DetailKelurahan.as_view()),
]
