"""
Author: Pruthvi Kumar BK
Email: pruthvikumar.123@gmail.com
Date: 10 April, 2018

Utilities to scrape chart data from Highcharts.

References: Thanks to answer from here - https://stackoverflow.com/questions/43727621/converting-svg-from-highcharts-data-into-data-points

Must have pre-requisites: 1. Chrome must be installed
                          2. Chrome-driver must be installed (Refer - https://gist.github.com/thotmx/046b6fa582f0725dc783)
                          3. Chrome driver must be available in the path (One way to check will be go to cmd and enter
                          chromedriver. Should you see an error, that means, chrome driver is not available in the path.
                          In the above link (point 2), refer to step which does sudo ln -s. This step creates a soft link
                          from the chrome-driver's installed path to /usr/bin/chromedriver.


"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scrape_engine.scrape_utilities import ScrapeUtilities
from utilities.utilities import MyUtilities
import demjson

class HighchartsScraper(ScrapeUtilities, MyUtilities):

    def __init__(self):
        super(HighchartsScraper, self).__init__()

        __chrome_options = Options()
        __chrome_options.add_argument("--headless")
        __chrome_options.add_argument("--window-size=1920x1080")

        self.driver = webdriver.Chrome(chrome_options=__chrome_options)
        self.seekUrl = self.__seekUrl
        self.conventionalExtractor = self.__extractor
        self.soupifiedExtractor = self.__extractUsingSoup
        self.hcExtractor = self.__tryExtractingViaPipeline

        self.logger = self.getLogger(logFileName='pk_scraperService_highChartsScraper',
                                     logFilePath='./logs/pk_scraperService_highChartsScraper.log')

    def __seekUrl(self, url):
        """
        Validate given URL to be alive!

        :param url:
        :return:
        """
        #TODO: Validate URL!
        return url

    def __extractor(self, targetUrl):
        """
        Extractor to scrape data in the following format:

        {
            seriesName: '...',
            xAxisData: [,,,],
            yAxisData: [,,,] //Missing data will be 'None'
        }

        :param targetUrl:
        :param meta:
        :return:
        """
        try:
            #get DOM id hosting highcharts.
            self.driver.get(self.seekUrl(targetUrl))
            chartElements = self.driver.find_elements_by_class_name('highcharts-container')
            chartIds = list(map( lambda ce: ce.find_element_by_xpath('..')
                                               .get_attribute('data-highcharts-chart'), chartElements))

            chartDataStore = list(map(lambda cid: self.driver.execute_script('var chartData = {}; '
                                            'Highcharts.charts[' + cid + '].'
                                            'series.map(function(chartContents, ix){ chartData[ix] = '
                                            '{"seriesName": chartContents.name, "xAxisData" : chartContents.xData, '
                                            '"yAxisData": chartContents.yData}}); return chartData;'), chartIds))

            return chartDataStore

        except Exception as e:
            self.logger.info('#########[HighchartsScraper]: Error while scraping Highcharts from given URL -{} using '
                  'webdriver'.format(targetUrl))
            self.logger.exception(str(e))
            self.logger.info('#########[HighchartsScraper]: End of stack trace')
            return {'message': 'Error while scraping Highcharts from target url using webdriver.'}


    def __extractUsingSoup(self, targetUrl):

        def extractContentsFromJs(scriptContents):

            try:
                # get DOM id hosting highcharts.
                domIdHostingChart = scriptContents.text.split("Highcharts.chart(")[1].split("'")[1]

                chartData = scriptContents.text.split("Highcharts.chart('"+domIdHostingChart+"',")[1]
                chartData = chartData.split("});")[0] + '}'
                return demjson.decode(chartData)

            except Exception as e:
                self.logger.info('######### [HighchartsScraper]: Error parsing JS')
                self.logger.exception(str(e))
                self.logger.info('######### [HighchartsScraper]: End of stackTrace\n')

        try:
            soup = self.soupAnUrl(targetUrl)
            #Get all scripts executed by HighCharts that house data empowering the charts.
            scripts = self.seekAllScriptsContainingKey(soup, "Highcharts.chart")
            if (scripts['totalMatch'] >= 1):
                resultingContents = list(map(lambda script: extractContentsFromJs(script),
                                             scripts['extractedScripts']))
                return resultingContents
            else:
                self.logger.info("[HighchartsScraper Logs]: There was no Highcharts Object found.")
                return {'message': 'No Highcharts object found in the given target URL'}

        except Exception as e:
            self.logger.info('#########[HighchartsScraper]: Error while scraping Highcharts from given URL -{} '
                  'using soup'.format(targetUrl))
            self.logger.exception(str(e))
            self.logger.info('#########[HighchartsScraper]: End of stack trace')
            return {'message': 'Error while scraping Highcharts from target url using Soup.'}


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
                    extractedResults['message'] = 'Our Pipeline is unable to scrape Highcharts from given URL. For further' \
                                                  'enquiry, please write to PK @ pruthvikumar.123@gmail.com with ' \
                                                  'valid subject line. (Eg. Unable to Scrape from http://www.abcd.com)'
                    extractedResults['status'] = 'Failure'
                    return extractedResults

                extractedResults['message'] = 'Successfully scraped Highcharts from given target URL'
                extractedResults['status'] = 'Success'
                extractedResults['scrapeResults'] = webdriverResults
                return extractedResults

            extractedResults['message'] = 'Successfully scraped Highcharts from given target URL'
            extractedResults['status'] = 'Success'
            extractedResults['scrapeResults'] = soupifiedResults
            return extractedResults


        except Exception as e:
            self.logger.info('#########[HighchartsScraperPipeline]: Something did not work as expected in the pipeline for scraping'
                  'HighCharts. Stack trace to follow')
            self.logger.exception(str(e))
            self.logger.info('#########[HighchartsScraperPipeline]: End of Stacktrace')
            return {
                'message': 'HighCharts scraper has failed to complete successfully.',
                'stackTrace': str(e),
                'hint': 'To facilitate debug and seek help, please report this message as is to PK '
                        '@ pruthvikumar.123@gmail.com. To facilitate quick response make sure to include subject line'
                        ' as: HighCharts Scraper Bug.'
            }


if __name__ == '__main__':
    he = HighchartsScraper()
    #print(he.conventionalExtractor('https://www.marketwatch.com/investing/future/nasdaq%20100%20futures'))
    #print(he.soupifiedExtractor('https://www.moneycontrol.com/sensex/bse/sensex-live'))
    print(he.hcExtractor('https://www.marketwatch.com/investing/future/nasdaq%20100%20futures'))