import sys
from django.utils import timezone
from django import forms

from oslayer.models import User, Company

class IllegalDeletion(Exception):
    """Exception when an attempt to delete an user is not consistent
    with the business logic.
    """
    def __init__(self, reason):
        """Instantiate a new object IllegalException.
        
        Args:
            reason: (str) Explanation for the exception.
        """
        super(Exception, self).__init__(reason) 

def add(keystone_client, fields_data):
    """Attempts the creation in Openstack and then in the local database model.
        
    Args:
        keystone_client: Openstack Keystone authorization client.
        fields_data: (dict) Attribute values for the new record.
    Returns:
        model user created in the local database.
    """
    name = fields_data['name']
    password = fields_data['password']
    email = fields_data['email']
    description = fields_data['description']
    enabled = fields_data['enabled']
    domain_id = fields_data['domain_id']
    default_project_id = fields_data['default_project_id']
    account_main_user = fields_data['account_main_user']
    security_question_answer = fields_data['security_question_answer']
    security_question = fields_data['security_question']

    try:
        new_user = keystone_client.users.create(name=name, description=description, enabled=enabled, domain=domain_id, 
                                     default_project=default_project_id, password=password, email=email)
    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info() #@UnusedVariable
        raise Exception("Error: " + str(exc_type) + " - " + ex.message)
    else:
        #Successful creation in OpenStack, proceed to local model 
        return User.objects.create(name=name, password=password, email=email, created_on=timezone.now(),
                                     account_main_user=account_main_user , external_id=new_user.id,
                                     security_question_answer=security_question_answer, 
                                     security_question=security_question)

def edit(keystone_client, user_id, fields_data):
    """Attempts the creation in Openstack and then in the local database model.
        
    Args:
        keystone_client: Openstack Keystone authorization client.
        fields_data: (dict) Attribute values for the new record.
    """
    # Get existing user from the local model database
    existing_user = User.objects.get(id=user_id)
    
    # Get data to update 
    name = fields_data['name']
    email = fields_data['email']
    description = fields_data['description']
    enabled = fields_data['enabled']
    default_project_id = fields_data['default_project_id']
    account_main_user = fields_data['account_main_user']
    security_question_answer = fields_data['security_question_answer']
    security_question = fields_data['security_question']
    if len(fields_data['password']) > 0:
        password = fields_data['password']
    else:
        password = None

    try:
        keystone_client.users.update(existing_user.external_id, name=name, description=description, 
                                     enabled=enabled, password=password, default_project=default_project_id, 
                                     email=email)
    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info() #@UnusedVariable
        raise Exception("Error: " + str(exc_type) + " - " + ex.message)
    else:
        # Successful update in OpenStack, proceed to local model 
        existing_user.name=name
        existing_user.email=email
        existing_user.account_main_user=account_main_user
        existing_user.security_question_answer=security_question_answer
        existing_user.security_question=security_question
        if password is not None:
            existing_user.password=password
        existing_user.save()

def delete(keystone_client, user_id):
    """Request the company elimination from openstack through the client API.
    Attempts the elimination of an existing domain in OpenStack, an existing user in both OpenStack
    and the local model database and an existing company in the local model database.
    
    Args:
        keystone_client: OpenStack KeyStone authorization client.
        user_id: (string) ID at the local model database for the user
    """
    existing_user = User.objects.get(id=user_id)
    
    # Check if the user exists
    if existing_user is None:
        raise IllegalDeletion("User with id %s not found.",user_id)
    
    # Check if the user is not needed
    if existing_user.account_main_user:
        raise IllegalDeletion("This user cannot be removed as long as it be the main user of an account.")
    
    companies_with_this_user = Company.objects.filter(created_by_id=existing_user.id)
    if len(companies_with_this_user) > 0:
        raise IllegalDeletion("This user cannot be removed as long as it was used to create a company.")
   
    # Remove from OpenStack
    if existing_user.external_id is not None:
        keystone_client.users.delete(existing_user.external_id)
    # Remove from local model database
    existing_user.delete()
  
class UserForm(forms.Form):
    """Displays a form to create a new Openstack user record or modify an existent one.
    """
    name = forms.CharField(label='Name', max_length=50, help_text='Domain name')
    description = forms.CharField(label='Description', widget=forms.Textarea, required=False, max_length=200, help_text='Short description for this user')
    password = forms.CharField(label='Password', widget=forms.PasswordInput, required=False, max_length=200, help_text='Default password for this user')
    email = forms.EmailField(label='E-mail', max_length=50, help_text='Contact email for this user')
    security_question = forms.CharField(label='Security question', max_length=100, required=False, 
                                        help_text="Security question to be used on the event of password lose or user ID lose.")   
    security_question_answer = forms.CharField(label='Answer', max_length=100, required=False,
                                               help_text="Answer to the security question to be used on the event of password lose or user ID lose.") 
    
    enabled = forms.BooleanField(label='Is enabled?', required=False, help_text='Check if the new user is enabled by default')
    account_main_user = forms.BooleanField(label='Is the main user of its account?', required=False, help_text='Check if this is the main user of its account')
    
    def set_choices(self, keystone_client, data=None):
        """Request the domains list to OpenStack through the client API.
        
        Args:
            keystone_client: OpenStack KeyStone authorization client.
            data: (dict) data values from the stored record.
        """
        initial = None
        if data is not None:
            initial = {
                       'domain_id':data['domain_id'], 
                       'default_project_id':data['default_project_id']
                       }
            # Prevent that the domain be changed, which is forbidden by Openstack.
            attrs={'disabled': 'disabled'}
        else:
            attrs=None
            
        choices = [(d.id, d.name) for d in keystone_client.domains.list()]
        domain_id = forms.ChoiceField(label='Parent domain', widget=forms.Select(attrs=attrs), choices=choices, 
                                      initial=initial, required=False, help_text='Domain to which this user belongs')
        self.fields['domain_id'] =  domain_id
        
        choices_projects = [(p.id, p.name) for p in keystone_client.projects.list()]
        default_project_id = forms.ChoiceField(label='Default project', widget=forms.Select, 
                                               choices=choices_projects, initial=initial, required=False, 
                                               help_text='Project under which this user will be created by default')
        self.fields['default_project_id'] =  default_project_id
        
