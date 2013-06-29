import requests, cookielib, re
from urlparse import urlparse

DEFAULT_HOST        = 'http://localhost'
DEFAULT_COOKIE_NAME = ''
cookies = {'defaultCookie' : ''}
headers = {'defaultHeader' : ''}

def cleanURL(url):
    url = url.replace("\r\n", "")
    
    if ("?" in url):
        url = url.replace(" ", "")
    else:
        url = url.replace(" ", "?")

    return url

def getCSRFTokenFromHtml(respuestaHTML):
    csrf_token = ''
  
    m = re.search('var CSRF_TOKEN = \'(.+?)\'', respuestaHTML)
    if m:
        csrf_token = m.group(1)

    return csrf_token

def makePOST(url):
    print "*************************"
    url = cleanURL(url)

    parsed_path   = urlparse(url)
    URL           = DEFAULT_HOST + parsed_path[2]

    print "POST request to " + URL
    
    try:
        params = dict([p.split('=') for p in parsed_path[4].split('&')])
    except:
        params = {}

    print 'POST data:' 
    print params
    print 'headers:' 
    print headers
    print 'cookies:' 
    print cookies

    result = requests.post(URL, headers=headers, data=params, cookies=cookies

    print "*************************"
    return result

def makeGET(url):
    print "*************************"
    parsed_path   = urlparse(url)
    URL           = DEFAULT_HOST + parsed_path[2]

    print "GET request to " + URL

    result = requests.get(URL, headers=headers, cookies=cookies)

    print 'headers:' 
    print headers
    print 'cookies:' 
    print cookies
    print "*************************"
    return result

inputFile = open('headers.txt', 'r')
requestNumber = 0
for line in iter(inputFile):  
    key, value = line.split(' ',1)  

    requestNumber += 1

    if key == 'POST': 
        result = makePOST(value)
        requestFileName = 'results/POST/Result-'+str(requestNumber)+'.txt'
    elif key == 'GET':
        result = makeGET(value)
        requestFileName = 'results/GET/Result-'+str(requestNumber)+'.txt'    

    try:
      
      if result.status_code == 200 :
            print "Request OK status code is " + str(result.status_code)
            if (requestNumber==1):
                print "This is the first request we save cookies for future use in request headers:"   
                lItems = result.cookies.items()    
                headers = dict(lItems)
                print headers
      else:
            print "Request error status code is " + str(result.status_code)

      print "\n"

      html_result = result.text.encode('utf-8')      
      
      fsalida = open(requestFileName,'w')
      fsalida.write(html_result) 
      
      fsalida.close()
    except: 
      pass

inputFile.close()