"""
Author: Pruthvi Kumar BK
Email: pruthvikumar.123@gmail.com
Date: 10 April, 2018

Utilities to scrape chart data from amcharts.

TODO: Make pipeline results same across both steps.
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scrape_engine.scrape_utilities import ScrapeUtilities
import json

class AmchartsScraper(ScrapeUtilities):

    def __init__(self):
        super(AmchartsScraper, self).__init__()

        __chrome_options = Options()
        __chrome_options.add_argument("--headless")
        __chrome_options.add_argument("--window-size=1920x1080")

        self.driver = webdriver.Chrome(chrome_options=__chrome_options)
        self.conventionalExtractor = self.__extractor
        self.soupifiedExtractor = self.__extractUsingSoup
        self.amcExtractor = self.__tryExtractingViaPipeline

    def __extractor(self, targetUrl):
        """
        Extractor to scrape data using selenium webdriver; returns an object of lists.
        Length of the list will be equivalent to the number of charts in the given URL.

        :param targetUrl:
        :return:
        """
        try:
            self.driver.get(targetUrl)
            chart_data = self.driver.execute_script('var chartData = {}; '
                                                'AmCharts.charts.map((el, ix) => {'
                                                    'chartData[ix] = el["dataProvider"]});'
                                                'return chartData;')
            return chart_data

        except Exception as e:
            print('#########[AmchartsScraper]: Error while scraping AmCharts from given URL -{} using '
                  'webdriver'.format(targetUrl))
            print(str(e))
            print('#########[AmchartsScraper]: End of stack trace')
            return {'message': 'Error while scraping AmCharts from target url using webdriver.'}


    def __extractUsingSoup(self, targetUrl):

        def extractContentsFromJs(scriptContents):

            try:
                chartData = scriptContents.text.split("dataProvider")[1][2:]
                chartData = json.loads(chartData.split("],")[0]+']')
                return chartData


            except Exception as e:
                print('######### [AmchartsScraper]: Error parsing JS')
                print(str(e))
                print('######### [AmchartsScraper]: End of stackTrace\n')

        try:
            soup = self.soupAnUrl(targetUrl)
            #Get all scripts executed by AmCharts that house data empowering the charts.
            scripts = self.seekAllScriptsContainingKey(soup, "AmCharts.makeChart")
            if (scripts['totalMatch'] >= 1):
                resultingContents = list(map(lambda script: extractContentsFromJs(script),
                                             scripts['extractedScripts']))
                return resultingContents
            else:
                print("[AmchartsScraper Logs]: There was no Amcharts Object found.")
                return {'message': 'No AmCharts object found in the given target URL'}

        except Exception as e:
            print('#########[AmchartsScraper]: Error while scraping Amcharts from given URL -{} '
                  'using soup'.format(targetUrl))
            print(str(e))
            print('#########[AmchartsScraper]: End of stack trace')
            return {'message': 'Error while scraping AmCharts from target url using Soup.'}


    def __tryExtractingViaPipeline(self, targetUrl):

        """
        Pipeline effort to try extracting via Selenium webdriver and Soupified extractor.
        :return:
        """
        try:
            extractedResults = {}
            # Step 1: Try Soupified extractor.
            soupifiedResults = self.__extractUsingSoup(targetUrl=targetUrl)

            if ((type(soupifiedResults) is dict and 'message' in soupifiedResults) or (type(soupifiedResults) is list
                                                                                      and (len(soupifiedResults) == 0
                                                                                       or None in soupifiedResults))):
                #Step 2: Try WebDriver extractor.
                webdriverResults = self.__extractor(targetUrl=targetUrl)
                if type(webdriverResults) is dict and 'message' in webdriverResults:
                    extractedResults['message'] = 'Our Pipeline is unable to scrape AmCharts from given URL. For further' \
                                                  'enquiry, please write to PK @ pruthvikumar.123@gmail.com with ' \
                                                  'valid subject line. (Eg. Unable to Scrape from http://www.abcd.com)'
                    extractedResults['status'] = 'Failure'
                    return extractedResults

                extractedResults['message'] = 'Successfully scraped AmCharts from given target URL'
                extractedResults['status'] = 'Success'
                extractedResults['scrapeResults'] = webdriverResults
                return extractedResults

            extractedResults['message'] = 'Successfully scraped AmCharts from given target URL'
            extractedResults['status'] = 'Success'
            extractedResults['scrapeResults'] = soupifiedResults
            return extractedResults


        except Exception as e:
            print('#########[AmchartsScraperPipeline]: Something did not work as expected in the pipeline for scraping'
                  'AmCharts. Stack trace to follow')
            print(str(e))
            print('#########[AmchartsScraperPipeline]: End of Stacktrace')
            return {
                'message': 'AmCharts scraper has failed to complete successfully.',
                'stackTrace': str(e),
                'hint': 'To facilitate debug and seek help, please report this message as is to PK '
                        '@ pruthvikumar.123@gmail.com. To facilitate quick response make sure to include subject line'
                        ' as: AmCharts Scraper Bug.'
            }



if __name__ == '__main__':
    ams = AmchartsScraper()
    print(ams.amcExtractor(targetUrl='https://www.worldcoinindex.com/coin/bitcoin'))