# -*- coding: utf-8 -*-
import string
from collections import OrderedDict
from markupsafe import Markup


TEMPLATES = OrderedDict((
    ('og', string.Template('<meta property="og:${name}" content="${value}"/>')),
    ('twitter', string.Template('<meta name="twitter:${name}" content="${value}"/>')),
    ('itemprop', string.Template('<meta itemprop="${name}" content="${value}"/>'))
))
TRANSLATIONS = {
    'title': {'itemprop': 'name'}
}


def _metatag(name, value):
    for ns, tmpl in TEMPLATES.items():
        yield tmpl.substitute(
            name=TRANSLATIONS.get(name, {}).get(ns, name),
            value=value
        )


def metatags(d=None, **kwargs):
    """Generate meta tags.

    :param title: og,twitter,itemprop title
    :param description: og,twitter,itemprop description
    :param image: og,twitter,itemprop thumbnail
    :param url: og,twitter,itemprop resource url
    """
    d = d or OrderedDict()
    d.update(kwargs)
    tags = []
    for tag in d:
        tags.extend(_metatag(tag, d[tag]))
    return Markup('\n'.join(tags))
