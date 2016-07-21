from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.views.generic.edit import DeleteView

from models import Company, User, Country, State, City, Group
from services import company, domain, user, project, country, state, city, group
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
    return render(request, 'oslayer/index.html')

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
        return render(request, 'oslayer/project_list.html', {'project_list': kc.projects.list()})
        
def project_edit(request, project_id):
    """Shows details for a given project id.
    
    Args:
        request: Django request containing session.
        project_id (str): 32 characters ID for a give project.
    Returns:
        HttpResponse
    """    
    
    try:
        keystone_client = __get_keystone_client__(request)
    except Exception as ex:
        return HttpResponse("Error: " + ex.message)
        
    instance = keystone_client.projects.get(project_id)
    data = {
                'name' : instance.name,
                'description' : instance.description,
                'enabled' : instance.enabled,
                'domain_id' : instance.domain_id
            }
    # if this is a POST request, process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = project.ProjectForm(request.POST)
        form.set_choices(keystone_client)
        # check whether it is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            project.edit(keystone_client, project_id, form.cleaned_data)
            # redirect to a new URL:
            return render(request, 'oslayer/project_list.html', {'project_list': keystone_client.projects.list()})

    # if a GET (or any other method) we'll create a form filled with the instance's data
    else:
        form = project.ProjectForm(initial=data)
        form.set_choices(keystone_client, data)

    return render(request, 'oslayer/project_edit.html', {'form': form, 'project_id':project_id})
    

def project_add(request):
    """Form to create a new project record.
    
    Args:
        request: Django request containing session and data from post.
    """
    keystone_client = __get_keystone_client__(request)
            
    # if this is a POST request, process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = project.ProjectForm(request.POST)
        form.set_choices(keystone_client)
        # check whether it is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            project.add(keystone_client, form.cleaned_data)
            # redirect to a new URL:
            return render(request, 'oslayer/project_list.html', {'project_list': keystone_client.projects.list()})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = project.ProjectForm()
        form.set_choices(keystone_client)

    return render(request, 'oslayer/project_form.html', {'form': form})

def user_list(request):
    """Lists current users available in OpenSTack.
    
    Args:
        request: Django request containing session
    Returns:
        HttpResponse 
    """
    
    return render(request, 'oslayer/user_list.html', {'user_list': User.objects.all()})
        
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

def user_edit(request, user_id):
    """Modifies an existing user associated to a given domain.
    
    Args:
        request: Django request containing session.
        user_id (int): sequence ID for the user.
    Returns:
        HttpResponse
    """
    try:
        keystone_client = __get_keystone_client__(request)
    except Exception as ex:
        return HttpResponse("Error: " + ex.message)
    
    # if this is a POST request, process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = user.UserForm(request.POST)
        form.set_choices(keystone_client)
        # check whether it is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            user.edit(keystone_client, user_id, form.cleaned_data)
            # redirect to a new URL:
            return redirect('/oslayer/user/')

    # if a GET (or any other method) we'll create a form filled with the instance's data
    else:
        instance = User.objects.get(id=user_id)
        ks_user = keystone_client.users.get(instance.external_id)
        data = {
                'name' : instance.name,
                'password' : instance.password,
                'email' : instance.email,
                'description' : ks_user.description,
                'enabled' : ks_user.enabled,
                'domain_id' : ks_user.domain_id,
                'default_project_id' : ks_user.default_project_id,
                'account_main_user' : instance.account_main_user,
                'security_question_answer' : instance.security_question_answer,
                'security_question' : instance.security_question                
                }
        form = user.UserForm(initial=data)
        form.set_choices(keystone_client, data)

    return render(request, 'oslayer/user_edit.html', {'form': form, 'user_id':user_id})    


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
        form = user.UserForm(request.POST)
        form.set_choices(keystone_client)
        # check whether it is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            user.add(keystone_client, form.cleaned_data)
            # redirect to a new URL:
            return redirect('/oslayer/user/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = user.UserForm()
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
        form = domain.AddDomainForm(request.POST)
        # check whether it is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            keystone_client = __get_keystone_client__(request)
            domain.add(keystone_client, form.cleaned_data)
            # redirect to a new URL:
            return redirect('/oslayer/domain/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = domain.AddDomainForm()

    return render(request, 'oslayer/domain_form.html', {'form': form})

def company_add(request):
    """Form to create a new company record.
    
    Args:
        request: Django request containing session and data from post.
    """
    # if this is a POST request, process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = company.AddCompanyForm(request.POST)
        # check whether it is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            keystone_client = __get_keystone_client__(request)
            form.save(keystone_client)
            # redirect to a new URL:
            return redirect('/oslayer/company/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = company.AddCompanyForm()

    return render(request, 'oslayer/company_form.html', {'form': form})

def company_edit(request, company_id):
    """Form to create a new company record.
    
    Args:
        request: Django request containing session and data from post.
        company_id: 
    """
    instance = get_object_or_404(Company, id=company_id)
    # if this is a POST request, process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = company.EditCompanyForm(request.POST or None, instance=instance)
        # check whether it is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            keystone_client = __get_keystone_client__(request)
            form.save(keystone_client)
            # redirect to a new URL:
            return redirect('/oslayer/company/')

    # if a GET (or any other method) we'll create a form filled with the instance's data
    else:
        form = company.EditCompanyForm(instance=instance)

    return render(request, 'oslayer/company_edit.html', {'form': form, 'company_id':company_id})

class CompanyListView(generic.ListView):
    """Lists current companies.
    """
    model = Company

class CompanyDelete(DeleteView):
    model = Company
    success_url = reverse_lazy('company_list')

#Created by Alexander Lopez
def country_add(request):
    """Form to create a new country record.
     
    Args:
        request: Django request containing session and data from post.
    """
    # if this is a POST request, process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = country.AddCountryForm(request.POST)
        # check whether it is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            form.save()
            # redirect to a new URL:
            return redirect('/oslayer/country/')
 
    # if a GET (or any other method) we'll create a blank form
    else:
        form = country.AddCountryForm()
 
    return render(request, 'oslayer/country_form.html', {'form': form})
 
def country_edit(request, country_id):
    """Form to edit a country record.
     
    Args:
        request: Django request containing session and data from post.
        country_id: 
    """
    instance = get_object_or_404(Country, id=country_id)
    # if this is a POST request, process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = country.EditCountryForm(request.POST or None, instance=instance)
        
        # check whether it is valid:  
        if form.is_valid():
            # process the data in form.cleaned_data as required
            form.save()
            # redirect to a new URL:
            return redirect('/oslayer/country/')
 
    # if a GET (or any other method) we'll create a form filled with the instance's data
    else:
        form = country.EditCountryForm(instance=instance)
 
    return render(request, 'oslayer/country_edit.html', {'form': form, 'country_id':country_id})
 
class CountryListView(generic.ListView):
    """Lists current countries.
    """
    model = Country
 
class CountryDelete(DeleteView):
    model = Country
    success_url = '/oslayer/country/'
    #success_url = reverse_lazy('country_list')

def state_add(request):
    """Form to create a new state record.
     
    Args:
        request: Django request containing session and data from post.
    """
    # if this is a POST request, process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = state.AddStateForm(request.POST)
        # check whether it is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            form.save()
            # redirect to a new URL:
            return redirect('/oslayer/state/')
 
    # if a GET (or any other method) we'll create a blank form
    else:
        form = state.AddStateForm()
 
    return render(request, 'oslayer/state_form.html', {'form': form})
 
def state_edit(request, state_id):
    """Form to edit a country record.
     
    Args:
        request: Django request containing session and data from post.
        country_id: 
    """
    instance = get_object_or_404(State, id=state_id)
    # if this is a POST request, process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = state.EditStateForm(request.POST or None, instance=instance)
        # check whether it is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            form.save()
            # redirect to a new URL:
            return redirect('/oslayer/state/')
 
    # if a GET (or any other method) we'll create a form filled with the instance's data
    else:
        form = state.EditStateForm(instance=instance)
 
    return render(request, 'oslayer/state_edit.html', {'form': form, 'state_id':state_id})
 
class StateListView(generic.ListView):
    """Lists current states.
    """
    model = State
 
class StateDelete(DeleteView):
    model = State
    success_url = '/oslayer/state/'
    #success_url = reverse_lazy('state_list',kwargs={},current_app='oslayer')

def city_add(request):
    """Form to create a new city record.
     
    Args:
        request: Django request containing session and data from post.
    """
    # if this is a POST request, process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = city.AddCityForm(request.POST)
        # check whether it is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            form.save()
            # redirect to a new URL:
            return redirect('/oslayer/city/')
 
    # if a GET (or any other method) we'll create a blank form
    else:
        form = city.AddCityForm()
 
    return render(request, 'oslayer/city_form.html', {'form': form})
 
def city_edit(request, city_id):
    """Form to edit a city record.
     
    Args:
        request: Django request containing session and data from post.
        country_id: 
    """
    instance = get_object_or_404(City, id=city_id)
    # if this is a POST request, process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = city.EditCityForm(request.POST or None, instance=instance)
        # check whether it is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            form.save()
            # redirect to a new URL:
            return redirect('/oslayer/city/')
 
    # if a GET (or any other method) we'll create a form filled with the instance's data
    else:
        form = city.EditCityForm(instance=instance)
 
    return render(request, 'oslayer/city_edit.html', {'form': form, 'city_id':city_id})
 
class CityListView(generic.ListView):
    """Lists current cities.
    """
    model = City
 
class CityDelete(DeleteView):
    model = City
    success_url = '/oslayer/city/'
    #success_url = reverse_lazy('city_list')

def group_add(request):
    """Form to create a new group record.
     
    Args:
        request: Django request containing session and data from post.
    """
    # if this is a POST request, process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = group.AddGroupForm(request.POST)
        # check whether it is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            form.save()
            # redirect to a new URL:
            return redirect('/oslayer/group/')
 
    # if a GET (or any other method) we'll create a blank form
    else:
        form = group.AddGroupForm()
 
    return render(request, 'oslayer/group_form.html', {'form': form})
 
def group_edit(request, group_id):
    """Form to edit a city record.
     
    Args:
        request: Django request containing session and data from post.
        country_id: 
    """
    instance = get_object_or_404(Group, id=group_id)
    # if this is a POST request, process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = group.EditGroupForm(request.POST or None, instance=instance)
        # check whether it is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            form.save()
            # redirect to a new URL:
            return redirect('/oslayer/group/')
 
    # if a GET (or any other method) we'll create a form filled with the instance's data
    else:
        form = group.EditGroupForm(instance=instance)
 
    return render(request, 'oslayer/group_edit.html', {'form': form, 'group_id':group_id})
 
class GroupListView(generic.ListView):
    """Lists current cities.
    """
    model = Group
 
class GroupDelete(DeleteView):
    model = Group
    success_url = '/oslayer/group/'
    #success_url = reverse_lazy('group_list')
