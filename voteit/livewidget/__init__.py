from pyramid.i18n import TranslationStringFactory


_ = TranslationStringFactory('voteit.livewidget')


def includeme(config):
    config.include('.views')