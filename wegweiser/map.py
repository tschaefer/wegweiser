import urllib
from motionless import DecoratedMap, LatLonMarker
from wegweiser.core import Spot

class Map(DecoratedMap):

	def __init__(self, size_x=400, size_y=400, maptype='roadmap', region=False, fillcolor='green', pathweight=None, pathcolor=None, filename=None):
		DecoratedMap.__init__(self, size_x=size_x, size_y=size_y, maptype=maptype, region=region, fillcolor=fillcolor, pathweight=None, pathcolor=None)
		self._filename = filename
		self._spots = []

	def add_marker(self, spot, size=None, color=None, label=None):
		if not isinstance(spot, Spot):
			raise ValueError("Spot object required")
		self._spots.append(spot)
		self.markers.append(LatLonMarker(spot.latitude, spot.longitude, size, color, label))

	def save_map_file(self):
		url = self.generate_url()
		urllib.urlretrieve(url, self._filename)

	@property
	def spots(self):
		return self._spots

	@property
	def filename(self):
		return self._filename

	@filename.setter
	def filename(self, filename):
		self._filename = filename
