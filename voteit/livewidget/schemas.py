import colander
from voteit.core.schemas.meeting import EditMeetingSchema
from arche.interfaces import ISchemaCreatedEvent

from voteit.livewidget import _


class LiveWidgetSettingsSchema(colander.Schema):
    live_widget_enabled = colander.SchemaNode(
        colander.Bool(),
        title=_("Enable Live Widget?"),
        description = _("live_widget_enabled_description",
                        default = "Note! This will allow unauthenticated users to "
                        "read the contents of this meeting. It will be exposed at "
                        "this meeting and every agenda item in it. "
                        "You'll find it at either 'live_widget' (for html view, suitable for iframes) "
                        "or 'live_widget.json' for a json structure."),
        tab='advanced',
        missing=False,
        default=False,
    )


def includeme(config):
    config.add_schema('Meeting', LiveWidgetSettingsSchema, 'live_widget_settings')
    # config.add_subscriber(add_livewidget_controls, [EditMeetingSchema, ISchemaCreatedEvent])
