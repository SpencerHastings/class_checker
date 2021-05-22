import requests

from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

retry_strategy = Retry(
    total=99999,
    status_forcelist=[429, 500, 502, 503, 504],
    method_whitelist=["HEAD", "GET", "OPTIONS"]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
http = requests.Session()
http.mount("https://", adapter)
http.mount("http://", adapter)

cookies = {
    '_ga': 'GA1.2.1629102257.1557290941',
}

courseheaders = {
    'Origin': 'http://saasta.byu.edu',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Referer': 'http://saasta.byu.edu/noauth/classSchedule/index.php',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
}

sectionheaders = {
    'Origin': 'http://saasta.byu.edu',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Referer': 'http://saasta.byu.edu/noauth/classSchedule/index.php',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
}

# sessionId = 'AAJ2IA0AEXPQHXCS0XDN'
sessionId = 'AAJ2AA0AEXPQHHHS0XDN'


def getCourses(yearterm):
    data = {
        'searchObject[yearterm]': yearterm,
        'sessionId': sessionId
    }

    return http.post('http://saasta.byu.edu/noauth/classSchedule/ajax/getClasses.php',
                     headers=courseheaders,
                     cookies=cookies,
                     data=data,
                     verify=False)


def getSections(yearterm, courseID):
    data = {
        'courseId': courseID,
        'sessionId': sessionId,
        'yearterm': yearterm,
        'no_outcomes': 'true'
    }

    return http.post('http://saasta.byu.edu/noauth/classSchedule/ajax/getSections.php',
                     headers=sectionheaders,
                     cookies=cookies,
                     data=data,
                     verify=False)
