from urllib.parse import urlparse

import numpy
import pandas
from rdflib.graph import Graph
from location.location import Location, compute_dampened_weight
import utils
from collections import Counter
import pandas as pd
import os
from math import e


class KGraph:
    Locations = {}

    # Since Python 3.7 the dictionaries are order-preserving
    Locations_sorted_by_Latitude = {}  # k: name, v: Location obj
    Locations_sorted_by_Longitude = {}  # k: name, v: Location obj

    def __init__(self):
        self.count = 0

    def insert_node(self, loc):
        # print("insert_node")
        self.count += 1
        if loc.resource in self.Locations:
            # print(node.Location.resource, " already exists")
            prev = self.Locations[loc.resource]
            loc.concat(prev)
        else:
            self.Locations[loc.resource] = loc  # add

    def clear(self):
        self.Locations.clear()

    def find_neighbors(self, loc):
        neighbors = []
        # l1-normalize weighted_adjacency_list, to achieve a valid probability distribution
        self.Locations[loc].l1_normalize_dampened_weights()

        for key, value in self.Locations[loc].adjacency_list.items():
            neighbors.append(
                tuple((key, self.Locations[loc].weighted_adjacency_list[key],
                       int(self.Locations[key].OS_ID), self.Locations[key].Center,
                       self.Locations[key].OS_type, self.Locations[key].area)))
        return neighbors

    def concat_geo(self):
        count = 0
        to_delete = []
        for x, y in self.Locations.items():
            if y.OS_Geometry in self.Locations:
                count = count + 1
                self.Locations[y.OS_Geometry].concat_locations(y)

                to_delete.append(y.resource)

        print("CONCAT COUNT ", count)
        print("UNIQUE :", len(Counter(to_delete).keys()))
        count = 0
        for x in Counter(to_delete).keys():
            del self.Locations[x]
            count = count + 1
        print(count, " DELETED")

    def concat_matches(self):
        temp_g = Graph()
        temp_g.parse("C:/Users/panai/Desktop/yago2geo_uk/os/OS_matches.nt", format="nt")
        count = 0
        count1 = 0
        count2 = 0
        for sub, pred, obj in temp_g:
            o = urlparse(sub)
            x = str(o.path).split("/")
            name1 = x[len(x) - 1]
            o = urlparse(obj)
            x = str(o.path).split("/")
            name2 = x[len(x) - 1]
            print("Name1 ", name1, " - Name2 ", name2)
            if name1 in self.Locations:
                count1 = count1 + 1
            if name2 in self.Locations:
                count2 = count2 + 1
            count = count + 1
        # print("COUNT1 : ", count1, " - COUNT2 : ", count2, " - COUNT : ", count)
        if count1 == 0:
            print("       NO MATCHES NEEDED")
        else:
            print("\n\n        ", count1, " MATCHES MUST BE DONE     !!!\n\n")
            # to do

    #################################
    #   writes all locations to a scv file
    #   for quicker reading in next parts of the project
    #################################
    def write_to_csv(self):
        temp_dict = {}

        resource_list = []
        center_list = []
        area_list = []

        geometry_list = []
        id_list = []
        name_list = []
        wkt_list = []
        type_list = []

        for key, item in self.Locations.items():
            resource_list.append(key)
            center_list.append(item.Center)
            area_list.append(item.area)

            name_list.append(item.OS_Name)
            id_list.append(item.OS_ID)
            type_list.append(item.OS_type)
            wkt_list.append(item.asWKT)
            geometry_list.append(item.OS_Geometry)

        # temp_dict["resource"] = resource_list
        temp_dict["name"] = name_list
        temp_dict["geometry"] = geometry_list
        # temp_dict["center"] = center_list
        # temp_dict["area"] = area_list
        temp_dict["id"] = id_list
        temp_dict["type"] = type_list
        temp_dict["asWKT"] = wkt_list
        df = pd.DataFrame.from_dict(temp_dict)
        df.to_csv('../datasets/locations_csv/locations.csv')

        temp_dict.pop("asWKT")
        df = pd.DataFrame.from_dict(temp_dict)
        df.to_csv('../datasets/locations_csv/locations_2.csv')

    #################################
    #   returns OS_type of the given location
    #################################
    def get_os_type(self, loc):
        return self.Locations[loc].OS_type

    #################################
    #   returns OS_type of the given location
    #################################
    def get_os_id(self, loc):
        return self.Locations[loc].OS_ID

    def print_info(self):
        print("COUNT : ", str(self.count))
        print("DICT_COUNT : ", len(self.Locations))
        index = 0
        for x, y in self.Locations.items():
            y.print_info()
            index = index + 1

    def print_statistics(self):
        utils.dict_info(self.Locations)

    def get_statistics_csv(self, vec_type):
        utils.dict_info_to_csv(self.Locations, vec_type)

    def location_exists(self, name):
        return name in self.Locations

    def add_within(self, subject_name, obj_name):
        self.Locations[subject_name].Within.append(obj_name)
        self.Locations[obj_name].Includes.append(subject_name)

    def add_touches(self, subject_name, obj_name):
        self.Locations[subject_name].Touches.append(obj_name)
        self.Locations[obj_name].Touches.append(subject_name)

    def print_loc_info(self, temp_loc):
        self.Locations[temp_loc].print_info()

    def get_location_info(self, temp_loc):
        temp_dict = {'area': self.Locations[temp_loc].area, "type": self.Locations[temp_loc].OS_type,
                     "OS_ID": self.Locations[temp_loc].OS_ID, "center": self.Locations[temp_loc].Center}
        return temp_dict


def read_RDF_Graph_and_store_Locations(main_graph):
    weighted_graph = KGraph()
    for subject, predicate, obj in main_graph:
        args = [subject, predicate, obj]
        temp_location = Location(args)
        weighted_graph.insert_node(temp_location)

    return weighted_graph


# ascending order
def sort_Locations(weighted_graph):
    # sorted by Latitude
    weighted_graph.Locations_sorted_by_Latitude = {k: v for k, v in sorted(weighted_graph.Locations.items(),
                                                                           key=lambda item: item[1].Lat)}
    temp_lat = {}
    for k, v in weighted_graph.Locations_sorted_by_Latitude.items():
        temp_lat[k] = v.Lat
    df1 = pandas.DataFrame.from_dict(temp_lat, orient='index')
    df1.to_csv('../datasets/locations_csv/lat_sorted.csv')

    # sorted by Longitude
    weighted_graph.Locations_sorted_by_Longitude = {k: v for k, v in sorted(weighted_graph.Locations.items(),
                                                                            key=lambda item: item[1].Lon)}
    temp_lon = {}
    for k, v in weighted_graph.Locations_sorted_by_Longitude.items():
        temp_lon[k] = v.Lon
    df2 = pandas.DataFrame.from_dict(temp_lon, orient='index')
    df2.to_csv('../datasets/locations_csv/lon_sorted.csv')


# for center distances
# 1. find distances from latitude list neighbors
# 2. same for longitude if they already exist
# 3. check within, includes and touches lists and if the location already exist
#       in  adjacency list and make distance 0 and weighted distance e
def find_center_distances(weighted_graph, window_size):
    # Latitude
    # pointer to the current location
    index = 0
    # for every location in the Latitude dict
    lat_sorted = list(weighted_graph.Locations_sorted_by_Latitude.keys())
    for name1 in lat_sorted:
        start = index + 1
        end = min(index + window_size + 1, len(lat_sorted))
        # print("Lat:", index, name1, weighted_graph.Locations[name1].Lat, end - start)
        for i in range(start, end):
            d, w = weighted_graph.Locations[name1].get_geodesic_distance(
                weighted_graph.Locations[lat_sorted[i]])
            weighted_graph.Locations[name1].adjacency_list[lat_sorted[i]] = d
            weighted_graph.Locations[name1].weighted_adjacency_list[lat_sorted[i]] = w
            # print(lat_sorted[i], d, w)
        index = index + 1

    # Longitude
    # pointer to the current location
    index = 0
    # for every location in the Longitude dict
    lon_sorted = list(weighted_graph.Locations_sorted_by_Longitude.keys())
    for name1 in lon_sorted:
        start = index + 1
        end = min(index + window_size + 1, len(lon_sorted))
        # print("Lon:", index, name1, weighted_graph.Locations[name1].Lon, end - start)
        for i in range(start, end):
            if lon_sorted[i] not in weighted_graph.Locations[name1].adjacency_list:
                d, w = weighted_graph.Locations[name1].get_geodesic_distance(
                    weighted_graph.Locations[lon_sorted[i]])
                weighted_graph.Locations[name1].adjacency_list[lon_sorted[i]] = d
                weighted_graph.Locations[name1].weighted_adjacency_list[lon_sorted[i]] = w
                # print(lon_sorted[i], d, w)

        # print("Lon:", index, name1, len(weighted_graph.Locations[name1].adjacency_list))
        index = index + 1

    # add within and touches
    # if locations in adjacency list belong to Include, within or touches list
    # distance = 0  and  dampened_weight = e
    # length of adjacency list doesn't change
    prev_sum = 0
    for key, value in weighted_graph.Locations.items():
        prev_length = len(weighted_graph.Locations[key].adjacency_list)
        prev_sum += prev_length
        # Within
        for neighbor in weighted_graph.Locations[key].Within:
            if neighbor in weighted_graph.Locations[key].adjacency_list:
                weighted_graph.Locations[key].adjacency_list[neighbor] = 0.0
                weighted_graph.Locations[key].weighted_adjacency_list[neighbor] = e
        # Includes
        for neighbor in weighted_graph.Locations[key].Includes:
            if neighbor in weighted_graph.Locations[key].adjacency_list:
                weighted_graph.Locations[key].adjacency_list[neighbor] = 0.0
                weighted_graph.Locations[key].weighted_adjacency_list[neighbor] = e
        # Touches
        for neighbor in weighted_graph.Locations[key].Touches:
            if neighbor in weighted_graph.Locations[key].adjacency_list:
                weighted_graph.Locations[key].adjacency_list[neighbor] = 0.0
                weighted_graph.Locations[key].weighted_adjacency_list[neighbor] = e

        # print("Prev ", prev_length, " added ", added, " new_length ", new_length)
    print(window_size, " average ", prev_sum/len(weighted_graph.Locations))


# for polygon distance
# distance between current location and its closest neighbors
# if distances for smaller windows exist we use them to do less computations
# that s why we check if the location is already in the adjacency list
#################################################################
def find_polygon_distances(weighted_graph, window_size):
    # Latitude
    # pointer to the current location
    index = 0
    # for every location in the Latitude dict
    lat_sorted = list(weighted_graph.Locations_sorted_by_Latitude.keys())
    for name1 in lat_sorted:
        start = index + 1
        end = min(index + window_size + 1, len(lat_sorted))
        # print("Lat:", index, name1, weighted_graph.Locations[name1].Lat, end - start)
        print(index, ")", name1)
        for i in range(start, end):
            if lat_sorted[i] not in weighted_graph.Locations[name1].adjacency_list:
                d, w = weighted_graph.Locations[name1].get_polygon_distance(
                    weighted_graph.Locations[lat_sorted[i]])
                weighted_graph.Locations[name1].adjacency_list[lat_sorted[i]] = d
                weighted_graph.Locations[name1].weighted_adjacency_list[lat_sorted[i]] = w
                # print(lat_sorted[i], d, w, "\n\n")
        #         print("\t", i)
        #     else:
        #         print("\t", i, " exists")
        # print(index, ")", name1, "DONE")
        index = index + 1

    # Longitude
    # pointer to the current location
    index = 0
    # for every location in the Longitude dict
    lon_sorted = list(weighted_graph.Locations_sorted_by_Longitude.keys())
    for name1 in lon_sorted:
        start = index + 1
        end = min(index + window_size + 1, len(lon_sorted))
        # print("Lon:", index, name1, weighted_graph.Locations[name1].Lon, end - start)
        print(index, ")", name1)
        for i in range(start, end):
            if lon_sorted[i] not in weighted_graph.Locations[name1].adjacency_list:
                d, w = weighted_graph.Locations[name1].get_polygon_distance(
                    weighted_graph.Locations[lon_sorted[i]])
                weighted_graph.Locations[name1].adjacency_list[lon_sorted[i]] = d
                weighted_graph.Locations[name1].weighted_adjacency_list[lon_sorted[i]] = w
                # print(lon_sorted[i], d, w, "\n\n")
            #     print("\t", i)
            # else:
            #     print("\t", i, " exists")
        # print(index, ")", name1, "DONE")
        index = index + 1

    # add within and touches
    # if locations in adjacency list belong to Include, within or touches list
    # distance = 0  and  dampened_weight = e
    # length of adjacency list doesn't change
    prev_sum = 0
    for key, value in weighted_graph.Locations.items():
        prev_length = len(weighted_graph.Locations[key].adjacency_list)
        prev_sum += prev_length
        # Within
        for neighbor in weighted_graph.Locations[key].Within:
            if neighbor in weighted_graph.Locations[key].adjacency_list:
                weighted_graph.Locations[key].adjacency_list[neighbor] = 0.0
                weighted_graph.Locations[key].weighted_adjacency_list[neighbor] = e
        # Includes
        for neighbor in weighted_graph.Locations[key].Includes:
            if neighbor in weighted_graph.Locations[key].adjacency_list:
                weighted_graph.Locations[key].adjacency_list[neighbor] = 0.0
                weighted_graph.Locations[key].weighted_adjacency_list[neighbor] = e
        # Touches
        for neighbor in weighted_graph.Locations[key].Touches:
            if neighbor in weighted_graph.Locations[key].adjacency_list:
                weighted_graph.Locations[key].adjacency_list[neighbor] = 0.0
                weighted_graph.Locations[key].weighted_adjacency_list[neighbor] = e

        # print("Prev ", prev_length, " added ", added, " new_length ", new_length)
    print(window_size, " average ", prev_sum/len(weighted_graph.Locations))


def get_polygon_distances(weighted_graph, window_size, smaller_window_size):
    file = "../datasets/center_distance/window_size_" + str(smaller_window_size) + "/distances/distances.csv"
    df = pandas.read_csv(file)

    for index, row in df.iterrows():
        current_location = row['0']
        for i in range(1, len(row), 3):
            neighbor_name = row[str(i)]
            j = i + 1
            d = row[str(j)]  # distance
            j = j + 1
            w = row[str(j)]  # dampened weight
            if neighbor_name is not numpy.nan:  # because each locations has different number of neighbors
                weighted_graph.Locations[current_location].adjacency_list[neighbor_name] = d
                weighted_graph.Locations[current_location].weighted_adjacency_list[neighbor_name] = w


def get_locations_from_csv(file):
    weighted_graph = KGraph()
    df = pd.read_csv(file)

    for index, row in df.iterrows():
        args = [row['name'], row['geometry'], row['id'], row['type'], row['asWKT']]
        temp_location = Location(args)
        weighted_graph.insert_node(temp_location)

    return weighted_graph


def store_distances(weighted_graph, distance_type, window_size):
    path = '../datasets/' + distance_type + '/window_size_' + str(window_size) + '/distances/'
    if not os.path.exists(path):
        os.makedirs(path)

    vectors = {}
    for key, value in weighted_graph.Locations.items():
        temp = []
        temp.append(key)  # name of current location
        for x, y in value.adjacency_list.items():
            temp.append(x)  # name
            temp.append(y)  # distance
            temp.append(value.weighted_adjacency_list[x])  # dampened distance
        vectors[key] = temp
    df = pandas.DataFrame.from_dict(vectors, orient='index')
    df.rows = None
    df.to_csv(path + 'distances.csv', index=False)


def get_distances_from_csv(weighted_graph, file):
    df = pd.read_csv(file)

    summ = 0
    count = 0
    for index, row in df.iterrows():
        count += 1
        current_location = row['0']
        for i in range(1, len(row), 3):     # for i in range(1, len(row) - 1, 3):
            neighbor_name = row[str(i)]
            j = i + 1
            d = row[str(j)]  # distance
            j = j + 1
            w = row[str(j)]  # dampened weight
            # print("\t" + str(i) + str(neighbor_name) + " - " + str(d) + " - " + str(w))
            if neighbor_name is not numpy.nan:  # because each locations has different number of neighbors
                weighted_graph.Locations[current_location].weighted_adjacency_list[neighbor_name] = w
                weighted_graph.Locations[current_location].adjacency_list[neighbor_name] = d
                summ += 1

    print(summ/count)


def empty_distance_dicts(weighted_graph):
    for key, value in weighted_graph.Locations.items():
        value.adjacency_list.clear()
        value.weighted_adjacency_list.clear()
