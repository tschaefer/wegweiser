# -*- coding: utf-8 -*-

import sys
import argparse
import re
import json

from wegweiser.core import Spot, Search, Scrape
from wegweiser.markup import Markup
from wegweiser.map import Map


def parse_options():
    parser = argparse.ArgumentParser(
        description='A python wikipedia geo spot scraper.')
    subparsers = parser.add_subparsers()
    # parser json
    parser_json = subparsers.add_parser('json')
    parser_json.set_defaults(json=True)
    parser_json.add_argument(
        'wikiobj',
        type=str,
        nargs='+',
        help='wikipedia url or search term'
    )
    parser_json.add_argument(
        '-f', '--filename',
        type=str,
        default=None,
        help='write JSON to file'
    )
    parser_json.add_argument(
        '-l', '--language',
        type=str,
        choices=['de', 'en', 'fr'],
        default='de',
        help='select wikipedia language'
    )
    # parser markup
    parser_markup = subparsers.add_parser('markup')
    parser_markup.set_defaults(markup=True)
    parser_markup.add_argument(
        'wikiobj',
        type=str,
        nargs='+',
        help='wikipedia url or search term'
    )
    parser_markup.add_argument(
        '-f', '--filename',
        type=str,
        default=None,
        help='write KML to file'
    )
    parser_markup.add_argument(
        '-l', '--language',
        type=str,
        choices=['de', 'en', 'fr'],
        default='de',
        help='select wikipedia language'
    )
    # parser map
    parser_map = subparsers.add_parser('map')
    parser_map.set_defaults(map=True)
    parser_map.add_argument(
        'wikiobj',
        type=str,
        nargs='+',
        help='wikipedia url or search term'
    )
    parser_map.add_argument(
        '-f', '--filename',
        type=str,
        default=None,
        help='save GMAP to file'
    )
    parser_map.add_argument(
        '-l', '--language',
        type=str,
        choices=['de', 'en', 'fr'],
        default='de',
        help='select wikipedia language'
    )
    parser_map.add_argument(
        '-p', '--path',
        action='store_true',
        help='connect markers'
    )
    parser_map.add_argument(
        '-r', '--region',
        action='store_true',
        help='fill region'
    )
    parser_map.add_argument(
        '-s', '--size',
        type=str,
        default='640x400',
        help='map size in pixel'
    )
    parser_map.add_argument(
        '-t', '--type',
        type=str,
        choices=['roadmap', 'satellite', 'terrain', 'hybrid'],
        default='roadmap',
        help='type of map to construct'
    )
    # parse and return options
    return parser.parse_args()


def get_spots(wikiobj, language):
    wiki_url_pattern = re.compile(
        r'^https://(de|en|fr).wikipedia.org/wiki/.+'
    )
    spots = []
    for obj in wikiobj:
        if wiki_url_pattern.match(obj):
            # scrape url
            spot = Spot.from_scrape(Scrape(obj))
        else:
            # search term
            try:
                spot = Spot.from_search(Search(obj, language=language))
            except IndexError:
                raise UserWarning("'%s' no search results" % obj)
        spots.append(spot)
    return spots


def generate_json(spots, filename=None):
    geojson = []
    for spot in spots:
        entry = {
            'title': spot.title,
            'url': spot.url,
            'latitude': spot.latitude,
            'longitude': spot.longitude,
            'elevation': spot.elevation
        }
        geojson.append(entry)
    if filename is not None:
        with open(filename, 'w') as f:
            f.write(json.dumps(geojson, sort_keys=True))
    else:
        print json.dumps(geojson, sort_keys=True, indent=4)


def generate_markup(spots, filename=None):
    geomarkup = Markup()
    for spot in spots:
        geomarkup.add_spot(spot)
    if filename is not None:
        geomarkup.filename = filename
        geomarkup.save_kml_file()
    else:
        print geomarkup.generate_kml()


def generate_map(
        spots, map=None, size=None, type=None, path=False, region=False,
        filename=None):
    labels = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    size_x, size_y = size.split('x')
    geomap = Map(
        size_x=int(size_x), size_y=int(size_y), maptype=type,
        region=region, fillcolor='gray')
    max_index = (len(spots) - 1)
    if path is True:
        for index, spot in enumerate(spots):
            geomap.add_marker(spot, label=labels[index])
            geomap.add_path_latlon(str(spot.latitude), str(spot.longitude))
    if region is True:
        for index, spot in enumerate(spots):
            geomap.add_path_latlon(str(spot.latitude), str(spot.longitude))
            if index == max_index:
                geomap.add_path_latlon(
                    str(spots[0].latitude), str(spots[0].longitude))
    else:
        for index, spot in enumerate(spots):
            geomap.add_marker(spot, label=labels[index])
    if filename is not None:
        geomap.filename = filename
        geomap.save_map_file()
    else:
        print geomap.generate_url()


def run(args):
    # get spots
    try:
        spots = get_spots(args.wikiobj, args.language)
    except UserWarning as msg:
        print msg
        sys.exit(1)
    # json
    if hasattr(args, 'json'):
        generate_json(spots, filename=args.filename)
    # markup
    if hasattr(args, 'markup'):
        generate_markup(spots, filename=args.filename)
    # map
    if hasattr(args, 'map'):
        generate_map(
            spots, map=args.map, size=args.size, type=args.type,
            path=args.path, region=args.region, filename=args.filename)


def main():
    args = parse_options()
    run(args)

if __name__ == '__main__':
    main()
