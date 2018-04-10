"""
Author: Pruthvi Kumar BK
Email: pruthvikumar.123@gmail.com
Date: 10 April, 2018

Utilities to scrape chart data from Highcharts.

References: Thanks to answer from here - https://stackoverflow.com/questions/43727621/converting-svg-from-highcharts-data-into-data-points
"""

from selenium import webdriver

class HighchartsScraper(object):

    def __init__(self):
        super(HighchartsScraper, self).__init__()
        self.driver = webdriver.Chrome()
        self.seekUrl = self._seekUrl
        self.getMetadata = self._getMetadata
        self.extractor = self._extractor

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
        chart_data = self.driver.execute_script('var chartData = {}; Highcharts.charts[' + chart_number + '].series.map(function(chartContents, ix){ chartData[ix] = {"seriesName": chartContents.name, "xAxisData" : chartContents.xData, "yAxisData": chartContents.yData}}); return chartData;')
        print(chart_data)


if __name__ == '__main__':
    he = HighchartsScraper()
    he.extractor('https://www.highcharts.com/demo/line-basic', {'penumtimate_dom_id': 'chart-container'})

