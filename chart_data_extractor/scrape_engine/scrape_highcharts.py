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
from chart_data_extractor.scrape_engine.scrape_utilities import ScrapeUtilities
import demjson

class HighchartsScraper(ScrapeUtilities):

    def __init__(self):
        super(HighchartsScraper, self).__init__()

        __chrome_options = Options()
        __chrome_options.add_argument("--headless")
        __chrome_options.add_argument("--window-size=1920x1080")

        self.driver = webdriver.Chrome(chrome_options=__chrome_options)
        self.seekUrl = self._seekUrl
        self.conventionalExtractor = self._extractor
        self.soupifiedExtractor = self._extractUsingSoup

    def _seekUrl(self, url):
        """
        Validate given URL to be alive!

        :param url:
        :return:
        """
        #TODO: Validate URL!
        return url

    def _extractor(self, targetUrl):
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
        #TODO: Validate how this reacts on dashboard full of charts' not just one chart per URL.
        try:
            #get DOM id hosting highcharts.
            soup = self.soupAnUrl(targetUrl)
            domIdHostingChart = soup.text.split("Highcharts.chart(")[1].split("'")[1]

            self.driver.get(self.seekUrl(targetUrl))
            chart_number = self.driver.find_element_by_id(domIdHostingChart).get_attribute('data-highcharts-chart')
            chart_data = self.driver.execute_script('var chartData = {}; '
                                                    'Highcharts.charts[' + chart_number + '].'
                                                    'series.map(function(chartContents, ix){ chartData[ix] = '
                                                    '{"seriesName": chartContents.name, "xAxisData" : chartContents.xData, '
                                                    '"yAxisData": chartContents.yData}}); return chartData;')
            return chart_data

        except Exception as e:
            print('#########[HighchartsScraper]: Error while scraping Highcharts from given URL -{} using '
                  'webdriver'.format(targetUrl))
            print(str(e))
            print('#########[HighchartsScraper]: End of stack trace')


    def _extractUsingSoup(self, targetUrl):

        def extractContentsFromJs(scriptContents):

            try:
                # get DOM id hosting highcharts.
                domIdHostingChart = scriptContents.text.split("Highcharts.chart(")[1].split("'")[1]

                chartData = scriptContents.text.split("Highcharts.chart('"+domIdHostingChart+"',")[1]
                chartData = chartData.split("});")[0] + '}'
                return demjson.decode(chartData)

            except Exception as e:
                print('######### [HighchartsScraper]: Error parsing JS')
                print(str(e))
                print('######### [HighchartsScraper]: End of stackTrace\n')

        try:
            soup = self.soupAnUrl(targetUrl)
            #Get all scripts executed by HighCharts that house data empowering the charts.
            scripts = self.seekAllScriptsContainingKey(soup, "Highcharts.chart")
            if (scripts['totalMatch'] >= 1):
                resultingContents = list(map(lambda script: extractContentsFromJs(script),
                                             scripts['extractedScripts']))
                return resultingContents
            else:
                print("[HighchartsScraper Logs]: There was no Highcharts Object found.")
                return ["NO Highcharts objects are found in the given URL."]

        except Exception as e:
            print('#########[HighchartsScraper]: Error while scraping Highcharts from given URL -{} '
                  'using soup'.format(targetUrl))
            print(str(e))
            print('#########[HighchartsScraper]: End of stack trace')


if __name__ == '__main__':
    he = HighchartsScraper()
    #print(he.conventionalExtractor('https://www.highcharts.com/demo/spline-inverted'))
    print(he.soupifiedExtractor('https://www.highcharts.com/demo/spline-inverted'))
