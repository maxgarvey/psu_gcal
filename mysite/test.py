'''/psu_gcal/mysite/psu_gcal/test.py'''

import sys
sys.path.append('/var/www/psu_gcal/')
sys.path.append('/var/www/psu_gcal/mysite/')

from support.calendar_util import calendar_validate, calendar_already_owner, \
    process_calendar, calendar_process_requestor, calendar_add_owner, \
    calendar_process_form
from support.group_util import group_validate, group_already_owner, \
    process_group, group_process_requestor, group_add_owner, \
    group_process_form
from psugle.calresource import CalendarResource
from psugle.group import Group
from random import randint
from hashlib import md5
from time import sleep
#from psugle.user import *

#helper functions
def get_client():
    '''this function creates a calendar resource client for our test domain'''
    _cal_client = CalendarResource( 'gtest.pdx.edu' )
    return _cal_client

def del_client( _cal_client ):
    '''this function deletes the calendar resource client we make at the
    start of the tests'''
    del _cal_client

__cal_client__ = get_client()

def test_calendar_validate_existing():
    '''this function tests running calendar_validate on a known existing 
    calendar'''
    calendar_already_exists, success, acl = \
        calendar_validate('abc_calendar', __cal_client__)
    assert (calendar_already_exists == True)
    assert (success == False)
    assert (len(acl)>0)

#this will be the new calendar for this sess. so we can recycle in a sense
__cal_id__ = md5()
__cal_id__.update(str(randint(0, 5000000)))
__cal_name__ = 'cal-'+str(__cal_id__.hexdigest())

def test_calendar_validate_new():
    '''this function tests running calendar_validate on a new calendar'''
    calendar_already_exists, success, acl = \
        calendar_validate(__cal_name__, __cal_client__)
    assert (calendar_already_exists == False)
    assert (success == True)
    assert ((len(acl)==2) or (len(acl)==0))

def test_calendar_already_owner_true():
    '''this function tests running calendar_already_owner on a calendar where we
    know that the given user is already an owner'''
    _, _, acl = calendar_validate('abc_calendar', __cal_client__)
    owner_already = calendar_already_owner('magarvey', acl, __cal_client__)
    assert owner_already

def test_calendar_already_owner_false():
    '''this function tests running calendar_already_owner on a calendar where we
    know that the given user is not already an owner'''
    _, _, acl = calendar_validate('abc_calendar', __cal_client__)
    owner_already = calendar_already_owner('phony_phony_phony', acl, __cal_client__)
    assert (owner_already == False)

def test_process_calendar_existing():
    '''this function tests running the process_calendar method on a known
    existing calendar'''
    response = process_calendar('calendar_name', True, False)
    assert (response == 'calendar_name (existing calendar)')

def test_process_calendar_new():
    '''this function tests running the process_calendar method on a new
    calendar'''
    response = process_calendar('calendar_name', False, True)
    assert (response == 'calendar_name (new calendar)')

def test_process_calendar_error():
    '''this function tests running the process_calendar method on invalid
    input; indicating failure to create calendar'''
    response = process_calendar('calendar_name', False, False)
    assert (response == 'could not make calendar: calendar_name')

def test_process_reqiuestor_existing():
    '''this function tests the calendar_process_requestor method on a requestor
    that is already the owner of the calendar'''
    response = calendar_process_requestor('magarvey',
        'abc_calendar',
        True,
        __cal_client__)
    assert (response == '\n<br/>magarvey (already owner)')

def test_calendar_process_requestor_new():
    '''this function tests the calendar_process_requestor method on a requestor
    that is already the owner of the calendar'''
    __a__ = md5()
    __a__.update(str(randint(0, 5000000)))
    user = 'test_user-'+str(__a__.hexdigest())
    response = calendar_process_requestor(user, 'abc_calendar', False, __cal_client__)
    assert (response == '\n<br/>' + user + ' (new owner)')

def test_calendar_process_requestor_invalid():
    '''this function tests the calendar_process_requestor method on a requestor with
    some invalid chars in the requestor's name (... to trigger the exception)'''
    response = calendar_process_requestor('', 'abc_calendar', False, __cal_client__)
    assert (response.startswith('\n<br/> is invalid user'))

def test_calendar_add_owner_existing():
    '''this function tests the calendar_add_owner method on a calendar that the user
    is already owner of'''
    calendar_already_exists, success, acl = \
        calendar_validate('abc_calendar', __cal_client__)
    calendar_already_owner_start = calendar_already_owner('magarvey', acl, __cal_client__)
    try:
        calendar_add_owner('magarvey', 'abc_calendar', __cal_client__)
        calendar_add_owner_success = True
    except:
        calendar_add_owner_success = False
    assert calendar_already_exists
    assert calendar_already_owner_start
    assert (success == False)
    assert (calendar_add_owner_success == False)

def test_calendar_add_owner_invalid():
    '''this function tests the calendar_add_owner method on a user that is not in the
    gtest.pdx.edu system'''
    calendar_already_exists, success, acl = \
        calendar_validate('abc_calendar', __cal_client__)
    calendar_already_owner_start = calendar_already_owner('?//%/$/#@', acl, __cal_client__)
    try:
        calendar_add_owner('?//%/$/#@', 'abc_calendar', __cal_client__)
        calendar_add_owner_success = True
    except:
        calendar_add_owner_success = False
    assert calendar_already_exists
    assert (calendar_already_owner_start == False)
    assert (success == False)
    assert (calendar_add_owner_success == False)

def test_calendar_add_owner_new():
    '''this function tests the calendar_add_owner method for a valid user not already
    owner of the calendar'''
    calendar_already_exists, success, acl = \
        calendar_validate(__cal_name__, __cal_client__)
    calendar_already_owner_start = calendar_already_owner('magarvey', acl, __cal_client__)
    try:
        calendar_add_owner('magarvey', __cal_name__, __cal_client__)
        calendar_add_owner_success = True
    except:
        calendar_add_owner_success = False
    calendar_already_exists, success, acl = \
        calendar_validate(__cal_name__, __cal_client__)
    calendar_already_owner_end = calendar_already_owner('magarvey', acl, __cal_client__)
    assert calendar_already_exists
    assert (calendar_already_owner_start == False)
    assert (success == False)
    assert calendar_add_owner_success
    assert calendar_already_owner_end


#def test_requestor_validate_valid():
#    '''this function tests the requestor_validate method on a valid user
#    for the domain'''
#    valid = requestor_validate('magarvey', __cal_client__)
#    assert valid

#def test_requestor_validate_invalid():
#    '''this function tests the requestor_validate method on a valid user
#    for the domain'''
#    valid = requestor_validate('phony_phony_phony', __cal_client__)
#    assert (valid == False)

class Form():
    '''a dummy form object for use with test_calendar_process_form function'''
    def __init__(self):
        '''this is the init method for the dummy form object
        we've defined here'''
        self.cleaned_data = {'calendar_name':'some_cal_name',
                'calendar_requestor_1':'some_cal_user',
                'calendar_requestor_2':'other_cal_user'}
    def contents(self):
        '''return the contents of cleaned data'''
        return self.cleaned_data
    def add(self, key, value):
        '''set a key, value pair'''
        self.cleaned_data[key] = value

def test_calendar_process_form():
    '''this function tests the process form function... just make sure
    it gets the right stuff from an object with the same contents
    as the one we're dealing with'''
    this_form = Form()
    calendar_name, requestor_1, requestor_2 = calendar_process_form(this_form)
    assert (calendar_name == 'some_cal_name')
    assert (requestor_1 == 'some_cal_user')
    assert (requestor_2 == 'other_cal_user')

del_client( __cal_client__ )

#some helper methods for the group object
def get_group_client():
    client = Group('gtest.pdx.edu')
    return client

def del_group_client(client):
    del client

__group_client__ = get_group_client()

def test_group_validate_existing():
    '''this function tests running group_validate on a known existing 
    group'''
    group_already_exists, success = \
        group_validate('abc_group', '', __group_client__)
    assert (group_already_exists == True)
    assert (success == False)

#this will be the new calendar for this sess. so we can recycle in a sense
__group_id__ = md5()
__group_id__.update(str(randint(0, 5000000)))
__group_name__ = 'group-'+str(__group_id__.hexdigest())

def test_group_validate_new():
    '''this function tests running calendar_validate on a new calendar'''
    group_already_exists, success = \
        group_validate(__group_name__, '',  __group_client__)
    assert (group_already_exists == False)
    assert (success == True)

def test_group_already_owner_true():
    '''this function tests running group_already_owner on a group where we
    know that the given user is already an owner'''
    owner_already = group_already_owner('magarvey', 'abc_group', __group_client__)
    assert owner_already

def test_group_already_owner_false():
    '''this function tests running group_already_owner on a group where we
    know that the given user is not already an owner'''
    owner_already = group_already_owner('phony_phony_phony', 'abc_group', __group_client__)
    assert (owner_already == False)

def test_process_group_existing():
    '''this function tests running the process_group method on a known
    existing group'''
    response = process_group('group_name', True, False)
    assert (response == 'group_name (existing group)')

def test_process_group_new():
    '''this function tests running the process_group method on a new
    group'''
    response = process_group('group_name', False, True)
    assert (response == 'group_name (new group)')

def test_process_group_error():
    '''this function tests running the process_group method on invalid
    input; indicating failure to create group'''
    response = process_group('group_name', False, False)
    assert (response == 'could not make group: group_name')

def test_group_process_reqiuestor_existing():
    '''this function tests the group_process_requestor method on a requestor
    that is already the owner of the calendar'''
    response = group_process_requestor('magarvey',
        'abc_group',
        True,
        __group_client__)
    assert (response == '\n<br/>magarvey (already owner)')

def test_group_process_requestor_new():
    '''this function tests the calendar_process_requestor method on a requestor
    that is not already the owner of the calendar'''
    #__a__ = md5()
    #__a__.update(str(randint(0, 5000000)))
    #user = 'test_user-'+str(__a__.hexdigest())
    response = group_process_requestor('magarvey', __group_name__, False, __group_client__)
    print response
    assert (response == '\n<br/>magarvey (new owner)')

def test_group_process_requestor_invalid():
    '''this function tests the group_process_requestor method on a requestor with
    some invalid chars in the requestor's name (... to trigger the exception)'''
    response = group_process_requestor('', 'abc_group', False, __group_client__)
    assert (response.startswith('\n<br/> is invalid user'))

def test_group_add_owner_existing():
    '''this function tests the group_add_owner method on a group that the user
    is already owner of'''
    group_already_exists, success = \
        group_validate('abc_calendar', '', __group_client__)
    group_already_owner_start = group_already_owner('magarvey', 'abc_group', __group_client__)
    try:
        group_add_owner('magarvey', 'abc_group', __group_client__)
        group_add_owner_success = True
    except:
        group_add_owner_success = False
    group_already_owner_end = group_already_owner('magarvey','abc_group',__group_client__)
    assert group_already_exists
    assert group_already_owner_start
    assert group_already_owner_end
    assert (success == False)
    assert (group_add_owner_success == True)

def test_group_add_owner_invalid():
    '''this function tests the group_add_owner method on a user that is not in the
    gtest.pdx.edu system'''
    group_already_exists, success = \
        group_validate('abc_group', '', __group_client__)
    try:
        group_already_owner_start = group_already_owner('?//%/$/#@', 'abc_group', __group_client__)
    except:
        group_already_owner_start = False
    try:
        subscribed, owner = group_add_owner('?//%/$/#@', 'abc_group', __group_client__)
        group_add_owner_success = True
    except:
        group_add_owner_success = False
    assert group_already_exists
    assert (group_already_owner_start == False)
    assert (success == False)
    assert (group_add_owner_success == True)
    assert (subscribed == False)
    assert (owner == False)

def test_group_add_owner_new():
    '''this function tests the group_add_owner method for a valid user not already
    owner of the group'''
    __group_id__ = md5()
    __group_id__.update(str(randint(0, 5000000)))
    __group_name__ = 'group-'+str(__group_id__.hexdigest())

    group_already_exists, success = \
        group_validate(__group_name__, '', __group_client__)
    group_already_owner_start = group_already_owner('magarvey', __group_name__, __group_client__)
    try:
        subscribed, owner = group_add_owner('magarvey', __group_name__, __group_client__)
        group_add_owner_success = True
    except:
        group_add_owner_success = False
    group_already_exists, success = \
        group_validate(__group_name__, '', __group_client__)

    sleep(3)
    group_already_owner_end = group_already_owner('magarvey', __group_name__, __group_client__)

    '''DEBUGGIN'''
    print str(__group_client__.status(__group_name__))
    print str(group_already_owner('magarvey',__group_name__,__group_client__))

    assert group_already_exists
    assert (group_already_owner_start == False)
    assert (success == False)
    assert group_add_owner_success
    assert subscribed
    assert owner
    assert group_already_owner_end

del_group_client(__group_client__)
