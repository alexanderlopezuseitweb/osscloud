from django.conf.urls import url

from . import views

app_name = 'oslayer'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^project\/$', views.project_list, name='project_list'),
    url(r'^project\/add$', views.project_add, name='project_add'),
    url(r'^project\/(?P<project_id>[a-z0-9]+)\/$', views.project_edit, name='project_edit'),
    url(r'^user\/$', views.user_list, name='user_list'),
    url(r'^user\/add$', views.user_add, name='user_add'),
    url(r'^user\/(?P<user_id>[0-9]+)\/$', views.user_edit, name='user_edit'),
    url(r'^domain\/$', views.domain_list, name='domain_list'),
    url(r'^domain\/add$', views.domain_add, name='domain_add'),
    url(r'^domain\/(?P<domain_id>[a-z0-9]+)\/$', views.domain_detail, name='domain_detail'),
    url(r'^company\/$', views.CompanyListView.as_view(), name='company_list'),
    url(r'^company\/add$', views.company_add, name='company_add'),
    url(r'^company\/(?P<company_id>[0-9]+)\/$', views.company_edit, name='company_edit'),
#    url(r'^company\/(?P<pk>[0-9]+)\/delete$', views.CompanyDelete.as_view(), name='company-delete'),
    url(r'^forums\/$', views.forums_space_list, name='forums_space_list'),
    url(r'^forums\/(?P<space_key>[a-zA-Z0-9]+)\/pages$', views.forums_space_list_pages, name='forums_space_list_pages'),
]