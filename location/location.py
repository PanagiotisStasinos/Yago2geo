import shapely.wkt
from shapely.geometry import Point
import numpy as np
from math import e
from geopy import distance  # https://geopy.readthedocs.io/en/stable/#module-geopy.distance
import re
from utils import get_url_value
from haversine import haversine # https://pypi.org/project/haversine/
from shapely.ops import nearest_points # https://shapely.readthedocs.io/en/latest/manual.html#shapely.ops.nearest_points


class Location:
    def __init__(self, args):
        if len(args) == 3:
            subject = args[0]
            predicate = args[1]
            obj = args[2]

            self.count = 0  # number of triples with this predicate

            self.OS_Geometry = None
            self.OS_ID = None
            self.OS_Name = None
            self.asWKT = None
            self.OS_type = None

            self.Within = []
            self.Includes = []
            self.Touches = []

            self.Lat = None
            self.Lon = None
            self.Center = None
            self.polygon = None
            self.area = None

            self.adjacency_list = {}
            self.weighted_adjacency_list = {}


            self.resource = get_url_value(subject)

            pred = get_type_predicate(predicate)
            if pred == "hasGeometry":
                self.OS_Geometry = get_url_value(obj)
            elif pred == "hasOS_Name":
                self.OS_Name = get_name(obj)
            elif pred == "hasOS_ID":
                self.OS_ID = get_ID(obj)
            elif pred == "asWKT":
                self.asWKT = get_asWKT(obj)
                self.polygon = shapely.wkt.loads(self.asWKT)
                self.Center = self.polygon.centroid
                self.area = self.polygon.area

                self.Lat = self.Center.y
                self.Lon = self.Center.x
                self.Center = Point(self.Lat, self.Lon)
            elif pred == "rdf-syntax-ns#type":
                self.OS_type = get_url_value(obj)
        else:   # get info from csv
            self.resource = args[0]

            self.OS_Name = args[0]
            self.OS_Geometry = args[1]
            self.OS_ID = args[2]
            self.OS_type = args[3]
            self.asWKT = args[4]

            self.Within = []
            self.Includes = []
            self.Touches = []

            self.polygon = shapely.wkt.loads(self.asWKT)
            self.Center = self.polygon.centroid
            self.area = self.polygon.area
            self.Lat = self.Center.y
            self.Lon = self.Center.x

            if self.OS_Geometry != self.OS_Geometry:    # is NaN
                self.OS_Geometry = None

            self.adjacency_list = {}
            self.weighted_adjacency_list = {}

    def print_info(self):
        # print("[", self.resource, ", ", self.OS_type, ", ",
        #       str(self.Center), ", ", self.OS_ID, ", ", self.OS_Name, ", ", self.OS_Geometry, ", ", self.asWKT
        #       , ", ", self.area, "]")
        print("\t", self.OS_Name, "\n",
              self.OS_type, "\n",
              self.area, "\n",
              self.Center)

    def get_OS_ID_from_OS_Name(self):
        a = re.findall("\d+", self.resource)
        self.OS_ID = a[0]

        def concat_locations(self, other):
            if self.OS_ID is None:
                self.OS_ID = other.OS_ID
            if self.OS_Name is None:
                self.OS_Name = other.resource
            if self.OS_type is None:
                self.OS_type = other.OS_type

            self.count = self.count + other.count

    #################################
    #   used when reading locations from RDF graph
    #   updates the info of an existing location with new values that were None before
    #################################
    def concat(self, prev):
        if self.asWKT is not None and prev.asWKT is None:
            prev.asWKT = self.asWKT
        elif self.OS_Geometry is not None and prev.OS_Geometry is None:
            prev.OS_Geometry = self.OS_Geometry
        elif self.OS_ID is not None and prev.OS_ID is None:
            prev.OS_ID = self.OS_ID
        elif self.OS_Name is not None and prev.OS_Name is None:
            prev.OS_Mame = self.OS_Name
        elif self.OS_type is not None and prev.OS_type is None:
            prev.OS_type = self.OS_type

    def get_geodesic_distance(self, other_Location):
        curr = (self.Lat, self.Lon)
        other = (other_Location.Lat, other_Location.Lon)

        # d = distance.geodesic(curr, other).km     # .miles
        # d ~= d1
        d1 = haversine(curr, other)     # in km

        w = compute_dampened_weight(d1)
        return d1, w

    def l1_normalize_dampened_weights(self):
        # get sum
        total_sum = 0
        for key, value in self.weighted_adjacency_list.items():
            total_sum += value
        # divide by sum
        test_sum = 0
        for key, value in self.weighted_adjacency_list.items():
            self.weighted_adjacency_list[key] = value/total_sum
            test_sum += self.weighted_adjacency_list[key]

    #################################
    #   finds the distance between the polygons of the 2 locations
    #   computes the dampened weight
    #################################
    def get_polygon_distance(self, other_Location):
        # find closest points between 2 multipolygons
        p1, p2 = nearest_points(self.polygon, other_Location.polygon)
        # get haversine distance between those 2 points
        curr = (p1.y, p1.x)
        other = (p2.y, p2.x)
        d = haversine(curr, other)

        w = compute_dampened_weight(d)
        return d, w


########################
#   util methods of the file
#
########################

def get_type_predicate(predicate):
    if str(predicate) == "http://www.opengis.net/ont/geosparql#asWKT":
        return "asWKT"
    elif str(predicate) == "http://www.opengis.net/ont/geosparql#hasGeometry":
        return "hasGeometry"
    elif str(predicate) == "http://www.w3.org/1999/02/22-rdf-syntax-ns#type":
        return "rdf-syntax-ns#type"
    elif str(predicate) == "http://kr.di.uoa.gr/yago2geo/ontology/hasOS_Name":
        return "hasOS_Name"
    elif str(predicate) == "http://kr.di.uoa.gr/yago2geo/ontology/hasOS_ID":
        return "hasOS_ID"


def get_name(obj):
    os_name = str(obj)
    return os_name


def get_ID(obj):
    OS_ID = str(obj)
    return OS_ID


def get_asWKT(obj):
    # print(str(obj))
    x = str(obj).split(">  ")
    as_wkt = ""
    if len(x) == 1:
        as_wkt = str(obj)
    else:
        as_wkt = x[1]
    # print(x[1])
    return as_wkt


# https://numpy.org/doc/stable/reference/generated/numpy.log.html
def compute_dampened_weight(dist):
    if dist == 0:
        # 1.0 / np.log(dist) -> 0
        return e
    # if max(1.0 / np.log(dist), e) != e:
    #     print(max(1.0 / np.log(dist), e))
    return max(1.0 / np.log(dist), e)


