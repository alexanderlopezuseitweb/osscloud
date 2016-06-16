from django.forms import ModelForm
from .models import Company

class AddCompanyForm(ModelForm):
    """Creates a new company record.
    """
    class Meta:
        model = Company
        fields = ['name', 'description', 'active', 'contact_address', 'billing_contact_name', 'billing_contact_email', 'billing_contact_phone', 'technical_contact_name', 'technical_contact_email']