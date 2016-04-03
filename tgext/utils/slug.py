import re, unicodedata


def slugify(entity_id, value):
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub('[^\w\s-]', '', value).strip().lower()
    value = re.sub('[-\s]+', '-', value)

    return '%s-%s' % (value, entity_id)


def slug2entityid(slug):
    try:
        return slug.split('-', 1)[-1]
    except:
        return slug
