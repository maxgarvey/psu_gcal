"""Google user profile management."""

from psugle import creds

import gdata.contacts.client
import gdata.contacts.data
import gdata.gauth


class Profile:
    """Google user profile management."""

    def __init__(self, domain=None, adminuser=None, oauth_secret=None, g_client=None):
        """New profile object. Google <domain> required. <adminuser> and
        <oauth_secret> will override module defaults.
        A <g_client> of type gdata.contacts.client.ContactsClient
        can be specified to re-use an existing client."""
        self.domain = domain

        if not adminuser:
            adminuser = creds.google[domain]["adminuser"]
        if not oauth_secret:
            oauth_secret = creds.google[domain]["oauth_secret"]

        if g_client:
            self.g_client = g_client
        else:
            self.g_client = gdata.contacts.client.ContactsClient(
                source = "pdx-edu-user-profile-client"
                ,domain=domain
            )
            self.g_client.auth_token = gdata.gauth.TwoLeggedOAuthHmacToken(
                consumer_key=domain
                ,consumer_secret=oauth_secret
                ,requestor_id="%s@%s" % (adminuser, domain)
            )


    def get_gal_visibility(self, user=None):
        """Queries the given <user>'s current visibility setting in Google's
        global address list."""
        user_uri = "https://www.google.com/m8/feeds/profiles/domain/%s/full/%s"\
            % (self.domain, user)

        profile = self.g_client.GetProfile(uri=user_uri)

        for element in profile.extension_elements:
            if element.attributes.has_key("indexed"): # indexed == "show in GAL"
                if element.attributes["indexed"] == "true":
                    return True
                else:
                    return False

            else: # If the field is missing, we're at a loss.
                return None


    def set_gal_visibility(self, user=None, visible=False):
        """Changes a given <user>'s visibility setting in Google's global
        address list."""
        user_uri = "https://www.google.com/m8/feeds/profiles/domain/%s/full/%s"\
            % (self.domain, user)

        if self.get_gal_visibility(user) != visible: # Change required
            new_setting = str(visible).lower()
            profile = self.g_client.GetProfile(uri=user_uri)

            for element in profile.extension_elements:
                if element.attributes.has_key("indexed"): # indexed == "show in GAL"
                    element.attributes["indexed"] = new_setting

            new_profile = self.g_client.UpdateProfile(profile) # Apply

            for element in new_profile.extension_elements:
                if element.attributes.has_key("indexed"): # indexed == "show in GAL"
                    if element.attributes["indexed"] == new_setting: # Did it take?
                        return True
                    else:
                        return False

        else: # No change required
            return True
