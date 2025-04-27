from configparser import ConfigParser

class ConfigHandler:
    def __init__(self, config_file='config.ini'):
        self.config_file = config_file

    def get_config(self, section, option):
        """Чтение конфигурации"""
        config = ConfigParser()
        config.read(self.config_file)
        return config.get(section, option)

    def set_config(self, section, option, value):
        """Запись конфигурации"""
        config = ConfigParser()
        config.read(self.config_file)
        config.set(section, option, value)
        with open(self.config_file, 'w') as f:
            config.write(f)
