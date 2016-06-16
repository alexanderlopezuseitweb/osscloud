from django.conf.urls import url

from . import views

app_name = 'oslayer'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^projects\/$', views.projects, name='projects'),
    url(r'^projects\/(?P<project_id>[a-z0-9]+)\/$', views.project_detail, name='project_detail'),
    url(r'^users\/$', views.users, name='users'),
    url(r'^users\/(?P<user_id>[a-z0-9]+)\/$', views.user_detail, name='user_detail'),
    url(r'^users\/create$', views.create_user, name='create_user'),
    url(r'^domains\/$', views.domains, name='domains'),
    url(r'^domains\/(?P<domain_id>[a-z0-9]+)\/$', views.domain_detail, name='domain_detail'),
    url(r'^companies\/$', views.CompanyListView.as_view()),
    url(r'^companies\/(?P<pk>[a-z0-9]+)\/$', views.CompanyDetailView.as_view(), name='company_detail'),
    url(r'^company\/add\/$', views.CompanyCreate.as_view(), name='company-add'),
    url(r'^company\/(?P<pk>[0-9]+)\/$', views.CompanyUpdate.as_view(), name='company-update'),
    url(r'^company\/(?P<pk>[0-9]+)\/delete\/$', views.CompanyDelete.as_view(), name='company-delete'),
]