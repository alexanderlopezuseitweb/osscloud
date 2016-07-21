import sys
from jira.client import JIRA 
from oslayer.models import Setting
def admin_connect_to_jira():
    
    user = Setting.objects.get(id='user_atlassian').value
    pw = Setting.objects.get(id='pass_atlassian').value
    jira_options = { 'server': Setting.objects.get(id='server_atlassian').value}
    try:
        jira = JIRA(options=jira_options, basic_auth=(user,pw))
    except Exception as e:
        jira = None
    
    return jira

"""Method for connect with users global
"""
def user_connect_to_jira(user,pw):
    jira_options = { 'server': Setting.objects.get(id='server_atlassian').value}
    try:
        jira = JIRA(options=jira_options, basic_auth=(user,pw))
    except Exception as e:
        jira = None
    
    return jira

def get_server():
    return Setting.objects.get(id='server_atlassian').value

def create_group(name_group):
    jira=admin_connect_to_jira()
    group=jira.add_group(name_group)
    return group

def create_user(username, email):
    jira=admin_connect_to_jira()
    user=jira.add_user(username, email) 
    return user

def add_user_to_group(username, group):
    jira=admin_connect_to_jira()
    res=jira.add_user_to_group(username, group)
    return res
    
    
    