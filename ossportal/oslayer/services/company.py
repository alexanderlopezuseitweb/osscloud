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

def edit(keystone_client, company_id, fields_data):
    """Request the domain change in OpenStack and the company update in the local model database.
    
    Args:
        keystone_client: Openstack Keystone authorization client.
        company_id: Company ID in the local model database.
        fields_data: (dict) Attribute values for the record to update. 
    """
    # Get the record from local model database.
    existing_company = Company.objects.get(id=company_id)
    new_name = existing_company.name
    new_description = existing_company.description
    update_domain = False
    
    # Validate name change
    
    if 'name' in fields_data:
        if fields_data['name'] is not None and fields_data['name'] != existing_company.name:
        
            # Verify that the new name is not used by other domain in OpenStack
            found_domains = keystone_client.domains.list(name=fields_data['name'])
            if len(found_domains) > 0:
                raise Exception("The domain name '%s' is already used in OpenStack.",fields_data['name'])
            
            new_name = fields_data['name']
            update_domain = True
            
    # Validate description change
    if 'description' in fields_data:
        if fields_data['description'] is not None and fields_data['description'] != existing_company.description:
            new_description = fields_data['description']
            update_domain = True  
                  
    # Update the record in OpenStack.
    if update_domain:
        found_domains = keystone_client.domains.list(name=existing_company.name)
        keystone_client.domains.update(found_domains[0].id, name=new_name, description=new_description)
              
    # Validate active change
    if 'active' in fields_data:
        if fields_data['active'] is not None and fields_data['active'] != existing_company.active:
            existing_company.active = fields_data['active']
    
    # Validate access_level change
    if 'access_level' in fields_data:
        if fields_data['access_level'] is not None and fields_data['access_level'].id != existing_company.access_level.id:
            existing_company.access_level = AccessLevel.objects.get(fields_data['access_level'])
                
    # Validate contact_address change
    if 'contact_address' in fields_data:
        if fields_data['contact_address'] is not None and fields_data['contact_address'] != existing_company.contact_address:
            existing_company.contact_address = fields_data['contact_address']
    
    # Validate billing_contact_name change
    if 'billing_contact_name' in fields_data:
        if fields_data['billing_contact_name'] is not None and fields_data['billing_contact_name'] != existing_company.billing_contact_name:
            existing_company.billing_contact_name = fields_data['billing_contact_name']
            
    # Validate billing_contact_email change
    if 'billing_contact_email' in fields_data:
        if fields_data['billing_contact_email'] is not None and fields_data['billing_contact_email'] != existing_company.billing_contact_email:
            existing_company.billing_contact_email = fields_data['billing_contact_email']
            
    # Validate billing_contact_phone change
    if 'billing_contact_phone' in fields_data:
        if fields_data['billing_contact_phone'] is not None and fields_data['billing_contact_phone'] != existing_company.billing_contact_phone:
            existing_company.billing_contact_phone = fields_data['billing_contact_phone']
            
    # Validate technical_contact_name change
    if 'technical_contact_name' in fields_data:
        if fields_data['technical_contact_name'] is not None and fields_data['technical_contact_name'] != existing_company.technical_contact_name:
            existing_company.technical_contact_name = fields_data['technical_contact_name']
                     
    # Validate technical_contact_email change
    if 'technical_contact_email' in fields_data:
        if fields_data['technical_contact_email'] is not None and fields_data['technical_contact_email'] != existing_company.technical_contact_email:
            existing_company.technical_contact_email = fields_data['technical_contact_email']
            
    # Validate technical_contact_phone change
    if 'technical_contact_phone' in fields_data:
        if fields_data['technical_contact_phone'] is not None and fields_data['technical_contact_phone'] != existing_company.technical_contact_phone:
            existing_company.technical_contact_phone = fields_data['technical_contact_phone']
           
    # Validate alternate_contact_name change
    if 'alternate_contact_name' in fields_data:
        if fields_data['alternate_contact_name'] is not None and fields_data['alternate_contact_name'] != existing_company.alternate_contact_name:
            existing_company.alternate_contact_name = fields_data['alternate_contact_name']
            
    # Validate alternate_contact_email change
    if 'alternate_contact_email' in fields_data:
        if fields_data['alternate_contact_email'] is not None and fields_data['alternate_contact_email'] != existing_company.alternate_contact_email:
            existing_company.alternate_contact_email = fields_data['alternate_contact_email']
           
    # Validate alternate_contact_phone change
    if 'alternate_contact_phone' in fields_data:
        if fields_data['alternate_contact_phone'] is not None and fields_data['alternate_contact_phone'] != existing_company.alternate_contact_phone:
            existing_company.alternate_contact_phone = fields_data['alternate_contact_phone']

    # Update the record in the local model database.
    if update_domain:
        existing_company.name = fields_data['name']
        existing_company.description = fields_data['description']
        
    existing_company.save()
        
    

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

class EditCompanyForm(forms.ModelForm):
    """Updates an existing company record.
    """
    
    def save(self, keystone_client):
        """Overrides the default save method to attempt the update of a 
        domain in OpenStack in both OpenStack and local model.
         
        Args:
            keystone_client: Openstack Keystone authorization client.
        """
        
        try:   
            fields_data = self.cleaned_data.copy()
            fields_data['enabled'] = self.cleaned_data['active']
            edit(keystone_client, self.instance.id, fields_data)
        except Exception as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info() #@UnusedVariable
            raise Exception("Error: " + str(exc_type) + " - " + ex.message)
            
    class Meta:
        model = Company
        exclude = ['created_on','created_by','modified_on','modified_by']
        widgets = {
                   'description':forms.Textarea(),
                   }

