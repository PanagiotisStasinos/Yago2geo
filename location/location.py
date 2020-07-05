import shapely.wkt
from shapely.geometry import Point
import numpy as np
from math import e
from geopy import distance
import re
from utils import get_url_value


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
            self.rdf_syntax_ns_type = None

            self.Within = []
            self.Includes = []
            self.Touches = []

            self.Lat = None
            self.Lon = None
            self.Center = None
            self.polygon = None
            self.area = None

            self.Closest_Location_by_Latitude = {}      # key: name of neighbor, value: distance
            self.Closest_Location_by_Latitude_dampened_weight = {}  # key: name of neighbor, value: dampened distance
            self.dampened_weight_for_closest_by_Latitude_sum = 0.0

            self.Closest_Location_by_Longitude = {}
            self.Closest_Location_by_Longitude_dampened_weight = {}
            self.dampened_weight_for_closest_by_Longitude_sum = 0.0

            self.total_weight_sum = 0.0

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

                self.Lat = self.Center.x
                self.Lon = self.Center.y
                self.Center = Point(self.Lat, self.Lon)
            elif pred == "rdf-syntax-ns#type":
                self.rdf_syntax_ns_type = get_url_value(obj)
        else:   # get info from csv
            self.resource = args[0]

            self.OS_Name = args[0]
            self.OS_Geometry = args[1]
            self.OS_ID = args[2]
            self.rdf_syntax_ns_type = args[3]
            self.asWKT = args[4]

            self.Within = []
            self.Includes = []
            self.Touches = []

            self.polygon = shapely.wkt.loads(self.asWKT)
            self.Center = self.polygon.centroid
            self.area = self.polygon.area
            self.Lat = self.Center.x
            self.Lon = self.Center.y

            if self.OS_Geometry != self.OS_Geometry:    # is NaN
                self.OS_Geometry = None

            self.Closest_Location_by_Latitude = {}
            self.Closest_Location_by_Latitude_dampened_weight = {}
            self.dampened_weight_for_closest_by_Latitude_sum = 0.0

            self.Closest_Location_by_Longitude = {}
            self.Closest_Location_by_Longitude_dampened_weight = {}
            self.dampened_weight_for_closest_by_Longitude_sum = 0.0

            self.total_weight_sum = 0.0

    def print_info(self):
        print("[", self.resource, ", ", self.rdf_syntax_ns_type, ", ",
              str(self.Center), ", ", self.OS_ID, ", ", self.OS_Name, ", ", self.OS_Geometry, ", ", self.asWKT, "]")

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
        elif self.rdf_syntax_ns_type is not None and prev.rdf_syntax_ns_type is None:
            prev.rdf_syntax_ns_type = self.rdf_syntax_ns_type

    #################################
    #   finds the geodesic distance between the centers of the 2 locations
    #   computes the dampened weight
    #   adds the weight to dampened_weight_for_closest_by_Latitude_sum and to total_weight_sum for later use
    #################################
    def compute_distance_from_closest_by_Latitude(self, other_Location):
        # d = self.Center.distance(other_Location.Center)
        curr = (self.Lat, self.Lon)
        other = (other_Location.Lat, other_Location.Lon)
        d = distance.geodesic(curr, other).miles
        w = compute_dampened_weight(d)
        # print("dist ", self.resource, "(", self.Lat, self.Lon, ") ", other_Location.resource, "(", other_Location.Lat,
        #       other_Location.Lon, ") = ", d, ", ", w)

        self.Closest_Location_by_Latitude_dampened_weight[other_Location.resource] = w
        self.Closest_Location_by_Latitude[other_Location.resource] = d

        self.dampened_weight_for_closest_by_Latitude_sum = self.dampened_weight_for_closest_by_Latitude_sum + w
        self.total_weight_sum = self.total_weight_sum + w

    #################################
    #   does the same as compute_distance_from_closest_by_Latitude
    #   but for closest by longitude locations
    #################################
    def compute_distance_from_closest_by_Longitude(self, other_Location):
        # d = self.Center.distance(other_Location.Center)
        curr = (self.Lat, self.Lon)
        other = (other_Location.Lat, other_Location.Lon)
        d = distance.geodesic(curr, other).miles
        w = compute_dampened_weight(d)
        # print("dist ", self.resource, "(", self.Lat, self.Lon, ") ", other_Location.resource, "(", other_Location.Lat,
        #       other_Location.Lon, ") = ", d, ", ", w)

        self.Closest_Location_by_Longitude_dampened_weight[other_Location.resource] = w
        self.Closest_Location_by_Longitude[other_Location.resource] = d

        self.dampened_weight_for_closest_by_Longitude_sum = self.dampened_weight_for_closest_by_Longitude_sum + w
        self.total_weight_sum = self.total_weight_sum + w

    def compute_dampened_weights_Latitude(self):
        for key in self.Closest_Location_by_Latitude_dampened_weight:
            self.Closest_Location_by_Latitude_dampened_weight[key] = self.Closest_Location_by_Latitude_dampened_weight[
                                                                         key] / self.total_weight_sum

    def compute_dampened_weights_Longitude(self):
        for key in self.Closest_Location_by_Longitude_dampened_weight:
            self.Closest_Location_by_Longitude_dampened_weight[key] = \
                self.Closest_Location_by_Longitude_dampened_weight[
                    key] / self.total_weight_sum

    def print_dampened_weights_Latitude(self):
        for item in self.Closest_Location_by_Latitude_dampened_weight.items():
            print(self.resource, " - ", item[0], " = ", item[1])
        print(self.dampened_weight_for_closest_by_Latitude_sum)

    def print_dampened_weights_Longitude(self):
        for item in self.Closest_Location_by_Longitude_dampened_weight.items():
            print(self.resource, " - ", item[0], " = ", item[1])
        print(self.dampened_weight_for_closest_by_Longitude_sum)

    def get_OS_ID_from_OS_Name(self):
        a = re.findall("\d+", self.resource)
        self.OS_ID = a[0]

    def concat_locations(self, other):
        if self.OS_ID is None:
            self.OS_ID = other.OS_ID
        if self.OS_Name is None:
            self.OS_Name = other.resource
        if self.rdf_syntax_ns_type is None:
            self.rdf_syntax_ns_type = other.rdf_syntax_ns_type

        self.count = self.count + other.count

    #################################
    #   finds the geodesic distance between the centers of the 2 locations
    #   computes the dampened weight
    #   adds the weight to dampened_weight_for_closest_by_Latitude_sum and to total_weight_sum for later use
    #################################
    def compute_distance_from_closest_by_Latitude_2(self, other_Location):
        # d = self.Center.distance(other_Location.Center)
        d = self.polygon.distance(other_Location.polygon)
        w = compute_dampened_weight(d)
        # curr = (self.Lat, self.Lon)
        # other = (other_Location.Lat, other_Location.Lon)
        # d1 = distance.geodesic(curr, other).miles   # MILES
        # w1 = compute_dampened_weight(d1)
        d2 = self.Center.distance(other_Location.Center)
        w2 = compute_dampened_weight(d2)
        print("dist ", self.resource, "-", other_Location.resource, "( ", d, ", ", w, ")", "( ", d2, ", ", w2, ")")

        self.Closest_Location_by_Latitude_dampened_weight[other_Location.resource] = w
        self.Closest_Location_by_Latitude[other_Location.resource] = d

        self.dampened_weight_for_closest_by_Latitude_sum = self.dampened_weight_for_closest_by_Latitude_sum + w
        self.total_weight_sum = self.total_weight_sum + w

    #################################
    #   does the same as compute_distance_from_closest_by_Latitude
    #   but for closest by longitude locations
    #################################
    def compute_distance_from_closest_by_Longitude_2(self, other_Location):
        # d = self.Center.distance(other_Location.Center)
        d = self.polygon.distance(other_Location.polygon)
        w = compute_dampened_weight(d)
        d2 = self.Center.distance(other_Location.Center)
        w2 = compute_dampened_weight(d2)
        print("dist ", self.resource, "-", other_Location.resource, "( ", d, ", ", w, ")", "( ", d2, ", ", w2, ")")

        self.Closest_Location_by_Longitude_dampened_weight[other_Location.resource] = w
        self.Closest_Location_by_Longitude[other_Location.resource] = d

        self.dampened_weight_for_closest_by_Longitude_sum = self.dampened_weight_for_closest_by_Longitude_sum + w
        self.total_weight_sum = self.total_weight_sum + w


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


def compute_dampened_weight(dist):
    if dist == 0:
        return e
    return max(1.0 / np.log(dist), e)
    # return 1.0 / np.log(dist)
