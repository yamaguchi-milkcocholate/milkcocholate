import configparser
import os


class ConfigManager:

    def __init__(self):
        """
        ファイルのパスをチェックして、設定ファイルを読み込む
        """
        INI_FILE = os.curdir+'/../config.ini'
        if not os.path.isfile(INI_FILE):
            raise Exception("設定ファイルのパスが間違っている")
        self.ini = configparser.SafeConfigParaser()
        self.ini.read(INI_FILE)

    def show_config(self):
        """
        設定ファイルのすべての内容を表示
        :return:
        """
        for section in self.ini.sections():
            print("[" + section + "]")
            self.show_section(section)
        return

    def show_section(self, section):
        """
        セクションのキーを表示する
        :param section: string セクションの文字列
        :return:
        """
        for key in self.ini.options(section):
            self.show_key(section, key)
        return

    def show_key(self, section, key):
        """
        キーを表示する
        :param section: string セクションの文字列
        :param key: string キーの文字列
        :return:
        """
        print(section + "." + key + " = " + self.ini.get(section, key))
        return

    def set_value(self, section, key, value):
        """
        キーを設定する
        :param section: string
        :param key: string
        :param value: string
        :return:
        """
        self.ini.set(section, key, value)
        print(section + "." + key + " = " + self.ini.get(section, key))
        return
