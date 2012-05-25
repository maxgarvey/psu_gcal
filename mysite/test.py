'''/psu_gcal/mysite/test.py'''

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
from nose.tools import with_setup

#@with_setup(initialize_cals, cleanup_cals)
class calendar_test:
    '''test class for calendar operations'''
    def __init__(self):
        '''init the client obj and the new cal's name to null'''
        self.client = None
        self.cal_name = ''

    def setUp(self):
        '''set the client obj to a new client, and set the cal name to the name we\'re using'''
        self.client = CalendarResource('gtest.pdx.edu')
        self.cal_name = 'new_cal_name'

    def tearDown(self):
        '''delete the newly created calendar object as well as the client we were using'''
        try:
            self.client.g_res_client.delete_resource(md5('new_cal_name').hexdigest())
        except:
            print 'error deleting the cal with name "new_cal_name"'
        del self.client

    def test_calendar_validate_existing(self):
        '''this function tests running calendar_validate on a known existing 
        calendar'''
        calendar_already_exists, success, acl = \
            calendar_validate('abc_calendar', self.client)
        assert (calendar_already_exists == True)
        assert (success == False)
        assert (len(acl)>0)

    def test_calendar_validate_new(self):
        '''this function tests running calendar_validate on a new calendar'''
        calendar_already_exists, success, acl = \
            calendar_validate(self.cal_name, self.client)
        assert (calendar_already_exists == False)
        assert (success == True)
        assert ((len(acl)==2) or (len(acl)==0))

    def test_calendar_already_owner_true(self):
        '''this function tests running calendar_already_owner on a calendar where we
        know that the given user is already an owner'''
        _, _, acl = calendar_validate('abc_calendar', self.client)
        owner_already = calendar_already_owner('magarvey', acl, self.client)
        assert owner_already

    def test_calendar_already_owner_false(self):
        '''this function tests running calendar_already_owner on a calendar where we
        know that the given user is not already an owner'''
        _, _, acl = calendar_validate('abc_calendar', self.client)
        owner_already = calendar_already_owner('phony_phony_phony', acl, self.client)
        assert (owner_already == False)

    def test_process_calendar_existing(self):
        '''this function tests running the process_calendar method on a known
        existing calendar'''
        response = process_calendar('calendar_name', True, False)
        assert (response == 'calendar_name (existing calendar)')

    def test_process_calendar_new(self):
        '''this function tests running the process_calendar method on a new
        calendar'''
        response = process_calendar('calendar_name', False, True)
        assert (response == 'calendar_name (new calendar)')

    def test_process_calendar_error(self):
        '''this function tests running the process_calendar method on invalid
        input; indicating failure to create calendar'''
        response = process_calendar('calendar_name', False, False)
        assert (response == 'could not make calendar: calendar_name')

    def test_process_reqiuestor_existing(self):
        '''this function tests the calendar_process_requestor method on a requestor
        that is already the owner of the calendar'''
        response = calendar_process_requestor('magarvey',
            'abc_calendar',
            True,
            self.client)
        assert (response == '\n<br/>magarvey (already owner)')

    def test_calendar_process_requestor_new(self):
        '''this function tests the calendar_process_requestor method on a requestor
        that is already the owner of the calendar'''
        __a__ = md5()
        __a__.update(str(randint(0, 5000000)))
        user = 'test_user-'+str(__a__.hexdigest())
        response = calendar_process_requestor(user, 'abc_calendar', False, self.client)
        assert (response == '\n<br/>' + user + ' (new owner)')

    def test_calendar_process_requestor_invalid(self):
        '''this function tests the calendar_process_requestor method on a requestor with
        some invalid chars in the requestor's name (... to trigger the exception)'''
        response = calendar_process_requestor('', 'abc_calendar', False, self.client)
        assert (response.startswith('\n<br/> is invalid user'))

    def test_calendar_add_owner_existing(self):
        '''this function tests the calendar_add_owner method on a calendar that the user
        is already owner of'''
        calendar_already_exists, success, acl = \
            calendar_validate('abc_calendar', self.client)
        calendar_already_owner_start = calendar_already_owner('magarvey', acl, self.client)
        try:
            calendar_add_owner('magarvey', 'abc_calendar', self.client)
            calendar_add_owner_success = True
        except:
            calendar_add_owner_success = False
        assert calendar_already_exists
        assert calendar_already_owner_start
        assert (success == False)
        assert (calendar_add_owner_success == False)

    def test_calendar_add_owner_invalid(self):
        '''this function tests the calendar_add_owner method on a user that is not in the
        gtest.pdx.edu system'''
        calendar_already_exists, success, acl = \
            calendar_validate('abc_calendar', self.client)
        calendar_already_owner_start = calendar_already_owner('?//%/$/#@', acl, self.client)
        try:
            calendar_add_owner('?//%/$/#@', 'abc_calendar', self.client)
            calendar_add_owner_success = True
        except:
            calendar_add_owner_success = False
        assert calendar_already_exists
        assert (calendar_already_owner_start == False)
        assert (success == False)
        assert (calendar_add_owner_success == False)

    def test_calendar_add_owner_new(self):
        '''this function tests the calendar_add_owner method for a valid user not already
        owner of the calendar'''
        self.client.create(self.cal_name)
        calendar_already_exists, success, acl = \
            calendar_validate(self.cal_name, self.client)
        calendar_already_owner_start = calendar_already_owner('magarvey', acl, self.client)
        try:
            calendar_add_owner('magarvey', self.cal_name, self.client)
            calendar_add_owner_success = True
        except Exception, err:
            print err
            calendar_add_owner_success = False
        calendar_already_exists, success, acl = \
            calendar_validate(self.cal_name, self.client)
        calendar_already_owner_end = calendar_already_owner('magarvey', acl, self.client)
        assert calendar_already_exists
        assert (calendar_already_owner_start == False)
        assert (success == False)
        assert calendar_add_owner_success
        assert calendar_already_owner_end

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

    def test_calendar_process_form(self):
        '''this function tests the process form function... just make sure
        it gets the right stuff from an object with the same contents
        as the one we're dealing with'''
        this_form = self.Form()
        calendar_name, requestor_1, requestor_2 = calendar_process_form(this_form)
        assert (calendar_name == 'some_cal_name')
        assert (requestor_1 == 'some_cal_user')
        assert (requestor_2 == 'other_cal_user')

class group_test:
    '''test class for groups'''
    def __init__(self):
        '''init client and group_name to none'''
        self.client = None
        self.group_name = None

    def setUp(self):
        '''set up the group client and set the group name'''
        self.client = Group('gtest.pdx.edu')
        self.group_name = 'new_test_group'

    def tearDown(self):
        '''delete the newly created test group and the client object'''
        try:
            self.client.delete(group_name='new_test_group')
        except:
            print "error deleting group: 'new_test_group'"
        del self.client

    def test_group_validate_existing(self):
        '''this function tests running group_validate on a known existing 
        group'''
        group_already_exists, success = \
            group_validate('abc_group', '', self.client)
        assert (group_already_exists == True)
        assert (success == False)

    def test_group_validate_new(self):
        '''this function tests running calendar_validate on a new calendar'''
        group_already_exists, success = \
            group_validate(self.group_name, '',  self.client)
        assert (group_already_exists == False)
        assert (success == True)

    def test_group_already_owner_true(self):
        '''this function tests running group_already_owner on a group where we
        know that the given user is already an owner'''
        owner_already = group_already_owner('magarvey', 'abc_group', self.client)
        assert owner_already

    def test_group_already_owner_false(self):
        '''this function tests running group_already_owner on a group where we
        know that the given user is not already an owner'''
        owner_already = group_already_owner('phony_phony_phony', 'abc_group', self.client)
        assert (owner_already == False)

    def test_process_group_existing(self):
        '''this function tests running the process_group method on a known
        existing group'''
        response = process_group('group_name', '', True, False)
	meaningful_response = response.split('\n')[0]
	print meaningful_response
        assert (meaningful_response == 'group name: group_name (existing group)')

    def test_process_group_new(self):
        '''this function tests running the process_group method on a new
        group'''
        response = process_group('group_name', '', False, True)
	meaningful_response = response.split('\n')[0]
	print meaningful_response
        assert (meaningful_response ==  'group name: group_name (new group)')

    def test_process_group_error(self):
        '''this function tests running the process_group method on invalid
        input; indicating failure to create group'''
        response = process_group('group_name', '', False, False)
	meaningful_response = response.split('\n')[0]
	print meaningful_response
        assert (meaningful_response == 'could not make group: group_name')

    def test_group_process_reqiuestor_existing(self):
        '''this function tests the group_process_requestor method on a requestor
        that is already the owner of the calendar'''
        response = group_process_requestor('magarvey',
            'abc_group',
            True,
            self.client)
        assert (response == '\n<br/>magarvey (already owner)')

    def test_group_process_requestor_new(self):
        '''this function tests the calendar_process_requestor method on a requestor
        that is not already the owner of the calendar'''
        self.client.create(self.group_name)
        response = group_process_requestor('magarvey', self.group_name, False, self.client)
        print response
        assert (response == '\n<br/>magarvey (new owner)')

    def test_group_process_requestor_invalid(self):
        '''this function tests the group_process_requestor method on a requestor with
        some invalid chars in the requestor's name (... to trigger the exception)'''
        response = group_process_requestor('', 'abc_group', False, self.client)
        assert (response.startswith('\n<br/> is invalid user'))

    def test_group_add_owner_existing(self):
        '''this function tests the group_add_owner method on a group that the user
        is already owner of'''
        group_already_exists, success = \
            group_validate('abc_calendar', '', self.client)
        group_already_owner_start = group_already_owner('magarvey', 'abc_group', self.client)
        try:
            group_add_owner('magarvey', 'abc_group', self.client)
            group_add_owner_success = True
        except:
            group_add_owner_success = False
        group_already_owner_end = group_already_owner('magarvey','abc_group',self.client)
        assert group_already_exists
        assert group_already_owner_start
        assert group_already_owner_end
        assert (success == False)
        assert (group_add_owner_success == True)

    def test_group_add_owner_invalid(self):
        '''this function tests the group_add_owner method on a user that is not in the
        gtest.pdx.edu system'''
        group_already_exists, success = \
            group_validate('abc_group', '', self.client)
        try:
            group_already_owner_start = group_already_owner('?//%/$/#@', 'abc_group', self.client)
        except:
            group_already_owner_start = False
        try:
            subscribed, owner = group_add_owner('?//%/$/#@', 'abc_group', self.client)
            group_add_owner_success = True
        except:
            group_add_owner_success = False
        assert group_already_exists
        assert (group_already_owner_start == False)
        assert (success == False)
        assert (group_add_owner_success == True)
        assert (subscribed == False)
        assert (owner == False)

    def test_group_add_owner_new(self):
        '''this function tests the group_add_owner method for a valid user not already
        owner of the group'''
        self.client.create(self.group_name)
        group_already_exists, success = \
            group_validate(self.group_name, '', self.client)
        group_already_owner_start = group_already_owner('magarvey', self.group_name, self.client)
        try:
            subscribed, owner = group_add_owner('magarvey', self.group_name, self.client)
            group_add_owner_success = True
        except:
            group_add_owner_success = False
        group_already_exists, success = \
            group_validate(self.group_name, '', self.client)

        sleep(5)
        group_already_owner_end = group_already_owner('magarvey', self.group_name, self.client)

        '''DEBUGGIN'''
        print str(self.client.status(self.group_name))
        print str(group_already_owner('magarvey',self.group_name,self.client))

        assert group_already_exists
        assert (group_already_owner_start == False)
        assert (success == False)
        assert group_add_owner_success
        assert subscribed
        assert owner
        assert group_already_owner_end
