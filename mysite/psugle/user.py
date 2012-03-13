"""Google user management."""

from psugle import creds

import gdata.apps.service
import gdata.apps


class User:
    """Google user management."""

    def __init__(self, domain=None, adminuser=None, password=None, g_client=None):
        """New User object. Google <domain> required. <adminuser> and
        <password> will override module defaults.
        A <g_client> of type gdata.apps.service.AppsService
        can be specified to re-use an existing client."""
        self.domain = domain

        if not adminuser:
            adminuser = creds.google[domain]["adminuser"]
        if not password:
            password = creds.google[domain]["password"]

        if g_client:
            self.g_client = g_client
        else:
            self.g_client = gdata.apps.service.AppsService(
                domain=domain
                ,email="%s@%s" % (adminuser, domain)
                ,password=password
            )
            self.g_client.ProgrammaticLogin()


    def query_alias(self, alias=None):
        """For a given <alias>, returns a dict regarding existence
        and real user."""
        try:
            alias_data = self.g_client.RetrieveNickname(alias)
            return {"exists": True, "real_name": alias_data.login.user_name}

        except gdata.apps.service.AppsForYourDomainException, err:
            if err.error_code == 1301:
                return {"exists": False, "real_name": None}


    def query_user(self, user_name=None):
        """For a given <user_name>, returns a dict regarding existence
        and enabled/disabled status"""
        try:
            user_disabled = self.g_client.RetrieveUser(user_name).login.suspended
            if user_disabled == 'false':
                return {"exists": True, "enabled": True}
            elif user_disabled == 'true':
                return {"exists": True, "enabled": False}

        except gdata.apps.service.AppsForYourDomainException, err:
            if err.error_code == 1301:
                return {"exists": False, "enabled": False}


    def status(self, user_name=None):
        """For a given <user_name>, returns a dict regarding existence,
        type (user|alias), real username, and enabled/disabled status"""
        alias = self.query_alias(user_name)

        if alias["exists"] == True:
            real_name = alias["real_name"]
        else:
            real_name = user_name

        user = self.query_user(real_name)

        return {"exists": user["exists"]
            ,"enabled": user["enabled"]
            ,"is_alias": alias["exists"]
            ,"real_name": real_name
        }


    def create(self, user_name=None, given_name=None, family_name=None, user_suspended=False, password_hash=None, hash_algorithm="SHA-1"):
        """Creates a Google user given the attributes. Expects a
        pre-computed password hash. <pw_hash> is either 'MD5' or
        'SHA-1' (default)"""
        self.g_client.CreateUser(
            user_name = user_name
            ,family_name = family_name
            ,given_name = given_name
            ,password = password_hash
            ,password_hash_function = hash_algorithm
            ,suspended = str(user_suspended).lower()
        )


    def rename(self, user_name=None, new_user_name=None, new_given_name=None, new_family_name=None):
        """Changes a user's given_name, family_name, or user_name.
        Only specify the attributes you wish to change. Those left
        unspecified will be untouched."""
        user_record = self.g_client.RetrieveUser(user_name = user_name)

        if new_user_name:
            user_record.login.user_name = new_user_name

        if new_given_name:
            user_record.login.given_name = new_given_name

        if new_family_name:
            user_record.login.family_name = new_family_name

        if new_user_name or new_given_name or new_family_name:
            self.g_client.UpdateUser(user_name = user_name, user_entry = user_record)


    def create_alias(self, user_name=None, alias=None):
        """Creates an alias for a user."""
        self.g_client.CreateNickname(
            user_name = user_name
            ,nickname = alias
        )


    def reset_password(self, user_name=None, password_hash=None, hash_algorithm="SHA-1"):
        """Resets a Google user's password. Expects a pre-computing
        password hash. <pw_hash> is either 'MD5' or 'SHA-1' (default)"""
        user_record = self.g_client.RetrieveUser(user_name = user_name)

        user_record.login.password = password_hash
        user_record.login.hash_function_name = hash_algorithm

        self.g_client.UpdateUser(user_name, user_record)


    def enable(self, user_name=None):
        """Re-enables a suspended user."""
        self.g_client.RestoreUser(user_name = user_name)


    def disable(self, user_name=None):
        """Disables an enabled user."""
        self.g_client.SuspendUser(user_name = user_name)


    def delete(self, user_name=None):
        """Deletes a user."""
        self.g_client.DeleteUser(user_name = user_name)


    def delete_alias(self, alias=None):
        """Deletes an alias for a user."""
        self.g_client.DeleteNickname(nickname = alias)
