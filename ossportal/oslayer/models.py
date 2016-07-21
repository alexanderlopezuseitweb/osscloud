from __future__ import unicode_literals

from django.db import models
from django.template.defaultfilters import default
# from Canvas import Group

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
    
    def __str__(self):
        return self.name

class AuditInfo(models.Model):
    """Common fields to models intended to be used to audit transactions on records.
    """
    created_on = models.DateTimeField(auto_now_add=False, editable=False, blank=True, help_text="Date of creation.")
    created_by = models.ForeignKey(User, related_name='+', help_text="User who created the record.")
    modified_on = models.DateTimeField(auto_now=True, editable=False, blank=True, help_text="Date of last modification.")
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
        
class Setting(models.Model):
    """Configuration settings.
    """
    id = models.CharField(max_length=20, primary_key=True, help_text="Setting ID Key.")
    description = models.TextField(max_length=500, blank=True, help_text="Short description of how this setting works.")
    value = models.CharField(max_length=100, help_text="String value for this setting.")
    
    def __str__(self):
        return self.id

class Country(AuditInfo):
    """ Country information.
    """
    id = models.AutoField(primary_key=True, help_text="Country ID sequence.")
    name = models.CharField(max_length=64, help_text="Country name.")
    code2 = models.CharField(max_length=2, null=True, help_text="Two digits country code.")
    code3 = models.CharField(max_length=3, null=True, help_text="Three digits country code.")
    public = models.BooleanField(default=True, help_text="True: public, False: not public");
    #public = models.ForeignKey(AccessLevel, blank=True, help_text="Access Level required to see this company.")
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'countries'
        
class State(AuditInfo):
    """ State information.
    """
    id = models.AutoField(primary_key=True, help_text="State ID sequence.")
    country_id = models.ForeignKey(Country, blank=False, help_text="Country where the state is located.")
    name = models.CharField(max_length=45, help_text="State name.")
    code2 = models.CharField(max_length=2, null=True, help_text="Two digits state code.")
    code3 = models.CharField(max_length=3, null=True, help_text="Three digits state code.")
    public = models.BooleanField(default=True, help_text="True: public, False: not public")
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'states'
        
class City(AuditInfo):
    """ City information.
    """
    id = models.AutoField(primary_key=True, help_text="City ID sequence.")
    state_id = models.ForeignKey(State, blank=False, help_text="State where the city is located.")
    name = models.CharField(max_length=45, help_text="City name.")
    code2 = models.CharField(max_length=2, null=True, help_text="Two digits state code.")
    code3 = models.CharField(max_length=3, null=True, help_text="Three digits state code.")
    public = models.BooleanField(default=True, help_text="True: public, False: not public")
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'cities'
        
class Group(models.Model):
    """ Group information.
    """
    id = models.AutoField(primary_key=True, help_text="Group ID sequence.")
    parent_group = models.ForeignKey('self', null=True, blank=True, help_text="Group parent of this group.")
    name = models.CharField(max_length=64, help_text="Group name.")
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'groups'
        
class UserGroup(models.Model):
    """ Many to many intermediate class for User and Group.
    """
    user_id = models.ForeignKey(User, help_text="User Id sequence")
    group_id = models.ForeignKey(Group, help_text="Group Id sequence")
    
    class Meta:
        verbose_name_plural = 'users_groups'
    
class AccessLevelGroup(models.Model):
    """ Many to many intermediate class for AccessLevel and Group.
    """
    access_level_id = models.ForeignKey(AccessLevel, help_text="Access Level Id sequence")
    group_id = models.ForeignKey(Group, help_text="Group Id sequence")
    
    class Meta:
        verbose_name_plural = 'access_levels_groups'

