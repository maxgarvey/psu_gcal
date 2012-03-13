"""Google group management."""

from psugle import creds

import gdata.apps.groups.service
import gdata.apps


class Group:
    """Google group management."""

    def __init__(self, domain=None, adminuser=None, password=None, g_client=None):
        """New Group object. Google <domain> required. <adminuser> and
        <password> will override module defaults.
        A <g_client> of type gdata.apps.groups.service.GroupsService
        can be specified to re-use an existing client."""
        self.domain = domain

        if not adminuser:
            adminuser = creds.google[domain]["adminuser"]
        if not password:
            password = creds.google[domain]["password"]

        if g_client:
            self.g_client = g_client
        else:
            self.g_client = gdata.apps.groups.service.GroupsService(
                domain=domain
                ,email="%s@%s" % (adminuser, domain)
                ,password=password
            )
            self.g_client.ProgrammaticLogin()


    def status(self, group_name=None):
        """For a given <group_name>, returns a dict to indicate existence
        and other data."""
        try:
            group_status = self.g_client.RetrieveGroup(group_name)
            return {"exists": True, "data": group_status}

        except gdata.apps.service.AppsForYourDomainException, err:
            if err.error_code == 1301:
                return {"exists": False, "data": None}


    def create(self, group_name=None, description=None, open_membership=False):
        """Creates a Google group given the attributes.
        open_membership == True allows anyone to subscribe, False
        requires owner approval."""
        if open_membership == True:
            permissions = gdata.apps.groups.service.PERMISSION_ANYONE
        else:
            permissions = gdata.apps.groups.service.PERMISSION_OWNER

        self.g_client.CreateGroup(
            group_id = group_name
            ,group_name = group_name
            ,description = description
            ,email_permission = permissions
        )


    def subscribe(self, group_name=None, user_name=None):
        """Subscribes a user to a group."""
        user_email = "%s@%s" % (user_name, self.domain)

        if self.g_client.IsMember(user_email, group_name) == False:
            self.g_client.AddMemberToGroup(user_email, group_name)


    def unsubscribe(self, group_name=None, user_name=None):
        """Unsubscribes a user to a group."""
        user_email = "%s@%s" % (user_name, self.domain)

        if self.g_client.IsMember(user_email, group_name) == True:
            self.g_client.RemoveMemberFromGroup(user_email, group_name)


    def make_owner(self, group_name=None, user_name=None):
        """Makes a user an group owner. If <memberAlso> if False, user
        will not be able to post or recieve group email."""
        user_email = "%s@%s" % (user_name, self.domain)

        if self.g_client.IsOwner(user_email, group_name) == False:
            self.g_client.AddOwnerToGroup(user_email, group_name)


    def remove_owner(self, group_name=None, user_name=None):
        """Removes a user's group ownership. If <memberAlso> if False, user
        will not be able to post or recieve group email."""
        user_email = "%s@%s" % (user_name, self.domain)

        if self.g_client.IsOwner(user_email, group_name) == True:
            self.g_client.RemoveOwnerFromGroup(user_email, group_name)


    def delete(self, group_name=None):
        """Deletes a group."""
        self.g_client.DeleteGroup(group_id = group_name)
