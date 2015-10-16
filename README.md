# Wegweiser

A pythonic geographic wikipedia spot scraper.

## Introduction

**Wegweiser** is a python package to get geographic data
(longitude, latitude, elevation) from wikipedia pages, favoured describing
spots (e.g. cities, mountains, lakes ...) . It provides functionality to create
simple [KML](https://developers.google.com/kml/) data and
[Google static maps](https://developers.google.com/maps/) url.

The package is based on three main classes:

* Search
	* Searchs a 'term' on wikipedia and returns a list of resulting urls.
* Scrape
	* Scrapes geographic data from an wikipedia page (url) describing any spot.
* Spot
	* Describes a spot containing _title_, _url_, _latitude_, _longitude_ and _elevation_.

Two further _output_ classes:

* Markup
	* Creates KML data from on one or more Spot objects.
* Map
	* Creates a Google static maps url from one or mor Spot objects.

Last but not least the package includes an example script _wegweiser_.

## Installation

Clone the repository.

	$ git clone https://github.com/tschaefer/wegweiser.git

Install the package and script.

	$ python setup.py install

## Usage

### Map of a single spot

Get the spot.

	$ spot = Spot.from_search('New York City')

Prepare the map.

	$ map = Map(spot, size=250x250, maptype='terrain')

Add spot as map marker.

	$ map.add_marker(spot, label='N')

Genrate and print URL to map.

	$ print map.generate_url()
	$ http://maps.google.com/maps/api/staticmap?maptype=terrain&format=png&size=640x400&sensor=false&markers=|label:N|40.7127777778,-74.0058333333

Save map as png.

	$ map.filename = new_york_city.png
	$ map.save_map_file()

![New York City](http://maps.google.com/maps/api/staticmap?maptype=terrain&format=png&size=640x400&sensor=false&markers=|label:N|40.7127777778,-74.0058333333 "New York City")

### Map and KML of multiple spots

	$ wegweiser map -l en -p -t terrain 'Mount Rushmore' 'Area 51' 'Golden Gate Bridge' https://en.wikipedia.org/wiki/Niagara_Falls -f sights.png

![Sights](http://tinyurl.com/c6q4haz "Sights")

	$ wegweiser markup -l en 'Mount Rushmore' 'Area 51' 'Golden Gate Bridge' https://en.wikipedia.org/wiki/Niagara_Falls -f sights.kml

KML code.

	<?xml version="1.0" encoding="UTF-8"?>
	<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2">
	    <Document id="feat_1">
	        <Folder id="feat_2">
	            <name>Wegweiser</name>
	            <Placemark id="feat_3">
	                <name>Mount Rushmore</name>
	                <Point id="geom_0">
	                    <coordinates>-103.459825,43.8789472222,0.0</coordinates>
	                </Point>
	            </Placemark>
	            <Placemark id="feat_4">
	                <name>Area 51</name>
	                <Point id="geom_1">
	                    <coordinates>-115.811111111,37.235,0.0</coordinates>
	                </Point>
	            </Placemark>
	            <Placemark id="feat_5">
	                <name>Golden Gate Bridge</name>
	                <Point id="geom_2">
	                    <coordinates>-122.478611111,37.8197222222,0.0</coordinates>
	                </Point>
	            </Placemark>
	            <Placemark id="feat_6">
	                <name>Niagara Falls</name>
	                <Point id="geom_3">
	                    <coordinates>-79.0711111111,43.08,0.0</coordinates>
	                </Point>
	            </Placemark>
	        </Folder>
	    </Document>
	</kml>
