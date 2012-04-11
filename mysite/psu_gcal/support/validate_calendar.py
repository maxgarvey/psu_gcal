#calendar_validate.py

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
    except:
      pass

  #get acl
  if calendar_already_exists or success:
    try:
      acl = client.get_acl_by_name( calendar_name )
    except:
      acl = []
  else:
    acl = []

  return calendar_already_exists, success, acl

def already_owner( requestor, acl, client ):
  '''this function takes a requestor name an acl and a client and returns
  a boolean as to whether the requestor is already an owner'''
  for entry in acl:
    if entry[0] == (requestor+'@'+str( client.domain )):
      return True
  return False
