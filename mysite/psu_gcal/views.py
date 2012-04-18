'''psu_gcal/mysite/psu_gcal/views.py'''

from django.shortcuts import render_to_response 
from django.http import HttpResponse 
from django.template import RequestContext, Context, loader
from django.contrib.auth.decorators import login_required
from my_forms import CalendarForm, GroupForm
from psugle.calresource import CalendarResource
from psugle.group import Group
from support.calendar_util import calendar_validate, calendar_already_owner, \
process_calendar, calendar_process_requestor, calendar_process_form
from support.general_util import requestor_validate
from support.group_util import group_validate, group_already_owner, \
process_group, group_process_requestor

#for debug
import logging
__logger__ = logging.getLogger(__name__)

@login_required
def index(request):
    '''this is the index method, it serves and handles the calendar creation
    owner addition functionality'''
    #check for correct permission
    if not request.user.has_perm('psu_gcal.psu_gcal'):
        return render_to_response('invalid.html')
    else:
        #check if form submitted
        if not request.method == 'POST':
            calendar_form = CalendarForm()
            group_form = GroupForm()
            template = loader.get_template( 'index.html' )
            context = Context()
            return render_to_response( 'index.html',
                    { 'calendar_form':calendar_form, 'group_form':group_form },
                    context_instance=RequestContext(request)  )

        #else: #debug debug debug
        #    print str(request.POST.keys())
        #    print (u'calendar_name' in request.POST.keys())

        #if it's the calendar form that they submitted
        elif (u'calendar_name' in request.POST.keys()):
            form = CalendarForm( request.POST )
            #check if form valid
            if not form.is_valid():
                return HttpResponse("form not valid...")
            #handle form submission
            else:
                #print 'form.cleaned_data: ' + str( form.cleaned_data ) #debug
                #calendar_name = form.cleaned_data['calendar_name']
                #calendar_requestor_1 = form.cleaned_data['calendar_requestor_1']
                #calendar_requestor_2 = form.cleaned_data['calendar_requestor_2']
                #print 'request.post: ' + str(request.POST)
                calendar_name, calendar_requestor_1, calendar_requestor_2 = \
                    calendar_process_form(form)
                #print 'calendar_name: '+str(calendar_name)+' calendar_requestor_1:'+str(calendar_requestor_1)+\
                #    'calendar_requestor_2: '+str(calendar_requestor_2)
                try:
                    client = CalendarResource( 'gtest.pdx.edu' )
                    #print str(client) #debug
                    try:
                        calendar_already_exists, success, acl = calendar_validate( 
                        calendar_name, client )
                    except Exception, err:
                        print err

                    #print 'cal already exists: '+str(calendar_already_exists)+'\nsuccess: '+\
                    #    str(success)+'\nacl: '+str(acl) #debug
                    #create success message
                    response = process_calendar( 
                            calendar_name, calendar_already_exists, success )

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
                            response += '\n<br/>' + calendar_requestor_1 + ' is not a valid user'

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
                            response += '\n<br/>' + calendar_requestor_2 + ' is not a valid user'

                    #print str(response) #debug
                    __logger__.info('user: ' + str(request.user) + ' has made the following request:\n' \
                            + str(response))
                    return HttpResponse( response )

                except Exception, err:
                    response = err
                    response += '\n<br/>calendar name: ' + calendar_name
                    response += '\n<br/>requestor_1: ' + calendar_requestor_1
                    response += '\n<br/>requestor_2: ' + calendar_requestor_2
                    return HttpResponse( response )

        #if its the groups form that was submitted
        else:
            form = GroupForm( request.POST )
            #check if form valid
            #print 'request.post: '+str(request.POST) #debug
            if not form.is_valid():
                return HttpResponse("form not valid...")
            #handle form submission
            else:
                '''DEBUGS VVVV'''
                #print 'form.cleaned_data: ' + str( form.cleaned_data ) #debug
                group_email = form.cleaned_data['group_email']
                group_name = form.cleaned_data['group_name']
                group_description = form.cleaned_data['group_description']
                group_requestor_1 = form.cleaned_data['group_requestor_1']
                group_requestor_2 = form.cleaned_data['group_requestor_2']
                '''DEBUGS ^^^^'''

                #group_email, group_name, group_description, group_requestor_1, group_requestor_2 = group_process_form(form)
                print str(group_email)+ str(group_name)+ str(group_description) + str(group_requestor_1) + str( group_requestor_2)


                '''DEBUG VVVV'''
                #print 'group_email: '+str(group_email)+' group_name: '+str(group_name)+\
                #    ' group_desc: '+str(group_description)+' group_requestor_1: '+\
                #    str(group_requestor_1)+' group_requestor_2: '+str(group_requestor_2) #debug
                '''DEBUG ^^^^'''

                #print 'debug' #debug

                try:
                    client = Group( 'gtest.pdx.edu' )
                    #print 'debug' #debug
                    group_already_exists, success = group_validate( 
                    group_name, group_description, client )

                    #print 'group already exists: '+str(group_already_exists)+'\nsuccess: '\
                    #    +str(success) #debug
                    #create success message
                    response = process_group( 
                            group_name, group_already_exists, success )
                    #print response #debug

                    if group_requestor_1:
                        if requestor_validate( group_requestor_1, client ):
                            requestor_1_already_owner = group_already_owner(
                                group_requestor_1, 
                                acl, 
                                client )

                            response += group_process_requestor(
                                group_requestor_1, 
                                calendar_name, 
                                requestor_1_already_owner, 
                                client )
                        else:
                            response += '\n<br/>' + group_requestor_1 + ' is not a valid user'
                    print response #debug

                    if group_requestor_2:
                        if requestor_validate( group_requestor_2, client ):
                            requestor_2_already_owner = group_already_owner(
                                group_requestor_2,
                                acl,
                                client )

                            response += group_process_requestor(
                                group_requestor_2, 
                                calendar_name, 
                                requestor_2_already_owner, 
                                client )
                        else:
                            response += '\n<br/>' + group_requestor_2 + ' is not a valid user'

                    print str(response) #debug
                    __logger__.info('user: ' + str(request.user) + ' has made the following request:\n' \
                            + str(response))
                    return HttpResponse( response )

                except Exception, err:
                    response = err
                    response += '\n<br/>calendar name: ' + calendar_name
                    response += '\n<br/>requestor_1: ' + requestor_1
                    response += '\n<br/>requestor_2: ' + requestor_2
                    return HttpResponse( response )
