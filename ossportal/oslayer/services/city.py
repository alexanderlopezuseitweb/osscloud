import sys
import datetime
# from django.utils import timezone
from django import forms
from oslayer.models import City

def add(fields_data):
    """City Creation.
     
    Args:
        fields_data: (dict) Attribute values for the new record
    Return:
        new state record in the model database.
    """
    
    new_city = City.objects.create(state_id=fields_data['state_id'],
                                    name=fields_data['name'],code2=fields_data['code2'],
                                    code3=fields_data['code3'],public=fields_data['public'],
                                    created_by=fields_data['created_by'],modified_by=fields_data['modified_by'],
                                    created_on=str(datetime.datetime.now()),modified_on=str(datetime.datetime.now())
                                    )
    return new_city


def edit(city_id, fields_data):
    """Request the domain change in the city update in the local model database.
     
    Args:
        state_id: Country ID in the local model database.
        fields_data: (dict) Attribute values for the record to update. 
    """
    # Get the record from local model database.
    existing_city = City.objects.get(id=city_id)
    
    # Validate name change
    if 'name' in fields_data:
        if fields_data['name'] is not None and fields_data['name'] != existing_city.name:         
            existing_city.name = fields_data['name']
            
    # Validate name change
    if 'state_id' in fields_data:
        if fields_data['state_id'] is not None and fields_data['state_id'] != existing_city.state_id:         
            existing_city.state_id = fields_data['state_id']
            
    # Validate code2 change
    if 'code2' in fields_data:
        if fields_data['code2'] is not None and fields_data['code2'] != existing_city.code2:         
            existing_city.code2 = fields_data['code2']
            
    # Validate code3 change        
    if 'code3' in fields_data:
        if fields_data['code3'] is not None and fields_data['code3'] != existing_city.code3:         
            existing_city.code3 = fields_data['code3']
            
    # Validate public change        
    if 'public' in fields_data:
        if fields_data['public'] is not None and fields_data['public'] != existing_city.public:         
            existing_city.public = fields_data['public']
            
    # Validate modified_by change
    if 'modified_by' in fields_data:
        if fields_data['modified_by'] is not None and fields_data['modified_by'] != existing_city.modified_by_id:         
            existing_city.modified_by_id = fields_data['modified_by']
         
    existing_city.modified_on = str(datetime.datetime.now())
    
    existing_city.save()
         
     
 
class AddCityForm(forms.ModelForm):
    """Creates a new city record.
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
        model = City
        exclude = ['created_on','modified_on']
#         widgets = {
#                    'description':forms.Textarea(),
#                    }

class EditCityForm(forms.ModelForm):
    """Updates an existing city record.
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
        model = City
        exclude = ['created_on','created_by','modified_on']
#         widgets = {
#                    'description':forms.Textarea(),
#                    }

