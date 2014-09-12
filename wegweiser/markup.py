import simplekml
from wegweiser.core import Spot

class Markup(object):

	def __init__(self, title='Wegweiser', filename=None):
		self._title = title
		self._filename = filename
		self._spots = []

	def add_spot(self, spot):
		if not isinstance(spot, Spot):
			raise ValueError("Spot object required")
		self._spots.append(spot)

	def generate_kml(self):
		self._kml = simplekml.Kml()
		folder = self._kml.newfolder(name=self.title)
		for spot in self.spots:
			point = folder.newpoint()
			point.name = spot.title
			if spot.elevation is not None:
				point.coords = [(spot.longitude, spot.latitude, spot.elevation)]
			else:
				point.coords = [(spot.longitude, spot.latitude)]
		return self._kml.kml()

	def save_kml_file(self):
		self.generate_kml()
		self._kml.save(self._filename)

	@property
	def title(self):
		return self._title

	@property
	def spots(self):
		return self._spots

	@property
	def filename(self):
		return self._filename

	@filename.setter
	def filename(self, filename):
		self._filename = filename
