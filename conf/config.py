from configparser import ConfigParser


class Config:
    def __init__(self, path):
        self.path = path

    @property
    def settings(self):
        conf = ConfigParser()
        conf.read(self.path)
        return conf

    @property
    def basic(self):
        return self.settings['APP']
