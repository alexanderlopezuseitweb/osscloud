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
    #Added by Alexander Lopez
    url(r'^group\/$', views.GroupListView.as_view(), name='group_list'),
    url(r'^group\/add$', views.group_add, name='group_add'),
    url(r'^group\/(?P<group_id>[0-9]+)\/$', views.group_edit, name='group_edit'),
    url(r'^state\/delete_group\/(?P<pk>[0-9]+)\/$', views.GroupDelete.as_view(), name='group_delete'),
    url(r'^country\/$', views.CountryListView.as_view(), name='country_list'),
    url(r'^country\/add$', views.country_add, name='country_add'),
    url(r'^country\/(?P<country_id>[0-9]+)\/$', views.country_edit, name='country_edit'),
    url(r'^state\/delete_country\/(?P<pk>[0-9]+)\/$', views.CountryDelete.as_view(), name='country_delete'),
    url(r'^state\/$', views.StateListView.as_view(), name='state_list'),
    url(r'^state\/add$', views.state_add, name='state_add'),
    url(r'^state\/(?P<state_id>[0-9]+)\/$', views.state_edit, name='state_edit'),
    url(r'^state\/delete_state\/(?P<pk>[0-9]+)\/$', views.StateDelete.as_view(), name='state_delete'),
    url(r'^city\/$', views.CityListView.as_view(), name='city_list'),
    url(r'^city\/add$', views.city_add, name='city_add'),
    url(r'^city\/(?P<city_id>[0-9]+)\/$', views.city_edit, name='city_edit'),
    url(r'^state\/delete_city\/(?P<pk>[0-9]+)\/$', views.CityDelete.as_view(), name='city_delete'),

]