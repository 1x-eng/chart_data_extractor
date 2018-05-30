"""
Author: Pruthvi Kumar BK
Date: May 29, 2018

Set of utilities to assist in scraping contents of a web page.
"""
from bs4 import BeautifulSoup
import re
import requests
import demjson

class ScrapeUtilities(object):

    def __init__(self):
        super(ScrapeUtilities, self).__init__()
        self.soupAnUrl = self._soupAnUrl
        self.getDomIdContainingAttribute = self._getDomIdContainingAttribute
        self.seekAllScriptsContainingKey = self._seekAllScriptsContainingKey
        self.extractContentsFromJs = self._extractContentsFromJs

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
            print('######### [ScrapeUtilities]: Error getting DOM IDs containing attribute {}'.format(attributeContents))
            print(str(e))
            print('######### [ScrapeUtilities]: End of stackTrace\n')

    def _soupAnUrl(self, targetUrl='http://www.google.com'):

        try:
            #Default agent is Crawler; most websites do not like it; wil result in 403 forbidden; hence state other agent.
            #headers = {'User-Agent':'Mozilla/5.0'}
            page = requests.get(targetUrl)
            soup = BeautifulSoup(page.text, "html.parser")
            soup.prettify()
            return soup

        except Exception as e:
            print('######### [ScrapeUtilities]: Error soupifying {}'.format(targetUrl))
            print(str(e))
            print('######### [ScrapeUtilities]: End of stackTrace\n')

    def _seekAllScriptsContainingKey(self, soup, key):

        try:
            scripts = soup.find_all('script', text=re.compile(key))
            return {
                'extractedScripts': scripts,
                'totalMatch': len(scripts)
            }
        except Exception as e:
            print('######### [ScrapeUtilities]: Error scraping scripts for matching key: {}'.format(key))
            print(str(e))
            print('######### [ScrapeUtilities]: End of stackTrace\n')


    def _extractContentsFromJs(self, scriptContents):

        try:

            chartData = scriptContents.text.split("Highcharts.chart('container',")[1]
            chartData = chartData.split("});")[0] + '}'
            return demjson.decode(chartData)

        except Exception as e:
            print('######### [ScrapeUtilities]: Error parsing JS')
            print(str(e))
            print('######### [ScrapeUtilities]: End of stackTrace\n')


if __name__ == '__main__':
    su = ScrapeUtilities()
    soupifiedPage = su.soupAnUrl('https://www.highcharts.com/demo/line-basic')
    print(su.getDomIdContainingAttribute(soupifiedPage, attributeName='data-highcharts-chart', attributeContents='0'))


