'''/psu_gcal/mysite/psu_gcal/support/calendar_validate.py'''

from psugle.user import User

def calendar_validate( calendar_name, client ):
    '''this function takes a calendar name and a client object and returns
    a boo telling whether the cal exists, and a boo if we're successful in
    creating a new cal if it doesn't. Also, the acl is retrieved'''
    #does cal with name == calendar_name already exist?
    calendar_already_exists = False
    existing_cals = client.get_all_resources()
    for cal in existing_cals:
        if cal['name'] == calendar_name:
            calendar_already_exists = True
            break

    #if not existing, create new. successful create?
    success = False
    if not calendar_already_exists:
        try:
            client.create( name=str(calendar_name) )
            success = True
        except Exception, err:
            success = str(err)
            #pass

    #get acl
    if calendar_already_exists or success:
        try:
            acl = client.get_acl_by_name( calendar_name )
        except:
            acl = []
    else:
        acl = []

    #print 'debug3'
    return calendar_already_exists, success, acl

def calendar_already_owner( requestor, acl, client ):
    '''this function takes a requestor name an acl and a client and returns
    a boolean as to whether the requestor is already an owner'''
    for entry in acl:
        if entry[0] == (requestor+'@'+str( client.domain )):
            return True
    return False

def process_calendar( calendar_name, calendar_already_exists, success ):
    '''this function generates the part of the success message dealing with
    the calendar'''
    response = calendar_name
    if success:
        response += ' (new calendar)'
    elif calendar_already_exists:
        response += ' (existing calendar)'
    else:
        response =  'could not make calendar: '+calendar_name
    return response

def calendar_process_requestor( requestor_name, calendar_name, already_owner, client ):
    '''this function generates the part of the success message dealing with
    a requestor'''
    response = '\n<br/>'+requestor_name
    if already_owner:
        response += ' (already owner)'
    else:
        try:
            calendar_add_owner(requestor_name, calendar_name, client)
            response += ' (new owner)'
        except Exception, err:
            response += ' is invalid user: <br/>&nbsp;&nbsp;&nbsp;'+str(err)
    return response

def calendar_add_owner( requestor_name, calendar_name, client ):
    '''this method adds a new owner to a calendar'''
    client.set_owner_by_name(name=calendar_name,owner=requestor_name)

def calendar_process_form( form ):
    '''this method gets the different fields from the calendar form'''
    #print 'form.cleaned_data: ' + str(form.cleaned_data)
    return form.cleaned_data['calendar_name'], form.cleaned_data['calendar_requestor_1'], form.cleaned_data['calendar_requestor_2']
