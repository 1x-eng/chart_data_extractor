# Chart Data Extractor - SDK | API
This Microservice will help scrape data out of chart(s) presented on any given website. (At this moment, i only support scrape from HighCharts and AmCharts. Other libraries will be included in the near future). 

This is a webService powered by Python(v3).

NOTE: THIS CODEBASE USES FALCON & GUNICORN TO FACILITATE WEB SERVICE. GUNICORN WORKS ONLY ON UNIX/LINUX MACHINES. HENCE, THIS WILL BE OPERATIONAL ONLY ON LINUX DISTRO'S /UNIX MACHINES. WINDOWS IMPLEMENTATION IS WIP.

# Features:

* REST services for extracting data via URL. 
* No heavy setup/Code addition required. 

# Setup:

* Clone this repo; ensure to cd into 'chart_Data_extractor' directory.
* pip install all the requirements (Python=3). (NOTE: Always better to create a dedicated virtual environment. Either using Anaconda /Conventional Python).
* To start the web service, type the following command (whilst staying on 'chart_Data_extractor' directory):

```python
gunicorn -b localhost:8000 scraper_service:app --threads 3 --reload
```

* The above command must start gunicorn server locally and listen on port 8000 (Please feel free to change this to your convinience).

* Go to webserver and check with this endpoint:
```
http://localhost:8000/
```

* To conduct scrape, try this endpoint:
```
http://localhost:8000/v1/chartDataExtractor?targetUrl=http://www.google.com
```


# Non-Developers:

If you are a business user, visit https://dextr.pruthvikumar.ml to check a more complete functional product. 

If you dont feel confident of backend development and want to use the webservice, you could use https://dextr-service.pruthvikumar.ml/v1/targetUrl=http://www.google.com (feel free to edit targetUrl to your choice) for a readily available backend service.

# Support:

For any issues write to Pruthvi @ pruthvikumar.123@gmail.com. Ensure to have a valid subject line, detailed message with appropriate stack trace to expect prompt/quick response.


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
