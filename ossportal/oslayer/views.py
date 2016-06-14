from django.http import HttpResponse
from django.shortcuts import render

from openstack import api
from inspect import Arguments
# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the oslayer index.")

def tenants(request):
    """Lists current tenants available in OpenSTack."""
    try:
        kcf = api.KeystoneClientFactory()
        kc = kcf.create_client()
    except Exception, Arguments:
        return HttpResponse("Error: %s".format(Arguments))
    else:
        
        return render(request, 'oslayer/tenants.html', {'tenants_list': kc.projects.list()})
        
def tenant_detail(request, tenant_id):
    """Shows details for a given tenant id"""    
    
    try:
        kcf = api.KeystoneClientFactory()
        kc = kcf.create_client()
    except Exception, Arguments:
        return HttpResponse("Error: %s".format(Arguments))
    else:
        return render(request, 'oslayer/tenant_detail.html', {'tenant': kc.projects.get(tenant_id)})
    