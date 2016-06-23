from __future__ import unicode_literals

from django.db import models

from .apps import OSLayerConfig

# Create your models here.
class User(models.Model):
    """Login accesses for people related to an account in order to work in projects.
    """
    id = models.AutoField(primary_key=True, help_text="User ID sequence.")
    name = models.CharField(max_length=45, help_text="Name to identify the user.")
    email = models.CharField(max_length=45, help_text="Contact e-mail.")
    password = models.CharField(max_length=45, blank=True, help_text="Password set by the user.")
    security_question = models.CharField(max_length=100, blank=True, help_text="Security question to be used on the event of password lose or user ID lose.")   
    security_question_answer = models.CharField(max_length=100, blank=True, 
                                                help_text="Answer to the security question to be used on the event of password lose or user ID lose.")    
    created_on = models.DateTimeField(help_text="Date of creation.")
    is_confirmed = models.BooleanField(default=False, help_text="Whether the user is confirmed or not. Default is FALSE.")
    external_id = models.CharField(max_length=50, blank=True, help_text="Openstack ID for this user.")
    account_main_user = models.BooleanField(default=False, help_text="Whether the user is the main one for its Account. Default is FALSE.")
#    account = models.ForeignKey(Account, help_text="Account to which the user belongs.")
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = OSLayerConfig.name + "_users"

class AuditInfo(models.Model):
    """Common fields to models intended to be used to audit transactions on records.
    """
    created_on = models.DateTimeField(auto_now_add=True, help_text="Date of creation.")
    created_by = models.ForeignKey(User, related_name='+', help_text="User who created the record.")
    modified_on = models.DateTimeField(auto_now=True, help_text="Date of last modification.")
    modified_by = models.ForeignKey(User, related_name='+', help_text="User who last updated the record.")

    class Meta:
        abstract = True

class AccessLevel(models.Model):
    """Access levels to company records for users.
    """
    id = models.AutoField(primary_key=True, help_text="Access Level ID sequence.")
    name = models.CharField(max_length=45, help_text="Name to identify the access level.")

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = OSLayerConfig.name + "_access_levels"

class Company(AuditInfo):
    """Entity to be billed for products and services.
    """
    id = models.AutoField(primary_key=True, help_text="Company ID sequence.")
    name = models.CharField(max_length=45, help_text="Company name or Customer.")
    description = models.CharField(max_length=500, blank=True, help_text="Short description of company or customer.")
    active = models.BooleanField(default=True, help_text="Is the company active?")
    access_level = models.ForeignKey(AccessLevel, blank=True, help_text="Access Level required to see this company.")
    contact_address = models.CharField(max_length=200, help_text="Address to contact the account representatives.")
    billing_contact_name = models.CharField(max_length=100, help_text="Name of the billing contact.")
    billing_contact_email = models.EmailField(max_length=254, help_text="Email of the billing contact.")
    billing_contact_phone = models.CharField(max_length=20, blank=True, help_text="Phone of the billing contact.")
    technical_contact_name = models.CharField(max_length=100, help_text="Name of the technical contact.")
    technical_contact_email = models.EmailField(max_length=254, help_text="Email of the technical contact.")
    technical_contact_phone = models.CharField(max_length=20, blank=True, help_text="Phone of the technical contact.")
    alternate_contact_name = models.CharField(max_length=100, blank=True, help_text="Name of the alternate contact.")
    alternate_contact_email = models.EmailField(max_length=254, blank=True, help_text="Email of the alternate contact.")
    alternate_contact_phone = models.CharField(max_length=20, blank=True, help_text="Phone of the alternate contact.")
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'companies'
        db_table = OSLayerConfig.name + "_companies"
        
class Setting(models.Model):
    """Configuration settings.
    """
    id = models.CharField(max_length=20, primary_key=True, help_text="Setting ID Key.")
    description = models.TextField(max_length=500, blank=True, help_text="Short description of how this setting works.")
    value = models.CharField(max_length=100, help_text="String value for this setting.")
    
    def __str__(self):
        return self.id

    class Meta:
        db_table = OSLayerConfig.name + "_settings"