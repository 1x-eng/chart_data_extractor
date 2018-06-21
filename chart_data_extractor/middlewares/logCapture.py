"""
Author: Pruthvi Kumar BK
Email: pruthvikumar.123@gmail.com
Date: June 21, 2018

This middleware needs to be tied with falcon; persists all API calls with timestamp.
"""
import logging
import pygogo as gogo
import time

class PersistApiCalls():

    def __init__(self):
        super(PersistApiCalls, self).__init__()
        self.__log_format = '[%(asctime)s] <---> [%(name)s] <---> [%(levelname)s] <---> [%(message)s]'
        self.__formatter = logging.Formatter(self.__log_format)

        self.timer = {}
        self.logger = gogo.Gogo(
            'pk_scraperService_middleware',
            low_hdlr=gogo.handlers.file_hdlr('./logs/pk_scraperService_middleware.log'),
            low_formatter=self.__formatter,
            high_level='error',
            high_formatter=self.__formatter,
            ).logger

    def process_request(self, req, resp):
        self.timer['startTime'] = time.time()

    def process_response(self, req, resp, resource, req_succeded):
        self.logger.info('{} resource was served as success={} in {}s to {}. '
                         'Requested endpoint was- {}'.format(resource, req_succeded, (time.time() -
                                                                                      self.timer['startTime']),
                                                                                    req.remote_addr, req.path))

