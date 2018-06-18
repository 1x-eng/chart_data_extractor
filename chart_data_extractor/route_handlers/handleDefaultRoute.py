"""
Author: Pruthvi Kumar BK
Email: pruthvikumar.123@gmail.com
Date: 18 June, 2018

This section handles default route for scrape webservice
"""
import falcon
import json

class HandleDefaultRoute(object):

    def __init__(self):
        super(HandleDefaultRoute, self).__init__()

    def on_get(self, req, resp):
        resp.body = json.dumps({'message': 'Scraper Service is initialized and functional! Please use valid endpoints to get value '
                                'of this webservice. At this moment, "/v1/chartDataExtractor" is a valid endpoint.'})
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        self.on_get(req, resp)
