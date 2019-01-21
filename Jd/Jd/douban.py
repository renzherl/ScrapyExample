import requests
from lxml import html

url='https://movie.douban.com/'
page=requests.Session().get(url)
print page
tree=html.fromstring(page.text)
print tree
result=tree.xpath('//td[@class="title"]//a/text()')
print(result)

import urllib, urllib2
url_pre = 'http://www.baidu.com/s'
params = {}
params['wd'] = u'France'.encode('utf-8')
url_params = urllib.urlencode(params)
# url = '%s?%s' % (url_pre, url_params)
url = 'https://fresh.jd.com/'
response = urllib2.urlopen(url)
html = response.read()
with open('test.txt', 'w') as f:
    f.write(html)

url = 'https://item.jd.com/3927947.html'
response = urllib2.urlopen(url)
html = response.read()
with open('test_jd.txt', 'w') as f:
    f.write(html)