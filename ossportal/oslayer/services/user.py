from datetime import datetime
from django import forms

from oslayer.models import User

def add(keystone_client, fields_data):
    """Attempts the creation in Openstack and then in the local database model.
        
    Args:
        keystone_client: Openstack Keystone authorization client.
        fields_data: (dict) Attribute values for the new record
    """
    name = fields_data['name']
    password = fields_data['password']
    email = fields_data['email']
    description = fields_data['description']
    enabled = fields_data['enabled']
    domain_id = fields_data['domain_id']
    default_project_id = fields_data['default_project_id']

    try:
        new_user = keystone_client.users.create(name=name, description=description, enabled=enabled, domain=domain_id, 
                                     default_project=default_project_id, password=password, email=email )
    except Exception as ex:
        raise Exception("Error: " + ex.type_name() + " - " + ex.message)
    else:
        #Successful creation in OpenStack, proceed to local model 
        User.objects.create(name=name, password=password, email=email, created_on=datetime.now(), 
                            account_main_user=False, external_id=new_user.id)
        
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
        
