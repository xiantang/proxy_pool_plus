import logging
from  logging.handlers import TimedRotatingFileHandler


CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0

class LogHandler(logging.Logger):

    def __init__(self,name,level=DEBUG,stream=True):
        self.level=level
        self.name=name
        logging.Logger.__init__(self,self.name,level=level)
        if stream:
            self.__setStreamHandler__()

    def __setStreamHandler__(self,level=None):
        '''

        :param level:
        :return:
        '''
        stream_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
        stream_handler.setFormatter(formatter)
        if not level:
            stream_handler.setLevel(self.level)
        else:
            stream_handler.setLevel(level)
        self.addHandler(stream_handler)

if __name__ == '__main__':
    log = LogHandler('test')
    log.info('this is a test msg')