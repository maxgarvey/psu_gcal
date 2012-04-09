from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
#added next line for ajax-ing
from django.core.context_processors import csrf
from django.template import RequestContext, Context, loader
from django.contrib.auth.decorators import login_required
from cal_forms import NewCalendar
from sys import exc_info
from psugle.calresource import CalendarResource
import os

#for debug
import logging
logger = logging.getLogger(__name__)

@login_required
def index(request):
  if request.user.has_perm('psu_gcal.psu_gcal'):
    #logger.info('user has permission') #debug
    #if form has been submitted
    if request.method == 'POST':
      form = NewCalendar( request.POST )
      #if form valid, take all of the vars from it
      if form.is_valid():
        calendar_name = form.cleaned_data['calendar_name']
        requestor_1 = form.cleaned_data['requestor_1']
        requestor_2 = form.cleaned_data['requestor_2']
        try:
          client = CalendarResource( 'gtest.pdx.edu' )
          #create calendar if it doens't already exist
          calendar_already_exists = False
          existing_cals = client.get_all_resources()
          for cal in existing_cals:
              if cal['name'] == calendar_name:
                  calendar_already_exists = True
          if not calendar_already_exists:
              client.create( name=str(calendar_name) )
          #add requestors if they aren't already owners
          requestor_1_already_owner = False
          requestor_2_already_owner = False
          acl = client.get_acl_by_name( calendar_name )
          for entry in acl:
              if entry[0] == (requestor_1+'@'+str(client.domain)):
                  requestor_1_already_owner = True
          if (requestor_1 != '') and (not requestor_1_already_owner):
            client.set_owner_by_name( name=str(calendar_name),owner=str(requestor_1) )
          acl = client.get_acl_by_name( calendar_name )
          for entry in acl:
              if entry[0] == (requestor_2+'@'+str(client.domain)):
                  requestor_2_already_owner = True
          if (requestor_2 != '') and (not requestor_2_already_owner):
            client.set_owner_by_name( name=str(calendar_name),owner=str(requestor_2) )
          #create the success message
          success_message = ''
          if calendar_already_exists:
              success_message += calendar_name + ' (existing calendar)'
          else:
              success_message += calendar_name + ' (new calendar created)'
 
          #display success string
          return success( success_message, requestor_1, requestor_2, calendar_name )
        except:
          return failure( str(exc_info()[1]) + '\n<br/>calendar name: '+str(calendar_name)+'\n<br/>requestor1: '+str(requestor_1)+'\n<br/>requestor2: '+str(requestor_2) )
  
      #if form not valid
      else:
        return failure( 'form not valid...' )

    #if form HASN'T been submitted
    else:
      form = NewCalendar()
      template = loader.get_template( 'index.html' )
      context = Context()
      return render_to_response( 'index.html', { 'form':form }, context_instance=RequestContext(request)  )

  #if the user isn't properly priviledged or authed
  else:
    return render_to_response( 'invalid.html' )

#@login_required
def success( success_message, requestor_1, requestor_2, calendar_name ):
  '''render the template with all of the correct fields'''
  #return render_to_response('success.html', { 'success_message': success_message, \
  #  'requestor_1': requestor_1, 'requestor_2': requestor_2, 'calendar_name':calendar_name } )
  return HttpResponse( success_message )
  #return success_message

#@login_required
def failure( error_msg ):
  '''render the failure template wih the error message'''
  #return render_to_response( 'failure.html', { 'error_msg': error_msg } )
  return HttpResponse( error_msg )

#@login_required
def static( request, file ):
  try:
    print os.getcwd() #debug
    print os.access(str('/static/'+file), os.F_OK )
    static_file = open( str('/static/'+file) , 'r' )
    fs = static_file.read()
    return HttpResponse( fs )
  except:
    return HttpResponse( str( str(exc_info()[1]) ) )
