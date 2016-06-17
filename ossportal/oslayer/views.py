from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView,\
    FormView

from .models import Company
from forms import AddCompanyForm, AddDomainForm, AddProjectForm, AddUserForm
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

def project_list(request):
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
        return render(request, 'oslayer/project_list.html', {'project_list': kc.projects.list()})
        
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

def project_add(request):
    """Form to create a new project record.
    
    Args:
        request: Django request containing session and data from post.
    """
    keystone_client = __get_keystone_client__(request)
            
    # if this is a POST request, process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AddProjectForm(request.POST)
        form.set_choices(keystone_client)
        # check whether it is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            form.request_openstack_creation(keystone_client)
            # redirect to a new URL:
            return render(request, 'oslayer/project_list.html', {'project_list': keystone_client.projects.list()})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AddProjectForm()
        form.set_choices(keystone_client)

    return render(request, 'oslayer/project_form.html', {'form': form})

def user_list(request):
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
        return render(request, 'oslayer/user_list.html', {'user_list': kc.users.list()})
        
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

def user_add(request):
    """Creates a new user associated to a given domain.
    
    Args:
        request: Django request containing session.
    Returns:
        HttpResponse
    """
    keystone_client = __get_keystone_client__(request)
    # if this is a POST request, process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AddUserForm(request.POST)
        form.set_choices(keystone_client)
        # check whether it is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            keystone_client = __get_keystone_client__(request)
            form.request_openstack_creation(keystone_client)
            # redirect to a new URL:
            return render(request, 'oslayer/user_list.html', {'user_list': keystone_client.users.list()})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AddUserForm()
        form.set_choices(keystone_client)

    return render(request, 'oslayer/user_form.html', {'form': form})    

def domain_list(request):
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
        return render(request, 'oslayer/domain_list.html', {'domain_list': kc.domains.list()})
        
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

def domain_add(request):
    """Form to create a new domain record.
    
    Args:
        request: Django request containing session and data from post.
    """
    # if this is a POST request, process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AddDomainForm(request.POST)
        # check whether it is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            keystone_client = __get_keystone_client__(request)
            form.request_openstack_creation(keystone_client)
            # redirect to a new URL:
            return render(request, 'oslayer/domain_list.html', {'domain_list': keystone_client.domains.list()})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AddDomainForm()

    return render(request, 'oslayer/domain_form.html', {'form': form})
    
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
    
class CompanyCreate(CreateView):
    model = Company
    fields = ['name', 'description', 'active', 'contact_address', 'billing_contact_name', 'billing_contact_email', 'billing_contact_phone', 'technical_contact_name', 'technical_contact_email']

class CompanyUpdate(UpdateView):
    model = Company
    fields = ['name', 'description', 'active']

class CompanyDelete(DeleteView):
    model = Company
    success_url = reverse_lazy('company-list')