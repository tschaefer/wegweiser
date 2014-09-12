import re
import urllib2
from cStringIO import StringIO
from xml.etree import ElementTree

agent = urllib2.build_opener()
agent.addheaders = [('User-agent', 'Mozilla/5.0')]

class Search(object):

	LANGUAGES = ['de', 'en', 'fr']
	BASE_URL = 'http://%s.wikipedia.org/w/api.php?action=opensearch&search=%s&format=xml&limit=%s'
	LIMIT = range(1,100)
	NAMESPACE = '{http://opensearch.org/searchsuggest2}'

	def __init__(self, term, language='de', limit=3):
		if language not in Search.LANGUAGES:
			raise ValueError("'%s' no valid language %s" % (language, Search.LANGUAGES))
		if limit not in Search.LIMIT:
			raise ValueError("'%d' no valid limit [%s]" % (limit, "1-100"))
		self._term = term
		self._language = language
		self._limit = limit
		self._results = []

	def search_term(self):
		url = Search.BASE_URL % (self._language, self._term.replace(" ", "%20") , self._limit)
		fd = agent.open(url)
		content = fd.read()
		self._evaluate_result(content)

	def _evaluate_result(self, content):
		tree = ElementTree.parse(StringIO(content))
		items = tree.findall('%sSection/%sItem' % (Search.NAMESPACE, Search.NAMESPACE))
		for item in items:
			title = item.find('%sText' % Search.NAMESPACE)
			url = item.find('%sUrl' % Search.NAMESPACE)
			entry = {
				'title': title.text,
				'url': url.text,
			}
			self._results.append(entry)

	@property
	def results(self):
		return self._results

	@property
	def term(self):
		return self._term

	@property
	def language(self):
		return self._language

	@property
	def limit(self):
		return self._limit

class Scrape(object):

	URL_OPTS = '%s?printable=yes'

	def __init__(self, url):
		pattern = re.compile(r'^http://(de|en|fr).wikipedia.org/wiki/.+')
		if not pattern.match(url):
			raise ValueError("'%s' no valid URL" % url)
		self._url = url
		self._title = None
		self._latitude = None
		self._longitude = None
		self._elevation = None

	def scrape_url(self):
		url = Scrape.URL_OPTS % self.url
		fd = agent.open(url)
		content = fd.read()
		tree = ElementTree.parse(StringIO(content))
		root = tree.getroot()
		tags = root.getiterator(tag='span')
		for tag in tags:
			if 'dir' in tag.attrib:
				if tag.attrib['dir'] == 'auto':
					title = tag.text
			if 'class' in tag.attrib:
				if tag.attrib['class'] == 'latitude':
					if 'latitude' in locals():
						continue
					latitude = tag.text
				if tag.attrib['class'] == 'longitude':
					if 'longitude' in locals():
						continue
					longitude = tag.text
				if tag.attrib['class'] == 'elevation':
					if 'elevation' in locals():
						continue
					elevation = tag.text
		if 'latitude' not in locals() or 'longitude' not in locals():
			raise UserWarning("'%s' no valid geographic spot" % title)
		if 'en.wikipedia.org' in self.url:
			latitude = self._calculate_decimal_degree(latitude)
			longitude = self._calculate_decimal_degree(longitude)
		self._title = title
		self._latitude = float(latitude)
		self._longitude = float(longitude)
		if 'elevation' in locals():
			self._elevation = float(elevation)

	def _calculate_decimal_degree(self, coordinates):
		coordinates = coordinates.replace(u'°', ' ').replace(u'′', ' ').replace(u'″', ' ')
		length = len(coordinates.split())
		if length == 4:
			degree, minutes, seconds, orientation =  coordinates.split()
		elif length == 3:
			degree, minutes, orientation =  coordinates.split()
		else:
			raise UserWarning("'%s' no valid geographic spot" % self.title)
		if 'seconds' not in locals():
			coordinates = (float(minutes) / 60) + int(degree)
		else:
			coordinates = (((float(seconds) / 60) + float(minutes)) / 60) + int(degree)
		if 'W' in orientation or 'S' in orientation:
			coordinates *= (-1)
		return coordinates

	@property
	def url(self):
		return self._url

	@property
	def title(self):
		return self._title

	@property
	def latitude(self):
		return self._latitude

	@property
	def longitude(self):
		return self._longitude

	@property
	def elevation(self):
		return self._elevation

class Spot(object):

	def __init__(self, title=None, latitude=None, longitude=None, elevation=None, url=None):
		self._title = title
		self._latitude = latitude
		self._longitude = longitude
		self._elevation = elevation
		self._url = url

	@classmethod
	def from_scrape(cls, scrape):
		if not isinstance(scrape, Scrape):
			raise ValueError("Scrape object required")
		scrape.scrape_url()
		cls = cls(title=scrape.title, latitude=scrape.latitude, longitude=scrape.longitude, elevation=scrape.elevation, url=scrape.url)
		return cls

	@classmethod
	def from_search(cls, search):
		if not isinstance(search, Search):
			raise ValueError("Search object required")
		search.search_term()
		result = search.results[0]
		scrape = Scrape(result['url'])
		cls = Spot.from_scrape(scrape)
		return cls

	@property
	def title(self):
		return self._title

	@property
	def url(self):
		return self._url

	@property
	def latitude(self):
		return self._latitude

	@property
	def longitude(self):
		return self._longitude

	@property
	def elevation(self):
		return self._elevation
