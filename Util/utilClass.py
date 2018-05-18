from configparser import ConfigParser



class ConfigParse(ConfigParser):
    '''
    for support upper option
    '''
    def __init__(self):
        ConfigParser.__init__(self)

    def optionxform(self, optionstr):
        return optionstr