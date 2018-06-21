"""
Author: Pruthvi Kumar BK
Date: June 21, 2018

Set of utilities to assist general programming.
"""
import logging
import pygogo as gogo

class MyUtilities(object):

    def __init__(self):
        super(MyUtilities, self).__init__()
        self.getLogger = self._logger


    def _logger(self, logFileName='pk_logger_genericName', logFilePath='./logs/pk_logger_genericName'):
        log_format = '[%(asctime)s] <---> [%(name)s] <---> [%(levelname)s] <---> [%(message)s]'
        formatter = logging.Formatter(log_format)
        myLogger = gogo.Gogo(
            logFileName,
            low_hdlr=gogo.handlers.file_hdlr(logFilePath),
            low_formatter=formatter,
            high_level='error',
            high_formatter=formatter,
        ).logger

        return myLogger