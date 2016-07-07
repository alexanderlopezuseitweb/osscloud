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
    
def edit(keystone_client, project_id, fields_data):
    """Request the project mmodification to OpenStack through the client API.
    
    Args:
        keystone_client: OpenStack KeyStone authorization client.
        project_id (str): 32 characters ID for a give project.
        fields_data: (dict) Attribute values for the new record
    """
    name = fields_data['name']
    description = fields_data['description']
    enabled = fields_data['enabled']
    keystone_client.projects.update(project_id, name=name, description=description, enabled=enabled) 

class ProjectForm(forms.Form):
    """Creates a new Openstack project record.
    """
    name = forms.CharField(label='Name', max_length=50, help_text='Project name')
    description = forms.CharField(label='Description', widget=forms.Textarea, required=False, max_length=200, help_text='Short description for this project')
    enabled = forms.BooleanField(label='Is enabled?', required=False, help_text='Check if the new project is enabled by default')
    
    def set_choices(self, keystone_client, data=None):
        """Request the domains list to openstack through the client API.
        
        Args:
            keystone_client: Openstack Keystone authorization client.
            data: (dict) data values from the stored record.
        """
        initial = None
        if data is not None:
            initial = {'domain_id':data['domain_id']}
            attrs={'disabled': 'disabled'}
        else:
            attrs=None
            
        choices = [(d.id, d.name) for d in keystone_client.domains.list()]
        domain_id = forms.ChoiceField(label='Parent domain', widget=forms.Select(attrs=attrs), 
                                      choices = choices, initial=initial, required=False, 
                                      help_text='Parent domain for this project')
        self.fields['domain_id'] =  domain_id
        

