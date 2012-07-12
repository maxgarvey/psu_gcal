'''/var/www/psu_gcal/support/alias_util.py'''

from psugle.user import User
from subprocess import call
from tempfile import TemporaryFile

def create_alias(alias, uid):
    '''this method will create the alias in google's system via gam'''
    user_client = User()
    uid_exists = user_client.query_user(uid)
    if False in uid_exists.values():
        #if the uid doesn't exist or is disnabled, then we can't use it.
        #terminal failure
        return "the uid: {0} is not an existing user.".format(uid)
    else:
        alias_is_uid = user_client.query_user(alias)
        if True in alias_is_uid.values():
            #if the alias-to-be is an existing username, we can't
            #use it. terminal failure.
            return "the alias: {0} is a uid.".format(alias)
        else:
             alias_exists = user_client.query_alias(alias)
             if True in alias_exists.values():
                 #if the alias is an existing alias for someone else
                 #we can't use it. terminal failure.
                 return("The alias: {0} is already an alias for uid: {1}".format(alias,uid))
             else:
                 #if neither uid or alias are taken in any way. then try and
                 #add it as prescribed. First choice: psugle
                 user_client.create_alias(uid, alias)
                 #check results:
                 with TemporaryFile() as temp:
                     call(['/var/www/env/bin/python2.6',
                         '/var/www/psu_gcal/gam.py', 'info', 'user', uid],
                         stdout=temp)
                     temp.seek(0)
                     results = temp.read()
                 if alias in results:
                     return('Successfully created alias: {0} for user: {1}.'
                         .format(alias, uid))
                 else:
                     #if the first time doesn't go through, try again
                     #print('Google alias creation with psugle failed.' + \
                     #    'Attempting with gam.py.')
                     with TemporaryFile() as temp:
                         call(['/var/www/env/bin/python2.6',
                             '/var/www/psu_gcal/gam.py', 'create', 'alias',
                             alias, 'user', uid], stdout=temp)
                         temp.seek(0)
                         results = temp.read()
                     if not 'Creating alias {0}@pdx.edu for user {1}@pdx.edu'.format(alias, uid) in results:
                         pass #print('incorrect gam print statement.')
                     #one last check here to make sure the alias was added.
                     with TemporaryFile() as temp:
                         call(['/var/www/env/bin/python2.6',
                             '/var/www/psu_gcal/gam.py', 'info', 'user', uid],
                             stdout=temp)
                         temp.seek(0)
                         results = temp.read()
                     if alias in results:
                         return 'Successfully created alias: {0} for user: {1}'.format(alias, uid)
                     else:
                         return 'Could not create the alias: {0} for user: {1}'.format(alias, uid)+'\n'+str(results)
