import sys
from django.utils import timezone
from django import forms
from oslayer.models import Company, AccessLevel
from oslayer.services import domain 
from oslayer.services import user
from oslayer.openstack import api

def add(keystone_client, fields_data):
    """Request the company creation to openstack through the client API.
    Attempts the creation of a new domain in OpenStack, a new user in both OpenStack
    and the local database and a new company in the local database.
    
    Args:
        keystone_client: Openstack Keystone authorization client.
        fields_data: (dict) Attribute values for the new record
    Return:
        new company record in the model database.
    """
    # Create new domain in OpenStack
    new_domain = domain.add(keystone_client, fields_data)
    
    # Create new user in OpenStack and local model database
    user_fields_data = {
                        'name' : fields_data['name'],
                        'password' : api.get_setting(api.DEFAULT_PASSWORD_SETTING),
                        'email' : fields_data['technical_contact_email'],
                        'description' : fields_data['description'] ,
                        'enabled' : fields_data['enabled'],
                        'domain_id' : new_domain.id,
                        'default_project_id' : api.get_setting(api.DEFAULT_PROJECT_ID_SETTING),
                        'account_main_user':True                       
                        }
    new_model_user = user.add(keystone_client, user_fields_data)

    
    # Create new company in local database
    access_level_name = api.get_setting(api.DEFAULT_ACCESS_LEVEL)
    al = AccessLevel.objects.get(name=access_level_name)
    new_company = Company.objects.create(name=fields_data['name'],description=fields_data['description'],
                                         active=fields_data['active'],contact_address=fields_data['contact_address'],
                                         billing_contact_name=fields_data['billing_contact_name'],
                                         billing_contact_email=fields_data['billing_contact_email'],
                                         billing_contact_phone=fields_data['billing_contact_phone'],
                                         technical_contact_name=fields_data['technical_contact_name'],
                                         technical_contact_email=fields_data['technical_contact_email'],
                                         created_by=new_model_user, created_on=timezone.now(),
                                         modified_by=new_model_user, access_level=al)
    return new_company

class AddCompanyForm(forms.ModelForm):
    """Creates a new company record.
    """
    
    def save(self, keystone_client):
        """Overrides the default save method to attempt the creation of a 
        domain in OpenStack and a default user in both OpenStack and local model.
         
        Args:
            keystone_client: Openstack Keystone authorization client.
        """
        
        try:   
            fields_data = self.cleaned_data.copy()
            fields_data['enabled'] = self.cleaned_data['active']
            add(keystone_client, fields_data)
        except Exception as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info() #@UnusedVariable
            raise Exception("Error: " + str(exc_type) + " - " + ex.message)
            
    class Meta:
        model = Company
        exclude = ['created_on','created_by','modified_on','modified_by']
        widgets = {
                   'description':forms.Textarea(),
                   }
