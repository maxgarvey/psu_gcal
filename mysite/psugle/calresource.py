"""Google calendar resource management."""

from gdata.calendar_resource.client import CalendarResourceClient
from gdata.calendar.client import CalendarClient
from gdata.calendar.data import CalendarAclEntry
from gdata.acl.data import AclRole, AclScope
from hashlib import md5
from urllib import quote
from psugle import creds


class CalendarResource:
    """Google calendar resource management."""

    def __init__(self, domain=None, adminuser=None, password=None, g_cal_client=None, g_res_client=None):
        """New orgunit object. Google <domain> required. <adminuser> and
        <password> will override module defaults.
        A <g_cal_client> of gdata.calendar.client.CalendarClient and
        A <g_res_client> of gdata.calendar_resource.client.CalendarResourceClient
        can be specified to re-use an existing client."""

        self.domain = domain
        cal_id = "pdx-calendar-sync-1.0"
        res_id = "pdx-resource-sync-1.0"

        if not adminuser:
            adminuser = creds.google[domain]["adminuser"]
        if not password:
            password = creds.google[domain]["password"]

        if g_cal_client:
            self.g_cal_client = g_cal_client
        else:
            self.g_cal_client = CalendarClient(domain=self.domain)

            self.g_cal_client.ClientLogin(
                "%s@%s" % (adminuser, domain)
                ,password
                ,cal_id
            )

        if g_res_client:
            self.g_res_client = g_res_client
        else:
            self.g_res_client = CalendarResourceClient(domain=self.domain)

            self.g_res_client.ClientLogin(
                "%s@%s" % (adminuser, domain)
                ,password
                ,res_id
            )


    def create(self, name=None, resource_type=None, description=None):
        """Create a new calendar resource. <name> required.
        <resource_type> and <description> are optional free-form strings."""
        self.g_res_client.CreateResource(
            resource_id=md5(name).hexdigest()
            ,resource_common_name=name
            ,resource_type=resource_type
            ,resource_description=description
        )


    def get_all_resources(self):
        """Dump a list of all existing calendar resources, each resource
        is a dict, {"name","email"}."""
        feed = self.g_res_client.GetResourceFeed()
        resource_entries = feed.entry

        while feed.get_next_link() != None:
            feed = self.g_res_client.GetNext(feed)
            resource_entries.extend(feed.entry)

        return [{"name":entry.GetResourceCommonName()\
            ,"email":entry.GetResourceEmail()} for entry in resource_entries]


    def get_acl_by_name(self, name=None):
        """Retrieve the ACLs for a resource, given its <name>."""
        resource = self.g_res_client.GetResource(
            resource_id=md5(name).hexdigest()
        )

        return self.get_acl_by_resource_email(
            resource_email=resource.GetResourceEmail()
        )


    def get_acl_by_resource_email(self, resource_email=None):
        """Retrieve the ACLs for a resource, given its <resource_email>
        address."""
        acluri = "https://www.google.com/calendar/feeds/%s/acl/full" \
            % quote(resource_email)

        acl_feed = self.g_cal_client.GetCalendarAclFeed(uri=acluri)

        return [(entry.scope.value, entry.role.value)\
            for entry in acl_feed.entry]


    def set_owner_by_name(self, name=None, owner=None):
        """Add <owner> to the list of a resource's owners, given the
        resource's <name>."""
        resource = self.g_res_client.GetResource(
            resource_id=md5(name).hexdigest()
        )

        self.set_owner_by_resource_email(
            resource_email=resource.GetResourceEmail(), owner=owner
        )


    def set_owner_by_resource_email(self, resource_email=None, owner=None):
        """Add <owner> to the list of a resource's owners, given the
        resource's <resource_email>."""
        newrule = CalendarAclEntry()

        newrule.scope = AclScope(
            value="%s@%s" % (owner, self.domain)
            ,type='user'
        )

        newrole = 'http://schemas.google.com/gCal/2005#%s' % ('owner')
        newrule.role = AclRole(value=newrole)

        acluri = "https://www.google.com/calendar/feeds/%s/acl/full" \
            % quote(resource_email)

        self.g_cal_client.InsertAclEntry(new_acl_entry=newrule, insert_uri=acluri)
