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
from bs4 import BeautifulSoup
from chart_data_extractor.scrape_engine.scrape_utilities import ScrapeUtilities

class HighchartsScraper(ScrapeUtilities):

    def __init__(self):
        super(HighchartsScraper, self).__init__()

        __chrome_options = Options()
        __chrome_options.add_argument("--headless")
        __chrome_options.add_argument("--window-size=1920x1080")

        self.driver = webdriver.Chrome(chrome_options=__chrome_options)
        self.seekUrl = self._seekUrl
        self.getMetadata = self._getMetadata
        self.extractor = self._extractor
        self.extractUsingSoup = self._extractUsingSoup

    def _seekUrl(self, url):
        """
        Validate given URL to be alive!

        :param url:
        :return:
        """
        #TODO: Validate URL!
        return url

    def _getMetadata(self, meta):
        """
        Metadata defining steps to reach the dom element that contains chart.

        :param meta:
        :return:
        """
        #TODO: Unpack metadata and accordingly design steps to reach the desired DOM element.
        return

    def _extractor(self, url, meta):
        """
        Extractor to scrape data in the following format:

        {
            seriesName: '...',
            xAxisData: [,,,],
            yAxisData: [,,,] //Missing data will be 'None'
        }

        :param url:
        :param meta:
        :return:
        """
        #TODO: Define steps to reach the actual dom element containing the data. These steps to be driven by metadata.

        self.driver.get(self.seekUrl(url))
        chart_number = self.driver.find_element_by_id('container').get_attribute('data-highcharts-chart')
        chart_data = self.driver.execute_script('var chartData = {}; '
                                                'Highcharts.charts[' + chart_number + '].'
                                                'series.map(function(chartContents, ix){ chartData[ix] = '
                                                '{"seriesName": chartContents.name, "xAxisData" : chartContents.xData, '
                                                '"yAxisData": chartContents.yData}}); return chartData;')
        print(chart_data)


    def _extractUsingSoup(self, targetUrl):

        soup = self.soupAnUrl(targetUrl)
        #Get all scripts executed by HighCharts that house data empowering the charts.
        scripts = self.seekAllScriptsContainingKey(soup, "Highcharts.chart")
        #TODO: Extract contents/desired data from within these scripts.


if __name__ == '__main__':
    he = HighchartsScraper()
    #he.extractor('https://www.highcharts.com/demo/line-basic', {'penumtimate_dom_id': 'chart-container'})
    he.extractUsingSoup('https://www.highcharts.com/demo/line-basic')
