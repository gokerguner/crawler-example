import sys
import logging
import inspect
logging.getLogger("requests.packages.urllib3.connectionpool").setLevel(logging.WARNING)


class LOGGER(object):
    ''' Logger Class object
    Example usage:
    logging = LOGGER(status=1, param_handler=None)

    suggested to use envparams/Params object for passing arguments
    logging = LOGGER(status=prms.DEBUG, param_handler=prms)
    '''

    _prms = None
    log = None

    def __init__(self, status=0, param_handler=None, scrapy=None):
        if scrapy:
            self._prms = param_handler
            self.init_logger(self._prms.DEBUG, self._prms.SCRAPY_DEBUG_LOG_LEVEL, self._prms.DEBUG_LOG_FILE)
        elif param_handler is not None:
            self._prms = param_handler
            self.init_logger(self._prms.DEBUG, self._prms.DEBUG_LOG_LEVEL, self._prms.DEBUG_LOG_FILE)
        else:
            self.init_logger()

        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        caller_method = calframe[1].filename


    def init_logger(self, status=0, LOG_LEVEL='INFO', LOG_FILENAME=None):
        ''' Initialize the logging
        LOG LEVELS: CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET
        '''
        # src1: https://docs.python.org/2/library/logging.html
        # src2: https://stackoverflow.com/questions/24816456/python-logging-wont-shutdown
        # src3 https://stackoverflow.com/questions/6579496/using-print-statements-only-to-debug
        self.log = logging.getLogger()
        filehandler = None

        if status == 0:  # logging disabled
            self.log.setLevel(logging.NOTSET)
        elif LOG_FILENAME is not None:
            self.log.setLevel(logging.getLevelName(LOG_LEVEL))
            # fh = logging.FileHandler(filename='test.log')
            filehandler = logging.FileHandler(filename=LOG_FILENAME)
            filehandler.setLevel(logging.getLevelName(LOG_LEVEL))
            formatter = logging.Formatter(
                fmt='%(asctime)s %(module)s %(levelname)s: %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            filehandler.setFormatter(formatter)
            self.log.addHandler(filehandler)

            # donot forget to delete handlers at the end of execution
            # logging.removeHandler(fh)
            # del logging, fh
            # logging.shutdown()
        else:
            logging.basicConfig(stream=sys.stderr, level=logging.INFO)
            #logging.info("Logging initialized")
            self.log = logging.getLogger()

    @staticmethod
    def logger_shutdown():
        # self.logging.shutdown()
        logging.shutdown()

    def set_debug_loglevel(self, status):
        status = status.upper()

        try:
            self.log.setLevel(status)
            self._prms.DEBUG_LOG_LEVEL = status
        except:
            self.log.error("cannot set log level to: %s", status)


if __name__ == '__main__':
    pass