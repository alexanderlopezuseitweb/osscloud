from keystoneauth1.identity import v3
from keystoneauth1 import session
from keystoneclient.v3 import client
from keystoneauth1.exceptions.http import Unauthorized

from oslayer.models import Setting

SESSION_KEYWORD = 'keystone_session'
"""str: keyword to store and retrieve the Keystone connection 
settings dictionary from Django session.
"""
DEFAULT_PASSWORD_SETTING = 'default_password'
"""str: keyword to retrieve the default password for new users 
created automatically.
"""
DEFAULT_PROJECT_ID_SETTING = 'default_project_id'
"""str: keyword to retrive the id of the default project for new
users created automatically.
"""
DEFAULT_ACCESS_LEVEL = 'default_access_level'
"""str: keyword to retrieve the name of the default access level 
for new companies.
"""

class KeystoneClientFactory:
    """Factory for OpenStack Keystone Authentication client.
    """
    
    def __init__(self):
        """Sets authorization credentials to start a new session as admin user in Openstack Keystone.
        """
        pass
        
    def create_client(self, connection_settings):
        """Creates the new keystone client.
        
        Args:
            connection_settings (dict): Connection settings from the database.
        Returns:
            Keystone client
        """
        # Load connection credentials from settings database  
        auth = v3.Password(auth_url=connection_settings['auth_url'],
                            username=connection_settings['username'], 
                            password=connection_settings['password'], 
                            project_name=connection_settings['project_name'],
                            user_domain_name=connection_settings['user_domain_name'],
                            project_domain_id=connection_settings['project_domain_id'])
        # Set session with authorization credentials 
        keystone_session = session.Session(auth=auth)
        # Set Keystone client based on session
        keystoneClient = client.Client(session=keystone_session)
        # Validate that the Keystone client is working.
        try:
            headers = keystoneClient.session.get_auth_headers()  # @UnusedVariable
        except Unauthorized, ex: 
            keystoneClient = None
            raise "Authentication failed: " + str(ex)
        
        return keystoneClient
    
    def load_settings(self):
        """Loads settings values from database.
        
        Args:
        
        Returns:
            Dictionary with the connection settings from the database
        """
        # Define settings values with configuration from database
        connection_settings = {'auth_url':Setting.objects.get(id='auth_url').value,
                            'username':Setting.objects.get(id='username').value, 
                            'password':Setting.objects.get(id='password').value, 
                            'project_name':Setting.objects.get(id='project_name').value,
                            'user_domain_name':Setting.objects.get(id='user_domain_name').value,
                            'project_domain_id':Setting.objects.get(id='project_domain_id').value}
        return connection_settings
    
def get_setting(setting_key):
    """Gets the setting value of _setting_key_ from the database.
    
    Args:
        setting_key: (str) Key of the setting stored in the database.
    Returns:
        value (str) recovered from the database for the given setting key.
    """
    return Setting.objects.get(id=setting_key).value