from django import forms

def add(keystone_client, fields_data):
    """Request the domain creation to openstack through the client API.
        
    Args:
        keystone_client: Openstack Keystone authorization client.
        fields_data: (dict) Attribute values for the new domain.
    Returns:
        domain created by OpenStack.
    """
    name = fields_data['name']
    description = fields_data['description']
    enabled = fields_data['enabled']
    return keystone_client.domains.create(name=name, description=description, enabled=enabled)
        
class AddDomainForm(forms.Form):
    """Creates a new Openstack domain record.
    """
    name = forms.CharField(label='Name', max_length=50, help_text='Domain name')
    description = forms.CharField(label='Description', widget=forms.Textarea, required=False, max_length=200, help_text='Short description for this domain')
    enabled = forms.BooleanField(label='Is enabled?', required=False, help_text='Check if the new domain is enabled by default')
    