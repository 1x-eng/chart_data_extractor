"""
Author: Pruthvi Kumar BK
Date: May 29, 2018

Set of utilities to assist in scraping contents of a web page.
"""
from utilities.utilities import MyUtilities
from bs4 import BeautifulSoup
import re
import requests

class ScrapeUtilities(MyUtilities):

    def __init__(self):
        super(ScrapeUtilities, self).__init__()
        self.logger = self.getLogger(logFileName='pk_scraperService_scrapeUtilities',
                                     logFilePath='./logs/pk_scraperService_scrapeUtilities.log')
        self.soupAnUrl = self._soupAnUrl
        self.getDomIdContainingAttribute = self._getDomIdContainingAttribute
        self.seekAllScriptsContainingKey = self._seekAllScriptsContainingKey

    def _getDomIdContainingAttribute(self, soup, domType='div', attributeName='id', attributeContents='container'):
        """

        :param soup: a valid beautiful soup type
        :param domType:
        :param attributeContents:
        :return: list of matched dom elements.
        """
        try:
            return soup.find_all(domType, {attributeName:re.compile('^{}'.format(attributeContents))})
        except Exception as e:
            self.logger.info('######### [ScrapeUtilities]: Error getting DOM IDs containing attribute {}'.format(attributeContents))
            self.logger.exception(str(e))
            self.logger.info('######### [ScrapeUtilities]: End of stackTrace\n')

    def _soupAnUrl(self, targetUrl='http://www.google.com'):

        try:
            #Default agent is Crawler; most websites do not like it; wil result in 403 forbidden; hence state other agent.
            #headers = {'User-Agent':'Mozilla/5.0'}
            page = requests.get(targetUrl)
            soup = BeautifulSoup(page.text, "html.parser")
            soup.prettify()
            return soup

        except Exception as e:
            self.logger.info('######### [ScrapeUtilities]: Error soupifying {}'.format(targetUrl))
            self.logger.exception(str(e))
            self.logger.info('######### [ScrapeUtilities]: End of stackTrace\n')

    def _seekAllScriptsContainingKey(self, soup, key):

        try:
            scripts = soup.find_all('script', text=re.compile(key))
            return {
                'extractedScripts': scripts,
                'totalMatch': len(scripts)
            }
        except Exception as e:
            self.logger.info('######### [ScrapeUtilities]: Error scraping scripts for matching key: {}'.format(key))
            self.logger.exception(str(e))
            self.logger.info('######### [ScrapeUtilities]: End of stackTrace\n')


