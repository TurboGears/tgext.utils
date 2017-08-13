import uuid
from os import path, mkdir

from tg import config
from tg.util.files import safe_filename


def store(data):
    folder_name = generate_uuid()
    original_filename = safe_filename(data.filename)
    destination = _specify_path(folder_name, original_filename)

    with open(destination, mode='wb') as dest:
        content = data.file.read()
        dest.write(content)
        return destination


def _specify_path(folder_name, original_filename):
    storage_path = path.join(config['paths']['static_files'])
    if not path.exists(storage_path):
        mkdir(storage_path)

    destination_folder = path.join(storage_path, folder_name)
    mkdir(destination_folder)
    return path.join(destination_folder, original_filename)


def generate_uuid():
    return str(uuid.uuid1())
