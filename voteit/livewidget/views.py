from betahaus.viewcomponent import view_action
from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.view import view_config
from pyramid.view import view_defaults
from voteit.core import security
from voteit.core.models.interfaces import IMeeting
from voteit.core.views.base_edit import DefaultEditForm
from pyramid.traversal import find_interface
from pyramid.httpexceptions import HTTPForbidden
from pyramid.traversal import resource_path
from pyramid.traversal import find_root
from pyramid.traversal import find_resource
from voteit.core.models.interfaces import IDateTimeUtil
from voteit.core.models.interfaces import IFanstaticResources
from voteit.core.views.api import APIView

from voteit.livewidget import _
from voteit.livewidget.schemas import LiveWidgetSettingsSchema


@view_action('settings_menu', 'livewidget',
             title = _("Live widget"),
             permission = security.MODERATE_MEETING)
def generic_menu_link(context, request, va, **kw):
    api = kw['api']
    url = request.resource_url(api.meeting, 'live_widget_settings')
    return """<li><a href="%s">%s</a></li>""" % (url, request.localizer.translate(va.title))


@view_config(context = IMeeting,
             name = "live_widget_settings",
             permission = security.MODERATE_MEETING,
             renderer = "voteit.core:views/templates/base_edit.pt")
class LiveWidgetSettingsForm(DefaultEditForm):
    """ Configure live stream for this meeting.
        NOTE: This view depends on a deprecated view class in VoteIT.
    """

    def get_schema(self):
        return LiveWidgetSettingsSchema()


@view_defaults(context = IMeeting,
               permission = NO_PERMISSION_REQUIRED)
class LiveWidgetView(object):
    """ This view renders listings, if live widget is enabled.
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.api = APIView(context, request)
        meeting = self.api.meeting
        if not meeting.get_field_value('live_widget_enabled', None):
            raise HTTPForbidden(_("Feed disabled for this meeting"))
        self.root = find_root(meeting)
        self.dt_util = self.api.dt_util

    @view_config(name = "live_widget", renderer = "voteit.livewidget:templates/live_widget.pt")
    def view(self):
        #FIXME: This is not compatible with the newer Arche VoteIT
        self.api.include_needed(self.context, self.request, self)
        return {'meeting': self.api.meeting}

    @view_config(name = "live_widget.json", renderer = "json")
    def json(self):
        output = []
        for obj in self.get_objects():
            output.append({'title': obj.title, 'creators': obj.creators[0], 'content_type': obj.content_type, 'created': self.dt_util.dt_format(obj.created)})
        return output

    def get_objects(self):
        """ Fetch objects that should be listed. """
        limit = 10 #Configurable?
        query = 'content_type in any(["Proposal", "DiscussionPost"]) '
        query += 'and path == "%s"' % resource_path(self.context)
        cquery = self.root.catalog.query
        for docid in cquery(query, sort_index = 'created', reverse = True, limit = limit)[1]:
            path = self.root.catalog.document_map.address_for_docid(docid)
            yield find_resource(self.root, path)

        
def includeme(config):
    config.scan()
