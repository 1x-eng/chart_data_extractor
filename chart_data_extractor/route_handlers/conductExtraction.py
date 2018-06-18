"""
Author: Pruthvi Kumar BK
Email: pruthvikumar.123@gmail.com
Date: 18 June, 2018

This section handles route to initialize extraction.
"""

import falcon
import json
from scrape_engine.extractor import ChartsDataExtractor

class ConductExtraction(ChartsDataExtractor):

    def __init__(self):
        super(ConductExtraction, self).__init__()

    def on_get(self, req, resp):
        try:
            targetUrl = req.get_param('targetUrl') or None

            if (targetUrl != None):
                resp.body = json.dumps(self.executePipeline(targetUrl))
                resp.status = falcon.HTTP_200
            else:
                resp.body = json.dumps({'message': 'Scraper service has not received a valid URL to initialize scrape.'
                                                   'Please provide a queryParam named "targetUrl" '
                                                   '(eg. /v1/chartDataExtractor/?targetUrl=https://www.google.com) to'
                                                   'initialize scrape engine.'})
                resp.status = falcon.HTTP_200

        except Exception as e:
            resp.body = json.dumps({'message': 'There has been an error in servicing your request. Please report this '
                                               'to PK @ pruthvikumar.123@gmail.com with a valid subject line (eg. '
                                               'Bug in Scraper Service). Also, please copy paste the stackTrace that '
                                               'is included in this payload for prompt response.',
                                    'stackTrace': str(e)})
            resp.status = falcon.HTTP_500

    def on_post(self, req, resp):

        resp.body = json.dumps({'message': 'POST request is invalid. Scraper service is a GET call with "targetUrl" as'
                                           ' query param.'})
        resp.status = falcon.HTTP_200


