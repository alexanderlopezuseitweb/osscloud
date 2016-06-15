from django.test import TestCase

from .models import Setting
from openstack import api
# Create your tests here.

class OpenStackTests(TestCase):
    ks_client = None
    
    def setUp(self):
        """Create connection settings to be used in further tests.
        """
        TestCase.setUp(self)
        Setting.objects.create(id='auth_url', value='http://192.168.1.58:5000/v3')
        Setting.objects.create(id='username', value='ossportal')
        Setting.objects.create(id='password', value='ossportal1')
        Setting.objects.create(id='project_name', value='admin')
        Setting.objects.create(id='user_domain_name', value='default')
        Setting.objects.create(id='project_domain_id', value='default')
        kcf = api.KeystoneClientFactory()
        connection_settings = kcf.load_settings()
        self.ks_client = kcf.create_client(connection_settings)
         
    
    def test_connection_settings_in_database(self):
        """There must be a set of keystone authorization 
        settings defined in the database.
        """
        self.assertGreaterEqual(len(Setting.objects.all()), 6)
        self.assertIsNotNone(Setting.objects.get(id='auth_url'))
        self.assertIsNotNone(Setting.objects.get(id='username'))
        self.assertIsNotNone(Setting.objects.get(id='password'))
        self.assertIsNotNone(Setting.objects.get(id='project_name'))
        self.assertIsNotNone(Setting.objects.get(id='user_domain_name'))
        self.assertIsNotNone(Setting.objects.get(id='project_domain_id'))
        
    def test_access_to_tenants(self):
        """There must be at least three default tenants in Openstack.
        """
        self.assertGreaterEqual(len(self.ks_client.projects.list()), 3)
        
    def test_create_tenant(self):
        """A new tenant must be created.
        """
        self.ks_client.projects.create(name='test_tenant', domain='default', description='This is a test from oslayer.')
        ten = None
        for t in self.ks_client.projects.list():
            if t.name == 'test_tenant':
                ten = t
                break
            
        self.assertIsNotNone(ten)
        self.ks_client.projects.delete(ten)           
        
        
        
