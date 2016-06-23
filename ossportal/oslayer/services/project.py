from django import forms

def add(keystone_client, fields_data):
    """Request the project creation to openstack through the client API.
    
    Args:
        keystone_client: Openstack Keystone authorization client.
        fields_data: (dict) Attribute values for the new record
    """
    name = fields_data['name']
    description = fields_data['description']
    enabled = fields_data['enabled']
    domain_id = fields_data['domain_id']
    keystone_client.projects.create(name=name, description=description, enabled=enabled, domain=domain_id)

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
        

