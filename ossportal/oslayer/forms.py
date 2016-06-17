from django import forms
from .models import Company

class AddCompanyForm(forms.ModelForm):
    """Creates a new company record.
    """
    class Meta:
        model = Company
        fields = ['name', 'description', 'active', 'contact_address', 'billing_contact_name', 'billing_contact_email', 'billing_contact_phone', 'technical_contact_name', 'technical_contact_email']
        
class AddDomainForm(forms.Form):
    """Creates a new Openstack domain record.
    """
    name = forms.CharField(label='Name', max_length=50, help_text='Domain name')
    description = forms.CharField(label='Description', widget=forms.Textarea, required=False, max_length=200, help_text='Short description for this domain')
    enabled = forms.BooleanField(label='Is enabled?', required=False, help_text='Check if the new domain is enabled by default')
    
    def request_openstack_creation(self, keystone_client):
        """Request the domain creation to openstack through the client API.
        
        Args:
            keystone_client: Openstack Keystone authorization client.
        """
        name = self.cleaned_data['name']
        description = self.cleaned_data['description']
        enabled = self.cleaned_data['enabled']
        keystone_client.domains.create(name=name, description=description, enabled=enabled)
        
class AddProjectForm(forms.Form):
    """Creates a new Openstack project record.
    """
    name = forms.CharField(label='Name', max_length=50, help_text='Domain name')
    description = forms.CharField(label='Description', widget=forms.Textarea, required=False, max_length=200, help_text='Short description for this project')
    enabled = forms.BooleanField(label='Is enabled?', required=False, help_text='Check if the new project is enabled by default')
    
    def set_choices(self, keystone_client):
        """Request the domains list to openstack through the client API.
        
        Args:
            keystone_client: Openstack Keystone authorization client.
        """
        choices = [(d.id, d.name) for d in keystone_client.domains.list()]
        domain_id = forms.ChoiceField(label='Parent domain', widget=forms.Select, choices = choices, required=False, help_text='Short description for this project')
        self.fields['domain_id'] =  domain_id
        
    def request_openstack_creation(self, keystone_client):
        """Request the project creation to openstack through the client API.
        
        Args:
            keystone_client: Openstack Keystone authorization client.
        """
        name = self.cleaned_data['name']
        description = self.cleaned_data['description']
        enabled = self.cleaned_data['enabled']
        domain_id = self.cleaned_data['domain_id']
        keystone_client.projects.create(name=name, description=description, enabled=enabled, domain=domain_id)
        
class AddUserForm(forms.Form):
    """Creates a new Openstack user record.
    """
    name = forms.CharField(label='Name', max_length=50, help_text='Domain name')
    description = forms.CharField(label='Description', widget=forms.Textarea, required=False, max_length=200, help_text='Short description for this user')
    password = forms.CharField(label='Password', widget=forms.PasswordInput, max_length=200, help_text='Default password for this user')
    email = forms.EmailField(label='E-mail', max_length=50, help_text='Contact email for this user')
    enabled = forms.BooleanField(label='Is enabled?', required=False, help_text='Check if the new user is enabled by default')
    
    def set_choices(self, keystone_client):
        """Request the domains list to openstack through the client API.
        
        Args:
            keystone_client: Openstack Keystone authorization client.
        """
        choices = [(d.id, d.name) for d in keystone_client.domains.list()]
        domain_id = forms.ChoiceField(label='Parent domain', widget=forms.Select, choices=choices, required=False, help_text='Domain to which belongs this user')
        self.fields['domain_id'] =  domain_id
        
        choices_projects = [(p.id, p.name) for p in keystone_client.projects.list()]
        default_project_id = forms.ChoiceField(label='Default project', widget=forms.Select, choices=choices_projects, required=False, help_text='Project under which this user will be created by default')
        self.fields['default_project_id'] =  default_project_id
        
    def request_openstack_creation(self, keystone_client):
        """Request the user creation to openstack through the client API.
        
        Args:
            keystone_client: Openstack Keystone authorization client.
        """
        name = self.cleaned_data['name']
        password = self.cleaned_data['password']
        email = self.cleaned_data['email']
        description = self.cleaned_data['description']
        enabled = self.cleaned_data['enabled']
        domain_id = self.cleaned_data['domain_id']
        default_project_id = self.cleaned_data['default_project_id']
        keystone_client.users.create(name=name, description=description, enabled=enabled, domain=domain_id, 
                                     default_project=default_project_id, password=password, email=email )
        