from django import forms
from oslayer.models import Company 
from oslayer.services import domain 

def add(keystone_client, fields_data):
    """Request the company creation to openstack through the client API.
    
    Args:
        keystone_client: Openstack Keystone authorization client.
        fields_data: (dict) Attribute values for the new record
    """
    
    domain.add(keystone_client, fields_data)
    name = fields_data['name']
    description = fields_data['description']
    enabled = fields_data['enabled']
    

class AddCompanyForm(forms.ModelForm):
    """Creates a new company record.
    """
    
    def save(self, keystone_client):
        """Overrides the default save method to attempt the creation of a 
        domain in OpenStack and a default user in both OpenStack and local model.
         
        Args:
            keystone_client: Openstack Keystone authorization client.
        """
        
        company = super(AddCompanyForm, self).save(commit=False)
        try:
            #TODO: Complete    
            fields_data = {
                           'name':self.cleaned_data['name'],
                           'description':self.cleaned_data['description'],
                           'enabled':self.cleaned_data['enabled']
                           }
            add(keystone_client, fields_data)
        except Exception as ex:
            raise Exception("Error: " + ex.message)
        else:
            pass
            
    class Meta:
        model = Company
        fields = ['name', 'description', 'active', 'contact_address', 'billing_contact_name', 'billing_contact_email', 'billing_contact_phone', 'technical_contact_name', 'technical_contact_email']

