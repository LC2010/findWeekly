# -*- coding: utf-8 -*-

import urllib
import xml.dom.minidom
import re
import datetime

theQuery = u"{query}"
# theQuery = "CSS"
theQuery = theQuery.lower().strip()

rssMap = {
	"js" : {"name": "javascript", "key":"http://bcs.duapp.com/weekly/weekly.xml?sign=MBO:A8cdd3a284851538baf8a4f57d463da8:6pYv3rOvfNfMmYBmuUOat4ql6XY%3D&response-content-disposition=filename*=utf8''weekly.xml&response-cache-control=private", "reg": '<p class="smaller header"[^>]*><a href="([^"]*)"'},
	"h5":  {"name": "html5", "key": "http://bcs.duapp.com/weekly/h5.xml?sign=MBO:A8cdd3a284851538baf8a4f57d463da8:YF%2FvM3jY%2BguxoUFUNzBtJ%2F7BJz8%3D&response-content-disposition=filename*=utf8''h5.xml&response-cache-control=private", "reg": '<a href="([^"]*)" style="color: #1173c7">Read this on the Web</a>'},
	"css": {"name": "css", "key": "http://css-weekly.com/feed/" },
}
urldoc = xml.dom.minidom.parse(urllib.urlopen(rssMap[theQuery]['key']))


print "<?xml version=\"1.0\"?>\n<items>"
for item in urldoc.getElementsByTagName('item'):
	title = item.getElementsByTagName('title')[0].firstChild.data
	title = u"%s周刊第%s期" % (rssMap[theQuery]['name'], re.search('Issue #?(\d+)', title).group(1))

	if theQuery == 'css':
		link = item.getElementsByTagName('link')[0].firstChild.data
	else:
		content = item.getElementsByTagName('content:encoded')[0].firstChild.data
		link = re.search(rssMap[theQuery]['reg'], content)
		if link is not None:
			link = link.group(1)
		else:
			link = ''

	pubDate = item.getElementsByTagName('pubDate')[0].firstChild.data
	pubDate = datetime.datetime.strptime(pubDate,'%a, %d %b %Y %H:%M:%S +0000')
	pubDate = pubDate.strftime("%Y年%m月%d日 %H:%M:%S").decode('utf-8')
	pubDate = u"发布日期为:%s" % pubDate

	print "    <item uid=\"weekly\" arg=\""+ link +"\">"
	print "        <title>" + title.encode('utf-8') + "</title>"
	print "        <subtitle>" + pubDate.encode('utf-8') + "</subtitle>"
	print '''        <icon>2D5B3243-1F61-4C63-A2AB-320C51DC6FB2.png</icon>\n    </item>'''
print "</items>\n"

