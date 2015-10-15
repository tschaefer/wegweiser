# -*- coding: utf-8 -*-

import os
import unittest
import tempfile

from wegweiser.core import Search, Scrape, Spot
from wegweiser.markup import Markup
from wegweiser.map import Map


class BaseTest(unittest.TestCase):

    # object is from class
    def assertIs(self, obj, cls, msg=None):
        self.assert_(type(obj) is cls, msg)

    # member is in container
    def assertIn(self, member, container, msg=None):
        self.assert_(member in container, msg)

    # dictionaries are equal
    def assertDictEqual(self, dict1, dict2, msg=None):
        self.assertEqual(set(dict1.keys()), set(dict2.keys()), msg)
        self.assertEqual(sorted(dict1.values()), sorted(dict2.values()), msg)

    # dictionaries keys are equal
    def assertDictKeysEqual(self, dict1, dict2, msg=None):
        self.assertEqual(set(dict1.keys()), set(dict2.keys()), msg)

    # strings are equal
    def assertStrEqual(self, str1, str2, msg=None):
        self.assert_(str1 == str2, msg)


class CoreTest(BaseTest):

    def test_Search(self):

        # term
        search = Search('New York')
        self.assertIs(search, Search)
        # language
        search = Search('New York', language='en')
        self.assertIs(search, Search)
        self.assertRaises(ValueError, lambda: Search(
            'New York', language='it'))
        # limit
        search = Search('New York', limit=50)
        self.assertIs(search, Search)
        for limit in -1234, -1, 101, 356:
            self.assertRaises(ValueError, lambda: Search(
                'New York', limit=limit))

        search = Search('New York', language='en', limit=5)
        search.search_term()

        # results
        self.assertIs(search.results, list)
        dic = {
            'title': 'title',
            'url': 'url'
        }
        self.assertDictKeysEqual(search.results[0], dic)
        self.failUnlessRaises(
                AttributeError, setattr, search, "results", "set not allowed")
        # term
        self.assertIs(search.term, str)
        self.assertStrEqual(search.term, 'New York')
        self.failUnlessRaises(
            AttributeError, setattr, search, "term", "set not allowed")
        # language
        self.assertIs(search.language, str)
        self.assertStrEqual(search.language, 'en')
        self.failUnlessRaises(
            AttributeError, setattr, search, "language", "set not allowed")
        # limit
        self.assertIs(search.limit, int)
        self.assertEqual(search.limit, 5)
        self.failUnlessRaises(
            AttributeError, setattr, search, "limit", "set not allowed")

    def test_Scrape(self):

        # url
        scrape = Scrape('http://en.wikipedia.org/wiki/New_York_City')
        self.assertIs(scrape, Scrape)
        urls = [
            'http://it.wikipedia.org/wiki/New_York_City',
            'http://de.wikipedia.org/wiki/',
            'http://www.google.de/'
        ]
        for url in urls:
            self.assertRaises(ValueError, lambda: Scrape(url))
        scrape = Scrape('http://en.wikipedia.org/wiki/Python')
        self.assertRaises(UserWarning, lambda: scrape.scrape_url())

        scrape = Scrape('http://en.wikipedia.org/wiki/New_York_City')
        scrape.scrape_url()
        scrape = Scrape('http://en.wikipedia.org/wiki/Moscow')
        scrape.scrape_url()
        scrape = Scrape('http://de.wikipedia.org/wiki/New_York_City')
        scrape.scrape_url()

        # url
        self.assertIs(scrape.url, str)
        self.failUnlessRaises(
            AttributeError, setattr, scrape, "url", "set not allowed")
        # title
        self.assertIs(scrape.title, str)
        self.failUnlessRaises(
            AttributeError, setattr, scrape, "title", "set not allowed")
        # latitude
        self.assertIs(scrape.latitude, float)
        self.failUnlessRaises(
            AttributeError, setattr, scrape, "latitude", "set not allowed")
        # longitude
        self.assertIs(scrape.longitude, float)
        self.failUnlessRaises(
            AttributeError, setattr, scrape, "longitude", "set not allowed")
        # elevation
        self.assertIs(scrape.elevation, float)
        self.failUnlessRaises(
            AttributeError, setattr, scrape, "elevation", "set not allowed")

    def test_Spot(self):

        spot = Spot()
        self.assertIs(spot, Spot)
        spot = Spot(
            title='New York', latitude=-74.0058333333,
            longitude=40.7127777778, elevation=10.0,
            url='http://de.wikipedia.org/wiki/New_York_City')
        self.assertIs(spot, Spot)

        # url
        self.assertIs(spot.url, str)
        self.failUnlessRaises(
            AttributeError, setattr, spot, "url", "set not allowed")
        # title
        self.assertIs(spot.title, str)
        self.failUnlessRaises(
            AttributeError, setattr, spot, "title", "set not allowed")
        # latitude
        self.assertIs(spot.latitude, float)
        self.failUnlessRaises(
            AttributeError, setattr, spot, "latitude", "set not allowed")
        # longitude
        self.assertIs(spot.longitude, float)
        self.failUnlessRaises(
            AttributeError, setattr, spot, "longitude", "set not allowed")
        # elevation
        self.assertIs(spot.elevation, float)
        self.failUnlessRaises(
            AttributeError, setattr, spot, "elevation", "set not allowed")

        # search
        spot = Spot.from_search(Search('New York'))
        self.assertIs(spot, Spot)
        self.assertRaises(
            ValueError, lambda: Spot.from_search(
                Scrape('http://de.wikipedia.org/wiki/New_York_City')))
        # scrape
        spot = Spot.from_scrape(
            Scrape('http://de.wikipedia.org/wiki/New_York_City'))
        self.assertIs(spot, Spot)
        self.assertRaises(
            ValueError, lambda: Spot.from_scrape(Search('New York City')))


class MarkupTest(BaseTest):

    def setUp(self):
        self.tmpfile = tempfile.NamedTemporaryFile(suffix='.kml')
        self.tmpfile.close()

    def test_Markup(self):

        markup = Markup()
        self.assertIs(markup, Markup)
        markup = Markup(title='NewYorkCity', filename=self.tmpfile.name)
        self.assertIs(markup, Markup)

        # add_spot
        self.assertRaises(ValueError, lambda: markup.add_spot(
            Search('New York City')))
        # generate_kml
        markup.add_spot(Spot.from_search(
            Search('New York City')))
        markup.generate_kml()  # latitude, longitude, elevation
        markup.add_spot(
            Spot.from_search(Search('New York City', language='en')))
        markup.generate_kml()  # latitude, longitude
        # save_kml_file
        markup.save_kml_file()

        # title
        self.assertIs(markup.title, str)
        self.failUnlessRaises(
            AttributeError, setattr, markup, "title", "set not allowed")
        # spots
        self.assertIs(markup.spots, list)
        self.failUnlessRaises(
            AttributeError, setattr, markup, "spots", "set not allowed")
        # filename
        self.assertIs(markup.filename, str)
        markup.filename = 'filename'
        self.assertStrEqual(markup.filename, 'filename')

    def tearDown(self):
        os.remove(self.tmpfile.name)


class MapTest(BaseTest):

    def setUp(self):
        self.tmpfile = tempfile.NamedTemporaryFile(suffix='.kml')
        self.tmpfile.close()

    def test_Map(self):

        map = Map()
        self.assertIs(map, Map)
        map = Map(filename=self.tmpfile.name)
        self.assertIs(map, Map)

        # add_marker
        self.assertRaises(ValueError, lambda: map.add_marker(Search(
            'New York City')))
        map.add_marker(Spot.from_search(Search('New York City')))
        map.save_map_file()

        # spots
        self.assertIs(map.spots, list)
        self.failUnlessRaises(
            AttributeError, setattr, map, "spots", "set not allowed")
        # filename
        self.assertIs(map.filename, str)
        map.filename = 'filename'
        self.assertStrEqual(map.filename, 'filename')

    def tearDown(self):
        os.remove(self.tmpfile.name)

if __name__ == '__main__':
    unittest.main()
