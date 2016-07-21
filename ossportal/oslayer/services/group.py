import sys
import datetime
# from django.utils import timezone
from django import forms
from oslayer.models import Group

def add(fields_data):
    """Group Creation.
     
    Args:
        fields_data: (dict) Attribute values for the new record
    Return:
        new group record in the model database.
    """
    
    new_group = Group.objects.create(name=fields_data['name'],parent_group=fields_data['parent_group'])
    return new_group


def edit(group_id, fields_data):
    """Request the domain change in the group update in the local model database.
     
    Args:
        group_id: Country ID in the local model database.
        fields_data: (dict) Attribute values for the record to update. 
    """
    # Get the record from local model database.
    existing_group = Group.objects.get(id=group_id)
    
    # Validate name change
    if 'parent_group' in fields_data:
        if fields_data['parent_group'] is not None and fields_data['parent_group'] != existing_group.parent_group:         
            existing_group.parent_group = fields_data['parent_group']
            
    # Validate name change
    if 'name' in fields_data:
        if fields_data['name'] is not None and fields_data['name'] != existing_group.name:         
            existing_group.name = fields_data['name']
         
    existing_group.save()
         
     
 
class AddGroupForm(forms.ModelForm):
    """Creates a new group record.
    """
    def save(self):
        """Store the form information in DB.
         
        Args:
            self object.
        """
        try:   
            fields_data = self.cleaned_data.copy()
            add(fields_data)
        except Exception as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info() #@UnusedVariable
            raise Exception("Error: " + str(exc_type) + " - " + ex.message)
             
    class Meta:
        model = Group
        exclude = []
#         exclude = ['created_on','created_by','modified_on','modified_by']
#         widgets = {
#                    'description':forms.Textarea(),
#                    }

class EditGroupForm(forms.ModelForm):
    """Updates an existing group record.
    """
    def save(self):
        """Update the form information in DB.
         
        Args:
            self object.
        """
        try:   
            fields_data = self.cleaned_data.copy()
            edit(self.instance.id, fields_data)
        except Exception as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info() #@UnusedVariable
            raise Exception("Error: " + str(exc_type) + " - " + ex.message)
   
    class Meta:
        model = Group
        exclude = []
#         exclude = ['created_on','created_by','modified_on','modified_by']
#         widgets = {
#                    'description':forms.Textarea(),
#                    }

