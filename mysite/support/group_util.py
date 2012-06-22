'''/psu_gcal/mysite/psu_gcal/support/group_util.py'''

from psugle.user import User
from subprocess import call
import sys
import os

def group_validate( group_name, group_description, client ):
    '''this function takes a group name and a client object and returns
    a boo telling whether the group exists, and a boo if we're successful in
    creating a new group if it doesn't.'''
    #does cal with name == calendar_name already exist?
    group_already_exists = False
    group_status = client.status(group_name)
    if group_status['exists']:
        group_already_exists = True

    #if not existing, create new. successful create?
    success = False
    if not group_already_exists:
        try:
            client.create( group_name=group_name, description=group_description )
            success = True
        except:
            pass

    if success:
        try:
            #print 'os.getcwd(): {0}'.format(os.getcwd()) #debug
            #print 'sys.path: {0}'.format(sys.path) #debug
            #print 'os.listdir(os.getcwd()): {0}'.format(os.listdir(os.getcwd())) #debugi
            print '"{0}@pdx.edu".format(group_name): '+"{0}@pdx.edu".format(group_name) #debug
            call(['/var/www/env/bin/python2.6','/var/www/psu_gcal/gam.py','update','group',"{0}@pdx.edu".format(group_name),'settings','is_archived','True'])
        except Exception, err:
            print 'Error: {}'.format(err)

    return group_already_exists, success

def group_already_owner( requestor, group_name, client ):
    '''this function takes a requestor name a group name and a client and returns
    a boolean as to whether the requestor is already an owner'''
    return client.g_client.IsOwner(owner_email=requestor+'@'+client.domain, group_id=group_name+'@'+client.domain)

def process_group( group_name, group_description,  group_already_exists, success ):
    '''this function generates the part of the success message dealing with
    the group'''
    response = 'group name: ' + group_name
    if success:
        response += ' (new group)'
    elif group_already_exists:
        response += ' (existing group)'
    else:
        response =  'could not make group: ' + group_name
    response += '\n<br/>group description: ' + group_description
    return response

def group_process_requestor( requestor_name, group_name, already_owner, client ):
    '''this function generates the part of the success message dealing with
    a requestor'''
    response = '\n<br/>'+requestor_name
    if already_owner:
        response += ' (already owner)'
    else:
        try:
            subscribed, owner = group_add_owner(requestor_name, group_name, client)
            if owner:
                response += ' (new owner)'
            else:
                response += ' is invalid user'
        except Exception, err:
            response += ' is invalid user'
    return response

def group_add_owner( requestor_name, group_name, client ):
    '''this method adds a new owner to a group'''
    try:
        client.subscribe(group_name=group_name, user_name=requestor_name)
        subscribed = True
    except:
        subscribed = False
    try:
        client.make_owner(group_name=group_name, user_name=requestor_name)
        owner = True
    except:
        owner = False
    return subscribed, owner

def group_process_form( form ):
    '''this method gets the different fields from the calendar form'''
    return form.cleaned_data['group_email'], form.cleaned_data['group_name'], form.cleaned_data['group_description'], form.cleaned_data['group_requestor_1'], form.cleaned_data['group_requestor_2']
