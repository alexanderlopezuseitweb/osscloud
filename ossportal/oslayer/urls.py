from django.conf.urls import url

from . import views

app_name = 'oslayer'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^project\/$', views.project_list, name='project_list'),
    url(r'^project\/add$', views.project_add, name='project_add'),
    url(r'^project\/(?P<project_id>[a-z0-9]+)\/$', views.project_detail, name='project_detail'),
    url(r'^user\/$', views.user_list, name='user_list'),
    url(r'^user\/add$', views.user_add, name='user_add'),
    url(r'^user\/(?P<user_id>[a-z0-9]+)\/$', views.user_detail, name='user_detail'),
    url(r'^domain\/$', views.domain_list, name='domain_list'),
    url(r'^domain\/add$', views.domain_add, name='domain_add'),
    url(r'^domain\/(?P<domain_id>[a-z0-9]+)\/$', views.domain_detail, name='domain_detail'),
    url(r'^company\/$', views.CompanyListView.as_view()),
    url(r'^company\/add$', views.company_add, name='company_add'),
    url(r'^company\/(?P<pk>[a-z0-9]+)\/$', views.CompanyDetailView.as_view(), name='company_detail'),
#     url(r'^company\/(?P<pk>[0-9]+)\/$', views.CompanyUpdate.as_view(), name='company-update'),
#     url(r'^company\/(?P<pk>[0-9]+)\/delete$', views.CompanyDelete.as_view(), name='company-delete'),
]