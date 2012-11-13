'''A simple little lib for getting oauth, and doing the boogie into gdata.'''
import os
import pickle
import gdata
import sys
import gdata.apps
import gdata.apps.groupsettings
import gdata.apps.groupsettings.service

#a hard coded version in case we get errors
__this_dir__ = '/var/www/psu_gcal'

def try_oauth(gdata_object):
    '''try oauth attempts to find the oauth file and verify that it's good
    to make api calls'''
    oauth_filename = 'oauth.txt'
    try:
        oauth_filename = os.environ['OAUTHFILE']
    except KeyError:
        pass
    if os.path.isfile(get_path() + oauth_filename):
        oauthfile = open(get_path() + oauth_filename, 'rb')
        print oauthfile.read() #debug
        oauthfile.seek(0) #debug
        domain = oauthfile.readline()[0:-1]
        try:
            token = pickle.load(oauthfile)
            oauthfile.close()
        # Deals with tokens created by windows on old GAM versions.
        #Rewrites them with binary mode set
        except ImportError:
            oauthfile = open(get_path() + oauth_filename, 'r')
            domain = oauthfile.readline()[0:-1]
            token = pickle.load(oauthfile)
            oauthfile.close()
            file_desc = open(get_path() + oauth_filename, 'wb')
            file_desc.write('%s\n' % (domain,))
            pickle.dump(token, file_desc)
            file_desc.close()
        gdata_object.domain = domain
        gdata_object.SetOAuthInputParameters(
           gdata.auth.OAuthSignatureMethod.HMAC_SHA1,
           consumer_key=token.oauth_input_params._consumer.key,
           consumer_secret=token.oauth_input_params._consumer.secret)
        token.oauth_input_params = gdata_object._oauth_input_params
        gdata_object.SetOAuthToken(token)
        return True
    else:
        return False

def get_path():
    '''get the path to gam, used to find oauth.txt'''
    if os.name == 'windows' or os.name == 'nt':
        divider = '\\'
    else:
        divider = '/'
    try:
        print 'path to look for oauth: {0}'.format(os.getcwd()+divider)
        #return os.getcwd()+divider
        return __this_dir__+divider
    except:
        print 'path to look for oauth: {0}'.format(os.getcwd()+divider)
        #print os.path.dirname(os.path.realpath(__this_dir__))+divider #debug
        return os.path.dirname(os.path.realpath(__this_dir__))+divider

def group_settings_object():
    groupsettings = gdata.apps.groupsettings.service.GroupSettingsService()
    if not try_oauth(groupsettings):
        #doRequestoauth()
        try_oauth(groupsettings)
    #groupsettings = commonAppsObjInit(groupsettings)
    return groupsettings

def set_archived_status(group_email):
    print 'group_email: {0}'.format(group_email)
    print 'get_path(): {0}'.format(get_path())
    gdata_object = group_settings_object()
    xml =  '''<?xml version="1.0" encoding="UTF-8"?>
    <entry xmlns="http://www.w3.org/2005/Atom" xmlns:apps="http://schemas.google.com/apps/2006" xmlns:gd="http://schemas.google.com/g/2005">
    <id>tag:googleapis.com,2010:apps:groupssettings:GROUP:NNN</id>
    <title>Groups Resource Entry</title>
    <author>
    <name>Google</name>
    </author>
    <apps:id>%s</apps:id>
    <apps:email>%s</apps:email>
    ''' % (group_email, group_email)
    xml += '<apps:isArchived>true</apps:isArchived></entry>'    
    print 'xml: {0}'.format(xml) #debug
    uri = '/groups/v1/groups/{0}?alt=atom'.format(group_email)
    print 'uri: {0}'.format(uri) #debug
    try:
        gdata_object.Put(uri=uri,data=xml)
        print 'change went through.'
    except Exception, err:
        print 'setting archived bit failed: {0}'.format(err)

if __name__ == "__main__":
    print 'sys.argv: ' + str(sys.argv) #debug
    print 'get_path(): ' + str(get_path()) #debug
    gdata_object = group_settings_object()

    try:
        #this one works, but I'm going to try and do it with just XML going
        #through the authed gdata agent.
        '''allow_external_members = allow_google_communication = None
        allow_web_posting = archive_only = custom_reply_to = None
        default_message_deny_notification_text = description = None
        is_archived = max_message_bytes = members_can_post_as_the_group =  None
        message_display_font = message_moderation_level = name = None
        primary_language = reply_to = send_message_deny_notification = None
        show_in_group_directory = who_can_invite =  who_can_join = None
        who_can_post_message = who_can_view_group = None
        who_can_view_membership = None'''
        #gdata_object.UpdateGroupSettings(sys.argv[1],allow_external_members=allow_external_members, allow_google_communication=allow_google_communication, allow_web_posting=allow_web_posting, archive_only=archive_only, custom_reply_to=custom_reply_to, default_message_deny_notification_text=default_message_deny_notification_text, description=description, is_archived='true', max_message_bytes=max_message_bytes, members_can_post_as_the_group=members_can_post_as_the_group, message_display_font=message_display_font, message_moderation_level=message_moderation_level, name=name, primary_language=primary_language, reply_to=reply_to, send_message_deny_notification=send_message_deny_notification, show_in_group_directory=show_in_group_directory, who_can_invite=who_can_invite, who_can_join=who_can_join, who_can_post_message=who_can_post_message, who_can_view_group=who_can_view_group, who_can_view_membership=who_can_view_membership)

        #here's a way to change the is_archived setting via a raw atom XML message
        #going to the API thru an oauth-ed gdata client with groupsettings enabled
        xml =  '''<?xml version="1.0" encoding="UTF-8"?>
<entry xmlns="http://www.w3.org/2005/Atom" xmlns:apps="http://schemas.google.com/apps/2006" xmlns:gd="http://schemas.google.com/g/2005">
  <id>tag:googleapis.com,2010:apps:groupssettings:GROUP:NNN</id>
  <title>Groups Resource Entry</title>
  <author>
    <name>Google</name>
  </author>
  <apps:id>%s</apps:id>
  <apps:email>%s</apps:email>
''' % (sys.argv[1], sys.argv[1])
        xml += '<apps:isArchived>true</apps:isArchived></entry>'
        uri = '/groups/v1/groups/%s?alt=atom' % sys.argv[1]

        gdata_object.Put(uri=uri,data=xml)

        print 'change went through' #debug
    except Exception, err:
        print 'error setting archived bit: {0}'.format(err)
        #pass
