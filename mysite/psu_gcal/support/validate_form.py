#validate_form.py
#from cal_forms import NewCalendar
#from gdata.apps.client import AppsClient

def validate_cal_form( form, app_client ):
  '''this method validates a form takes form and client as input.'''
  if form.is_valid():
    calendar_name = form.cleaned_data['calendar_name']
    requestor_1 = form.cleaned_data['requestor_1']
    requestor_2 = form.cleaned_data['requestor_2']

    valid_requestor_1 = validate_cal_requestor( requestor_1, app_client )
    valid_requestor_2 = validate_cal_requestor( requestor_2, app_client )

    return True, calendar_name, valid_requestor_1, requestor_1, valid_requestor_2, requestor_2

  else: #if form is not valid...
    return False, calendar_name, False, requestor_1, False, requestor_2

def validate_cal_requestor( requestor, app_client ):
  '''this method validates that a user exists in the domain of interest'''
  valid = False
  try:
    app_client.RetrieveUser( requestor )
    valid = True
  except:
    pass

  return valid 
