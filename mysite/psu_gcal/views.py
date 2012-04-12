'''psu_gcal/mysite/psu_gcal/views.py'''

from django.shortcuts import render_to_response 
from django.http import HttpResponse 
from django.template import RequestContext, Context, loader
from django.contrib.auth.decorators import login_required
from cal_forms import NewCalendar
from psugle.calresource import CalendarResource
from support.calendar_util import calendar_validate, already_owner, \
process_calendar, process_requestor, requestor_validate

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
            form = NewCalendar()
            template = loader.get_template( 'index.html' )
            context = Context()
            return render_to_response( 'index.html',
                    { 'form':form },
                    context_instance=RequestContext(request)  )
        else:
            form = NewCalendar( request.POST )
            #check if form valid
            if not form.is_valid():
                return HttpResponse("form not valid...")
            #handle form submission
            else:
                print 'form.cleaned_data: ' + str( form.cleaned_data ) #debug
                calendar_name = form.cleaned_data['calendar_name']
                requestor_1 = form.cleaned_data['requestor_1']
                requestor_2 = form.cleaned_data['requestor_2']
                try:
                    client = CalendarResource( 'gtest.pdx.edu' )
                    calendar_already_exists, success, acl = calendar_validate( 
                    calendar_name, client )

                    #create success message
                    response = process_calendar( 
                            calendar_name, calendar_already_exists, success )

                    if requestor_1:
                        if requestor_validate( requestor_1, client ):
                            requestor_1_already_owner = already_owner(
                                requestor_1, 
                                acl, 
                                client )

                            response += process_requestor(
                                requestor_1, 
                                calendar_name, 
                                requestor_1_already_owner, 
                                acl, 
                                client )

                            response += process_requestor(
                                requestor_1, 
                                calendar_name, 
                                requestor_1_already_owner, 
                                client )
                        else:
                            response += '\n<br/>' + requestor_1 + ' is not a valid user'

                    if requestor_2:
                        if requestor_validate( requestor_2, client ):
                            requestor_2_already_owner = already_owner(
                                requestor_2,
                                acl,
                                client )

                            response += process_requestor(
                                requestor_2, 
                                calendar_name, 
                                requestor_2_already_owner, 
                                client )
                        else:
                            response += '\n<br/>' + requestor_2 + ' is not a valid user'

                    return HttpResponse( response )
                except Exception, err:
                    response = err
                    response += '\n<br/>calendar name: ' + calendar_name
                    response += '\n<br/>requestor_1: ' + requestor_1
                    response += '\n<br/>requestor_2: ' + requestor_2
                    return HttpResponse( response )

