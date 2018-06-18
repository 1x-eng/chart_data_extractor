"""
Author: Pruthvi Kumar BK
Email: pruthvikumar.123@gmail.com
Date: 10 April, 2018

Extractor is the main entrypoint file that is associated with all relevant & respective callables.

"""

from chart_data_extractor.scrape_engine.scrape_amcharts import AmchartsScraper
from chart_data_extractor.scrape_engine.scrape_highcharts import HighchartsScraper

class ChartsDataExtractor(AmchartsScraper, HighchartsScraper):

    def __init__(self):
        super(ChartsDataExtractor, self).__init__()
        self.executePipeline = self._extractionPipeline


    def _extractionPipeline(self, targetUrl):
        """

        :param targetUrl:
        :return:
        """
        #Step 1: Identify type of charts present.
        supportedChartingFrameworks = ['Amcharts', 'Highcharts']
        soupifiedText = self.soupAnUrl(targetUrl).text
        chartsStatus = list(map(lambda cf: cf in soupifiedText or cf.lower() in soupifiedText
                                          or cf.upper() in soupifiedText, supportedChartingFrameworks))

        if (chartsStatus[0]):
            return self.amcExtractor(targetUrl)
        elif (chartsStatus[1]):
            return self.hcExtractor(targetUrl)
        else:
            return {'message': 'There is either no Charts in the given URL or there is one that is not yet supported.'
                               'At this moment, we are supporting only Amcharts and Highcharts. If you have any '
                               'other library that you think should be prioritized for next release, please write to '
                               'PK @ pruthvikumar.123@gmail.com with valid subject line (eg. Scraper Support - Please '
                               'extend support for charting library "xyz"'}




if __name__ == '__main__':
    cde = ChartsDataExtractor()
    print(cde.executePipeline('https://www.highcharts.com/demo/line-basic'))
