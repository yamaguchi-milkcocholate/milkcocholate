from flask_modules.db import reader
from flask_modules.exceptions.dbhost import HostNotFoundException


class Repository:

    def __init__(self, host):
        try:
            self._reader = reader.Reader(host=host)
        except HostNotFoundException:
            raise
