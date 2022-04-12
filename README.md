# Chart Data Extractor - SDK | API
This webservice will help scrape data out of chart(s) presented on any given website. (At this moment, I only support scrape from HighCharts and AmCharts. Other libraries, maybe next time). 

NOTE: uses gunicorn (https://docs.gunicorn.org/en/stable/index.html) which is WSGI HTTP server for `*nix` systems. On windows, you might want to swap gunicorn with uWSGI or other alternatives.

# Features:

* REST services for extracting data via URL. 
* Simpler to get started. 

# Getting Started:

* Clone this repo > `cd chart_data_extractor.
* `pip install -r requirements.txt` in cenv of your choice (py=3)

```python
gunicorn -b localhost:8000 scraper_service:app --threads 3 --reload
```

* To extract data from a (supported)chart, try this:
```
http://localhost:8000/v1/chartDataExtractor?targetUrl=http://www.google.com
```


---------
MIT License

Copyright (c) 2018 Pruthvi Kumar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE. 
