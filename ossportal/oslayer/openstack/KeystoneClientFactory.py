from keystoneauth1.identity import v3
from keystoneauth1 import session
from keystoneclient.v3 import client
from keystoneauth1.exceptions.http import Unauthorized

class KeystoneClientFactory:
    """Factory for OpenStack Keystone Authentication client."""
    sess = None
        
    def __init__(self):
        
        auth = v3.Password(auth_url='http://192.168.1.58:5000/v3',
                            username='ossportal', 
                            password='ossportal1', 
                            project_name='admin',
                            user_domain_name='default',
                            project_domain_id='default')
        self.sess = session.Session(auth=auth)
        
    def create_client(self):
        """Creates the new keystone client."""
        keystoneClient = client.Client(session=self.sess)
        
        try:
            headers = keystoneClient.session.get_auth_headers()  # @UnusedVariable
        except Unauthorized, Argument: 
            keystoneClient = None
            raise "Authentication failed", Argument
        
        return keystoneClient