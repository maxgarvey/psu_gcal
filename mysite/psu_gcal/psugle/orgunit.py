"""Google organizational unit management."""

from psugle import creds

import gdata.apps.organization.service


class OrgUnit:
    """Google organizational unit management."""

    def __init__(self, domain=None, adminuser=None, password=None, g_client=None):
        """New OrgUnit object. Google <domain> required. <adminuser> and
        <password> will override module defaults.
        A <g_client> of type gdata.apps.organization.service.OrganizationService
        can be specified to re-use an existing client."""
        self.domain = domain

        if not adminuser:
            adminuser = creds.google[domain]["adminuser"]
        if not password:
            password = creds.google[domain]["password"]

        if g_client:
            self.g_client = g_client
        else:
            self.g_client = gdata.apps.organization.service.OrganizationService(
                domain=domain
                ,email="%s@%s" % (adminuser, domain)
                ,password=password
            )
            self.g_client.ProgrammaticLogin()

        self.customer_id = self.g_client.RetrieveCustomerId()["customerId"]


    def create(self, name=None, description=None, parent_org_unit_path="/"):
        """Create a new Organizational Unit with a given <name> and <description>.
        A <parent_org_unit_path> can be specified. Find them with list_all()."""
        return self.g_client.CreateOrgUnit(
            self.customer_id, name, parent_org_unit_path, description
        )


    def delete(self, org_unit_path=None):
        """Delete a given Organizational Unit, given its <org_unit_path>."""
        return self.g_client.DeleteOrgUnit(
            self.customer_id, org_unit_path
        )


    def list_users_in(self, org_unit_path=None):
        """List all users in a given <org_unit_path>."""
        addresses = self.g_client.RetrieveOrgUnitUsers(self.customer_id, org_unit_path)
        return [ a["orgUserEmail"].split('@')[0] for a in addresses ]


    def list_all(self):
        """List all Organizational Units, their paths and descriptions."""
        orgunits = self.g_client.RetrieveAllOrgUnits(self.customer_id)
        return [ {'org_unit_path':orgunit['org_unit_path']\
            ,'description':orgunit['description']} for orgunit in orgunits ]


    def move_user(self, user=None, org_unit_path="/"):
        """Move a <user> to a new <org_unit_path>. Moves to the root by default."""
        return self.g_client.UpdateOrgUser(
            self.customer_id, "%s@%s" % (user, self.domain), org_unit_path
        )


    def query_user(self, user=None):
        """Reports which Organizational Unit a given <user> resides."""
        user_status = self.g_client.RetrieveOrgUser(self.customer_id, "%s@%s" % (user, self.domain))

        if user_status["org_unit_path"] == None:
            user_status["org_unit_path"] = "/" # Make more consistent--moving requires a path.

        return user_status
