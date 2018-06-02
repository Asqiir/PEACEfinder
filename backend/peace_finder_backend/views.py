from django.shortcuts import render
from django.http import HttpResponse
import datetime
import json
from shapely.geometry import Point, shape
import numpy as np


def alldata(request):
    with open('../data/parkanlagen.json') as f:
        js = json.load(f)

    boxes = []

    for feature in js['features']:
        geometry = feature['geometry']
        if geometry['type'] == 'MultiPolygon':
            coordinates = geometry['coordinates']
            for Poligon in geometry['coordinates']:
                points = Poligon[0]
                boxes.append((max(points, key=lambda maxx: maxx[0]), max(points, key=lambda maxy: maxy[1]),
                              min(points, key=lambda minx: minx[0]), min(points, key=lambda miny: miny[1])))

                for point in boxes:
                    tl = [point[2][0], point[1][1]]
                    tr = [point[0][0], point[1][1]]
                    bl = [point[2][0], point[3][1]]
                    br = [point[0][0], point[3][1]]


    #  points = np.array(js)

    #
    #
    # for element in js:
    #     del element['properties']

    content = str(boxes)
    return HttpResponse(content, content_type='text/plain')
