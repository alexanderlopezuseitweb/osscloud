from keystoneauth1.identity import v3
from keystoneauth1 import session
from keystoneclient.v3 import client
from keystoneauth1.exceptions.http import Unauthorized

class OpenStackClient:

    keystoneClient = None
    
    def __init__(self):
        
        auth = v3.Password(auth_url='http://192.168.1.58:5000/v3',
                            username='ossportal', 
                            password='ossportal1', 
                            project_name='admin',
                            user_domain_name='default',
                            project_domain_id='default')
        sess = session.Session(auth=auth)
        self.keystoneClient = client.Client(session=sess)
        
        try:
            headers = self.keystoneClient.session.get_auth_headers()
        except Unauthorized, Argument: 
            self.keystoneClient = None
            raise "Authentication failed", Argument


try:
    osc = OpenStackClient()
except Exception, Argument:
    print "Error with OpenTsackClient: ", Argument
else:
    print "Athentication passed" 
    projects = osc.keystoneClient.projects.list()
    for p in projects:
        print p.name + ':' + p.description 