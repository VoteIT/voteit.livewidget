from pyramid.i18n import TranslationStringFactory


_ = TranslationStringFactory('voteit.livewidget')


def includeme(config):
    config.include('.views')
    config.include('.schemas')

    #Make sure meeting has a 'live_widget_enabled' property, accessing the old storage
    from voteit.core.models.meeting import Meeting
    
    def _lw_getter(self):
        return self.get_field_value('live_widget_enabled', False)
    def _lw_setter(self, value):
        self.set_field_value('live_widget_enabled', value)
    Meeting.live_widget_enabled = property(_lw_getter, _lw_setter)
