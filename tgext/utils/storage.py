import random
import string
from os import path, mkdir

from tg import config


def store(data):
    extension = tell_extension(data)
    filename = generate_id(extension)
    destination = _specify_path(filename)

    with open(destination, mode='wb') as dest:
        content = data.file.read()
        dest.write(content)
        return filename


def _specify_path(filename):
    storage_path = path.join(config['paths']['static_files'], '..', 'storage')
    if not path.exists(storage_path):
        mkdir(storage_path)
    return '{}/{}'.format(storage_path, filename)


def tell_extension(file):
    return file.filename.split('.')[-1]


def generate_id(ext, size=16, chars=string.ascii_lowercase + string.digits):
    uid = ''.join(random.choice(chars) for _ in range(size))
    return '{}.{}'.format(uid, ext)
