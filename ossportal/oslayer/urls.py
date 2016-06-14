from django.conf.urls import url

from . import views

app_name = 'oslayer'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^tenants\/$', views.tenants, name='tenants'),
    url(r'^tenants\/(?P<tenant_id>[a-z0-9]+)\/$', views.tenant_detail, name='tenant_detail'),
]