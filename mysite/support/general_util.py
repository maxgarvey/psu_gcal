'''/psu_gcal/mysite/psu_gcal/support/general_util.py'''

from psugle.user import User

def requestor_validate( requestor, client ):
    '''this method makes sure the user exists in the system'''
    try:
        user = User( client.domain )
    except:
        return False
    try:
        if user.query_user( requestor )['exists']:
            return True
        else:
            return False
    except TypeError, err:
        raise Exception('couldn\'t query user: '+str(requestor))
