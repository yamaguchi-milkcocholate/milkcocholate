import configparser
import os


class ConfigManager:

    def __init__(self):
        """
        check file path, and load it
        """
        INI_FILE = os.curdir+'/../config.ini'
        if not os.path.isfile(INI_FILE):
            raise Exception("error: wrong file path")
        self.ini = configparser.SafeConfigParaser()
        self.ini.read(INI_FILE)

    def show_config(self):
        """
        show all of contents in config file
        :return:
        """
        for section in self.ini.sections():
            print("[" + section + "]")
            self.show_section(section)
        return

    def show_section(self, section):
        """
        show a section
        :param section: string
        :return:
        """
        for key in self.ini.options(section):
            self.show_key(section, key)
        return

    def show_key(self, section, key):
        """
        show a key
        :param section: string
        :param key: string
        :return:
        """
        print(section + "." + key + " = " + self.ini.get(section, key))
        return

    def set_value(self, section, key, value):
        """
        add key and value
        :param section: string
        :param key: string
        :param value: string
        :return:
        """
        self.ini.set(section, key, value)
        print(section + "." + key + " = " + self.ini.get(section, key))
        return
