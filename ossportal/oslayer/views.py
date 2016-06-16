from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView,\
    FormView

from .models import Company
from forms import AddCompanyForm
from openstack import api
# Create your views here.

def __get_keystone_client__(request):
    """Checks the django session for connection settings, if they are not found 
    they are loaded from the database and stored in session. 
    A new keystone client is instanced.
    
    Args:
        request: Django request containing session
    Returns:
        Keystone client
    """
    
    kcf = api.KeystoneClientFactory()
    if api.SESSION_KEYWORD not in request.session:
        connection_settings = kcf.load_settings()
        request.session[api.SESSION_KEYWORD] = connection_settings
    else:
        connection_settings = request.session[api.SESSION_KEYWORD]
    kc = kcf.create_client(connection_settings)
    return kc        
    
def index(request):
    return HttpResponse("Hello, world. You're at the oslayer index.")

def projects(request):
    """Lists current projects available in OpenSTack.
    
    Args:
        request: Django request containing session
    Returns:
        HttpResponse 
    """
    
    try:
        kc = __get_keystone_client__(request)
    except Exception as ex:
        return HttpResponse("Error: " + ex.message)
    else:
        print("username:", request.session[api.SESSION_KEYWORD]['username'])
        print("regions:",kc.regions.list())
        #kc.projects.create(name='useit_project', domain='e0c9b559b31a41ceae4548ce04ef7789', description='Default project for useit domain', enabled=True, parent=None)
        return render(request, 'oslayer/projects.html', {'projects_list': kc.projects.list()})
        
def project_detail(request, project_id):
    """Shows details for a given project id.
    
    Args:
        request: Django request containing session.
        project_id (str): 32 characters ID for a give project.
    Returns:
        HttpResponse
    """    
    
    try:
        kc = __get_keystone_client__(request)
    except Exception as ex:
        return HttpResponse("Error: " + ex.message)
    else:
        return render(request, 'oslayer/project_detail.html', {'project': kc.projects.get(project_id)})

def users(request):
    """Lists current users available in OpenSTack.
    
    Args:
        request: Django request containing session
    Returns:
        HttpResponse 
    """
    
    try:
        kc = __get_keystone_client__(request)
    except Exception as ex:
        return HttpResponse("Error: " + ex.message)
    else:
        context = {
                   'users_list': kc.users.list(), 
                   'domains_list': kc.domains.list(), 
                   'projects_list': kc.projects.list()}
        return render(request, 'oslayer/users.html', context)
        
def user_detail(request, user_id):
    """Shows details for a given user id.
    
    Args:
        request: Django request containing session.
        user_id (str): 32 characters ID for a give user.
    Returns:
        HttpResponse
    """    
    
    try:
        kc = __get_keystone_client__(request)
    except Exception as ex:
        return HttpResponse("Error: " + ex.message)
    else:
        return render(request, 'oslayer/user_detail.html', {'user': kc.users.get(user_id)})

def create_user(request):
    """Creates a new user associated to a given domain.
    
    Args:
        request: Django request containing session.
    Returns:
        HttpResponse
    """    
    
    try:
        kc = __get_keystone_client__(request)
    except Exception as ex:
        return HttpResponse("Error: " + ex.message)
    else:
        
        kc.users.create(name=request.POST['name'], 
                        domain=request.POST['domain_id'], 
                        password=request.POST['password'], 
                        email=request.POST['email'], 
                        description=request.POST['description'], 
                        enabled=True, 
                        default_project=request.POST['default_project_id'])
        context = {
                   'users_list': kc.users.list(), 
                   'domains_list': kc.domains.list(), 
                   'projects_list': kc.projects.list()}
        return HttpResponseRedirect(reverse('oslayer:users'))

def domains(request):
    """Lists current domains available in OpenSTack.
    
    Args:
        request: Django request containing session
    Returns:
        HttpResponse 
    """
    
    try:
        kc = __get_keystone_client__(request)
    except Exception as ex:
        return HttpResponse("Error: " + ex.message)
    else:
        name = 'useit'
        description = 'Domain for UseIt projects'
        enabled = True
        #kc.domains.create(name=name, description=description, enabled=enabled)
        return render(request, 'oslayer/domains.html', {'domains_list': kc.domains.list()})
        
def domain_detail(request, domain_id):
    """Shows details for a given domain id.
    
    Args:
        request: Django request containing session.
        domain_id (str): 32 characters ID for a give domain.
    Returns:
        HttpResponse
    """    
    
    try:
        kc = __get_keystone_client__(request)
    except Exception as ex:
        return HttpResponse("Error: " + ex.message)
    else:
        return render(request, 'oslayer/domain_detail.html', {'domain': kc.domains.get(domain_id)})

class CompanyListView(generic.ListView):
    """Lists current companies.
    """
    model = Company
    form_class = AddCompanyForm

class CompanyDetailView(generic.DetailView):
    """Shows details for a given company.
    """
    model = Company
    template_name = 'oslayer/company_detail.html'
    
class CompanyCreate(FormView):
    model = Company
    template_name = 'oslayer/company_form.html'
    form_class = AddCompanyForm
    success_url = '/oslayer/companies'

class CompanyUpdate(UpdateView):
    model = Company
    fields = ['name', 'description', 'active']

class CompanyDelete(DeleteView):
    model = Company
    success_url = reverse_lazy('company-list')