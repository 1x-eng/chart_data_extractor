"""
Author: Pruthvi Kumar BK
Email: pruthvikumar.123@gmail.com
Date: 10 April, 2018

Utilities to scrape chart data from amcharts.

"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from chart_data_extractor.scrape_engine.scrape_utilities import ScrapeUtilities

class AmchartsScraper(ScrapeUtilities):

    def __init__(self):
        super(AmchartsScraper, self).__init__()

        __chrome_options = Options()
        __chrome_options.add_argument("--headless")
        __chrome_options.add_argument("--window-size=1920x1080")

        self.driver = webdriver.Chrome(chrome_options=__chrome_options)
        self.conventionalExtractor = self._extractor

    def _extractor(self, targetUrl):
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



if __name__ == '__main__':
    ams = AmchartsScraper()
    ams.conventionalExtractor(targetUrl='https://www.amcharts.com/demos/column-with-rotated-series/')