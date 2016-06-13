#from django.shortcuts import render
from django.http import HttpResponse

from openstack import KeystoneClientFactory
from inspect import Arguments
# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the oslayer index.")

def projects(request):
    kcf = KeystoneClientFactory()
    kc = kcf.create_client()
    return HttpResponse("Projects: ", kc.projects.list())
    
#     try:
#         kc = KeystoneClientFactory()
#     except Exception, Arguments:
#         return HttpResponse("Error: %s".format(Arguments))
#     else:
#         return HttpResponse("Projects: ", kc.projects.list())
#         for p in kc.projects.list():
#             print p.name + ':' + p.description
    
    