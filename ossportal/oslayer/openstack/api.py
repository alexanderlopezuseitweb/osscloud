from keystoneauth1.identity import v3
from keystoneauth1 import session
from keystoneclient.v3 import client
from keystoneauth1.exceptions.http import Unauthorized

from oslayer.models import Setting

class KeystoneClientFactory:
    """Factory for OpenStack Keystone Authentication client."""
    sess = None
        
    def __init__(self):
        """Sets authorization credentials to start a new session as admin user in Openstack Keystone."""
        # Load connection credentials from settings database  
        cs = self.__loadSettings__()
        auth = v3.Password(auth_url=cs['auth_url'],
                            username=cs['username'], 
                            password=cs['password'], 
                            project_name=cs['project_name'],
                            user_domain_name=cs['user_domain_name'],
                            project_domain_id=cs['project_domain_id'])
        # Set session with authorization credentials 
        self.sess = session.Session(auth=auth)
        
    def create_client(self):
        """Creates the new keystone client."""
        # Set Keystone client based on session
        keystoneClient = client.Client(session=self.sess)
        # Validate that the Keystone client is working.
        try:
            headers = keystoneClient.session.get_auth_headers()  # @UnusedVariable
        except Unauthorized, Argument: 
            keystoneClient = None
            raise "Authentication failed", Argument
        
        return keystoneClient
    
    def __loadSettings__(self):
        """Loads settings values from database."""
        # Define settings values with configuration from database
        connection_settings = {'auth_url':Setting.objects.get(id='auth_url').value,
                            'username':Setting.objects.get(id='username').value, 
                            'password':Setting.objects.get(id='password').value, 
                            'project_name':Setting.objects.get(id='project_name').value,
                            'user_domain_name':Setting.objects.get(id='user_domain_name').value,
                            'project_domain_id':Setting.objects.get(id='project_domain_id').value}
        return connection_settings