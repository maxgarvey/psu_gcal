"""Google email settings management."""

from psugle import creds

import gdata.apps.emailsettings.client
import gdata.gauth


class EmailSettings:
    """Google email settings management."""

    def __init__(self, domain=None, adminuser=None, oauth_secret=None, g_client=None):
        """New EmailSettings object. Google <domain> required. <adminuser> and
        <oauth_secret> will override module defaults.
        A <g_client> of type gdata.apps.emailsettings.client.EmailSettingsClient
        can be specified to re-use an existing client."""
        self.domain = domain

        if not adminuser:
            adminuser = creds.google[domain]["adminuser"]
        if not oauth_secret:
            oauth_secret = creds.google[domain]["oauth_secret"]

        if g_client:
            self.g_client = g_client
        else:
            self.g_client = gdata.apps.emailsettings.client.EmailSettingsClient(domain=domain)
            self.g_client.auth_token = gdata.gauth.TwoLeggedOAuthHmacToken(
                consumer_key=self.domain
                ,consumer_secret=oauth_secret
                ,requestor_id="%s@%s" % (adminuser, domain)
            )


    def get_forwarding(self, user=None):
        """Returns a dictionary for a given <user>:
        {"forwarding_enabled":boolean,"forwarding_address":email_address}"""
        user_uri = "https://www.google.com/a/feeds/emailsettings/2.0/%s/%s/forwarding"\
            % (self.domain, user)
        enabled = False
        address = None

        settings = self.g_client.GetEntry(uri=user_uri)

        for element in settings.extension_elements:
            try:
                if element.attributes["name"] == "enable": # Is forwarding enabled?
                    if element.attributes["value"] == "true":
                        enabled = True
                    else:
                        enabled = False
    
                elif element.attributes["name"] == "forwardTo": # Forwarding address
                    address = element.attributes["value"]

            except KeyError: # Sometimes we get empty dicts.
                pass

        return {"forwarding_enabled":enabled, "forwarding_address":address}


    def set_forwarding(self, user=None, enable=False, forwarding_address=None, action="KEEP"):
        """Sets forwarding for a given <user>.

        <forward_address> must be one of the following:
        1. It belongs to the same domain,
        2. It belongs to a subdomain of the same domain, or
        3. It belongs to a domain alias configured as part of the same Google Apps account.
        
        <actions> are one of the following strings:
        KEEP (in inbox), ARCHIVE, or DELETE (send to spam), or MARK_READ (marked as read)"""
        self.g_client.UpdateForwarding(
            username=user
            ,enable=enable
            ,forward_to=forwarding_address
            ,action=action
        )


    def set_webclip(self, user=None, enable=False):
        """Enabled or disables webclips for a given <user>."""
        self.g_client.UpdateWebclip(username=user, enable=enable)
