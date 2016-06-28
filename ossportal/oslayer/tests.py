from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from keystoneauth1.exceptions.http import NotFound

from .models import Setting, User, Company, AccessLevel
from openstack import api
from oslayer.services import user, company

class OpenStackTests(TestCase):
    ks_client = None
    test_user_name = None
    
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
        Setting.objects.create(id=api.DEFAULT_PROJECT_ID_SETTING, value='cbe14fdacc844d74a21d6d8a73c3d4cb')
        Setting.objects.create(id=api.DEFAULT_PASSWORD_SETTING, value='123456')
        kcf = api.KeystoneClientFactory()
        connection_settings = kcf.load_settings()
        self.ks_client = kcf.create_client(connection_settings)
        
        AccessLevel.objects.create(name='basic')
        Setting.objects.create(id=api.DEFAULT_ACCESS_LEVEL, value='basic')
        
        self.test_user_name = 'test_user6943237'
         
    
    def test_connection_settings_in_database(self):
        """There must be a set of KeyStone authorization 
        settings defined in the database.
        """
        self.assertGreaterEqual(len(Setting.objects.all()), 6)
        self.assertIsNotNone(Setting.objects.get(id='auth_url'))
        self.assertIsNotNone(Setting.objects.get(id='username'))
        self.assertIsNotNone(Setting.objects.get(id='password'))
        self.assertIsNotNone(Setting.objects.get(id='project_name'))
        self.assertIsNotNone(Setting.objects.get(id='user_domain_name'))
        self.assertIsNotNone(Setting.objects.get(id='project_domain_id'))
        
    def test_access_to_projects(self):
        """There must be at least three default tenants in OpenStack.
        """
        self.assertGreaterEqual(len(self.ks_client.projects.list()), 3)
        
    def test_create_project(self):
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
        
    def test_create_delete_user(self): 
        """A new user must be created in both OpenStack and local model database and then deleted.
        """          
        fields_data = {
                       'name' : self.test_user_name,
                       'password' : "test password",
                       'email' : self.test_user_name + "@test.com",
                       'description' : 'description for test_user',
                       'enabled' : True,
                       'domain_id' : 'default',
                       'default_project_id' : 'cbe14fdacc844d74a21d6d8a73c3d4cb',
                       'account_main_user' : False
                       }
        # Verify that the local model database is working
        test_user1 = user.add(self.ks_client, fields_data)
        self.assertIsNotNone(test_user1,"User record in local model database must be not null.")
        self.assertIsNotNone(test_user1.external_id, "OpenStack ID must be not null.")
        
        # Verify that the KeyStone client is working
        test_ks_user = self.ks_client.users.get(test_user1.external_id)
        self.assertIsNotNone(test_ks_user, "OpenStack user must be not null.")
        external_id = test_user1.external_id
        
        # Delete the created user
        user.delete(self.ks_client, test_user1.id)
        
        # Verify that the local model database is working
        self.assertRaises(ObjectDoesNotExist, User.objects.get, id=test_user1.id)

        # Verify that the KeyStone client is working
        self.assertRaises(NotFound, self.ks_client.users.get, external_id)
        
    def test_create_company(self):
        """A new company must be created and deleted in both local model database and OpenStack.
        """
        fields_data = {
                    'name' : self.test_user_name,
                    'email' : self.test_user_name + '@test.com',
                    'description' : 'description for ' + self.test_user_name ,
                    'enabled' : True,
                    'active' : True,
                    'account_main_user' : True,
                    'contact_address' : 'test address',
                    'billing_contact_name' : 'bill',
                    'billing_contact_email' : 'bill@test.com',
                    'billing_contact_phone' : '12345',
                    'technical_contact_name' : 'tech',
                    'technical_contact_email' : 'tech@test.com'                       
                    }
        new_company = company.add(self.ks_client, fields_data)
        
        # Verify that the local model database is working
        self.assertIsNotNone(new_company,"Company record in local model database must be not null.")
        new_user = new_company.created_by
        self.assertIsNotNone(new_user, "Company must have a valid companion user.")
        self.assertEqual(new_user.account_main_user, True, "The user must be the account main user.")
        
        # Verify that the KeyStone client is working
        found_domains = self.ks_client.domains.list(name=self.test_user_name)
        self.assertEqual(len(found_domains), 1, "A domain must be created in OpenStack alongside every company created in the local model database.")
        
        # Delete the created user
        # Verify that the user cannot be deleted when it is the account main user
        self.assertRaises(user.IllegalDeletion, user.delete, self.ks_client, new_user.id)
        new_user.account_main_user = False
        new_user.save()
        # Verify that the user cannot be deleted as long as it is referenced by a company
        self.assertRaises(user.IllegalDeletion, user.delete, self.ks_client, new_user.id)
        
        default_user = User.objects.create(name='default_user', email='default_user@test.com'
                                           , created_on=timezone.now())
        new_company.created_by = default_user
        new_company.save()
        user.delete(self.ks_client, new_user.id)
        default_user.delete()
        
        # Delete the created company
        self.ks_client.domains.update(found_domains[0].id,enabled=False)
        self.ks_client.domains.delete(found_domains[0].id)
        new_company.delete()
        
        # Verify that the local model database is working
        found_users = User.objects.filter(name=self.test_user_name)
        self.assertEqual(len(found_users), 0, "A user created must be deleted from the local model database.")
        
        found_companies = Company.objects.filter(name=self.test_user_name)
        self.assertEqual(len(found_companies), 0, "A company created must be deleted from the local model database.")         
        
        # Verify that the KeyStone client is working
        found_domains = self.ks_client.domains.list(name=self.test_user_name)
        self.assertEqual(len(found_companies), 0, "A domain created must be deleted from OpenStack.")
        found_users = self.ks_client.users.list(name=self.test_user_name)
        self.assertEqual(len(found_users), 0, "A user created must be deleted from OpenStack.")

   
