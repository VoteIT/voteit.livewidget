from pyramid.httpexceptions import HTTPForbidden
from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.traversal import find_resource
from pyramid.traversal import resource_path
from pyramid.view import view_config
from pyramid.view import view_defaults
from voteit.core.models.interfaces import IAgendaItem
from voteit.core.models.interfaces import IMeeting
from arche.views.base import BaseView

from voteit.livewidget import _



@view_defaults(permission = NO_PERMISSION_REQUIRED)
class LiveWidgetView(BaseView):
    """ This view renders listings, if live widget is enabled.
    """

    def __init__(self, context, request):
        self.meeting = request.meeting
        if not self.meeting.get_field_value('live_widget_enabled', None):
            raise HTTPForbidden(_("Feed disabled for this meeting"))
        super(LiveWidgetView, self).__init__(context, request)

    @view_config(context = IMeeting,
                 name = "live_widget",
                 renderer = "voteit.livewidget:templates/live_widget.pt")
    @view_config(context = IAgendaItem,
                 name = "live_widget",
                 renderer = "voteit.livewidget:templates/live_widget.pt")
    def view(self):
        return {'meeting': self.meeting}

    @view_config(context = IMeeting,
                 name = "live_widget.json",
                 renderer = "json")
    @view_config(context = IAgendaItem,
                 name = "live_widget.json",
                 renderer = "json")
    def json(self):
        output = []
        for obj in self.get_objects():
            output.append({'title': obj.title,
                           'creator': obj.creator[0],
                           'type_name': obj.type_name,
                           'created': self.request.dt_handler.format_dt(obj.created)})
        return output

    def get_objects(self):
        """ Fetch objects that should be listed. """
        limit = 10 #Configurable?
        query = 'type_name in any(["Proposal", "DiscussionPost"]) '
        query += 'and path == "%s"' % resource_path(self.context)
        cquery = self.root.catalog.query
        for docid in cquery(query, sort_index = 'created', reverse = True, limit = limit)[1]:
            path = self.root.document_map.address_for_docid(docid)
            yield find_resource(self.root, path)

def includeme(config):
    config.scan()
