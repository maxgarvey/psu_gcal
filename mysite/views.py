'''psu_gcal/mysite/psu_gcal/views.py'''

import sys
sys.path.append("/home/maxgarvey/projects/psu_gcal/live_version/mysite")

from django.shortcuts import render_to_response 
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, Context, loader
from django.contrib.auth.decorators import login_required
from my_forms import CalendarForm, GroupForm, AliasForm
try:
    from psugle.calresource import CalendarResource
    from psugle.group import Group
    from psugle.creds import google, group, calendar
except:
    from mysite.psugle.calresource import CalendarResource
    from mysite.psugle.group import Group
    from mysite.psugle.creds import google, group, calendar
from support.calendar_util import calendar_validate, calendar_already_owner, \
process_calendar, calendar_process_requestor, calendar_process_form
from support.general_util import requestor_validate
from support.group_util import group_validate, group_already_owner, \
process_group, group_process_requestor
from support.alias_util import create_alias

#for debug
import logging
__logger__ = logging.getLogger(__name__)

@login_required
def index(request):
    '''this is the index method, it serves and handles the calendar creation
    owner addition functionality'''
    #check for correct permission
    if not request.user.has_perm('mysite.psu_gcal'):
        return render_to_response('invalid.html')
    else:
        #check if form submitted
        if not request.method == 'POST':
            #if the user wants the calendar form
            if request.path == '/calendar_form/':
                calendar_form = CalendarForm()
                template = loader.get_template("calendar_form.html")
                context = Context()
                return render_to_response('calendar_form.html', {'calendar_form': calendar_form}, context_instance=RequestContext(request))
            #if the user wants the group form
            elif request.path == '/group_form/':
                group_form = GroupForm()
                template = loader.get_template("group_form.html")
                context = Context()
                return render_to_response('group_form.html', {'group_form': group_form}, context_instance=RequestContext(request))
            #no more alias form... handled with the other alias create scripts
            #alias_form = AliasForm()

            #the generic case
            else:
                template = loader.get_template( 'index.html' )
                context = Context()
                return render_to_response( 'index.html', {},
                    context_instance=RequestContext(request)  )

        #if it's the calendar form that they submitted
        elif (u'calendar_name' in request.POST.keys()):
            form = CalendarForm( request.POST )
            #check if form valid
            if not form.is_valid():
                return HttpResponse("form not valid...")
            #handle form submission
            else:
                calendar_name, calendar_requestor_1, calendar_requestor_2 = \
                    calendar_process_form(form)
                print 'calendar_name: {0}'.format(calendar_name)#debug
                print 'calendar_requestor_1: {0}'.format(calendar_requestor_1)#debug
                print 'calendar_requestor_2: {0}'.format(calendar_requestor_2)#debug
                try:
                    #client = CalendarResource( google.keys()[0] )
                    client = CalendarResource(domain=calendar.keys()[0],adminuser=calendar[calendar.keys()[0]]['adminuser'],password=calendar[calendar.keys()[0]]['password'])
                    print 'client: {0}'.format(client)#debug
                    #print str(client) #debug
                    try:
                        calendar_already_exists, success, acl = \
                            calendar_validate( calendar_name, client )
                        __logger__.info('calendar_already_exists: '+str(calendar_already_exists)+'\nsuccess: '+str(success)+'\nclient: '+str(client)) #debug
                    except Exception, err:
                        __logger__.info('err: '+str(err)) #debug

                    #create success message
                    response = process_calendar( 
                            calendar_name, calendar_already_exists, success )
                    __logger__.info('response: '+response) #debug
                    if calendar_requestor_1:
                        if requestor_validate( calendar_requestor_1, client ):
                            requestor_1_already_owner = calendar_already_owner(
                                calendar_requestor_1, 
                                acl, 
                                client )

                            response += calendar_process_requestor(
                                calendar_requestor_1, 
                                calendar_name, 
                                requestor_1_already_owner, 
                                client )
                        else:
                            response += '\n<br/>' + calendar_requestor_1 + \
                                ' is not a valid user'

                    if calendar_requestor_2:
                        if requestor_validate( calendar_requestor_2, client ):
                            requestor_2_already_owner = calendar_already_owner(
                                calendar_requestor_2,
                                acl,
                                client )

                            response += calendar_process_requestor(
                                calendar_requestor_2, 
                                calendar_name, 
                                requestor_2_already_owner, 
                                client )
                        else:
                            response += '\n<br/>' + calendar_requestor_2 + \
                                ' is not a valid user'

                    __logger__.info('user: ' + str(request.user) + \
                        ' has made the following request:\n' + str(response) + \
                        '\n')
                    #return HttpResponse( response )

                    template = loader.get_template("success.html")
                    context = Context()
                    return render_to_response('success.html', {'success_msg': response}, context_instance=RequestContext(request))

                except Exception, err:
                    response = str(err)
                    response += '\n<br/>calendar name: ' + str(calendar_name)
                    response += '\n<br/>requestor_1: ' + str(calendar_requestor_1)
                    response += '\n<br/>requestor_2: ' + str(calendar_requestor_2)
                    template = loader.get_template("success.html")
                    context = Context()
                    return render_to_response('success.html', {'success_msg': response}, context_instance=RequestContext(request))
                    #return HttpResponse( response )'''

        #if its the groups form that was submitted
        elif (u'group_name' in request.POST.keys()):
            form = GroupForm( request.POST )
            #check if form valid
            if not form.is_valid():
                return HttpResponse("form not valid...")
            #handle form submission
            else:
                group_name = form.cleaned_data['group_name']
                group_description = form.cleaned_data['group_description']
                group_requestor_1 = form.cleaned_data['group_requestor_1']
                group_requestor_2 = form.cleaned_data['group_requestor_2']

                try:
                    #client = Group( google.keys()[0] )
                    client = Group(domain=group.keys()[0],adminuser=group[group.keys()[0]]['adminuser'],password=group[group.keys()[0]]['password'])
                    group_already_exists, success = group_validate( 
                    group_name, group_description, client )

                    #create success message
                    response = process_group( 
                        group_name, group_description, 
                        group_already_exists, success )

                    if group_requestor_1:
                        try:
                            if requestor_validate( group_requestor_1, client ):
                                requestor_1_already_owner = group_already_owner(
                                    group_requestor_1, 
                                    group_name, 
                                    client )

                                response += group_process_requestor(
                                    group_requestor_1, 
                                    group_name, 
                                    requestor_1_already_owner, 
                                    client )
                            else:
                                response += '\n<br/>' + group_requestor_1 + \
                                    ' is not a valid user'
                        except Exception, err:
                            response += '\n<br/>' + str(err)

                    if group_requestor_2:
                        try:
                            if requestor_validate( group_requestor_2, client ):
                                requestor_2_already_owner = group_already_owner(
                                    group_requestor_2,
                                    group_name,
                                    client )

                                response += group_process_requestor(
                                    group_requestor_2, 
                                    group_name, 
                                    requestor_2_already_owner, 
                                    client )
                            else:
                                response += '\n<br/>' + group_requestor_2 + \
                                    ' is not a valid user'
                        except Exception, err:
                            response += '\n<br/>' + str(err)

                    __logger__.info('user: ' + str(request.user) + \
                        ' has made the following request:\n' \
                        + str(response) + '\n')

                    template = loader.get_template("success.html")
                    context = Context()
                    return render_to_response('success.html', {'success_msg': response}, context_instance=RequestContext(request))
                    #return HttpResponse( response )

                except Exception, err:
                    response = str(err)
                    response += '\n<br/>There was an error.'
                    response += '\n<br/>group name: '  +             str(group_name)
                    response += '\n<br/>description:'  +      str(group_description)
                    response += '\n<br/>requestor 1: ' +      str(group_requestor_1)
                    response += '\n<br/>requestor 2: ' +      str(group_requestor_2)
                    template = loader.get_template("success.html")
                    context = Context()
                    return render_to_response('success.html', {'success_msg': response}, context_instance=RequestContext(request))
