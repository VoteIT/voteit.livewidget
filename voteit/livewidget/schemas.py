import colander

from voteit.livewidget import _


class LiveWidgetSettingsSchema(colander.Schema):
    live_widget_enabled = colander.SchemaNode(colander.Bool(),
                                              title = _("Enable Live Widget?"),
                                              description = _("Note! This will allow unauthenticated users to read the contents of this meeting."))
