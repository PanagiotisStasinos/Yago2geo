from urllib.parse import urlparse

import pandas
from rdflib.graph import Graph
from location.location import Location, compute_dampened_weight
import utils
from collections import Counter
import pandas as pd
import itertools
import os


class KGraph:
    Locations = {}
    training_set = {}
    test_set = {}
    Locations_sorted_by_Latitude = {}
    Locations_sorted_by_Longitude = {}

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
        for key in self.Locations[loc].Closest_Location_by_Latitude_dampened_weight:
            neighbors.append(
                tuple((key, self.Locations[loc].Closest_Location_by_Latitude_dampened_weight[key],
                       int(self.Locations[key].OS_ID), self.Locations[key].Center,
                       self.Locations[key].rdf_syntax_ns_type, self.Locations[key].area)))

        for key in self.Locations[loc].Closest_Location_by_Longitude_dampened_weight:
            neighbors.append(
                tuple((key, self.Locations[loc].Closest_Location_by_Longitude_dampened_weight[key],
                       int(self.Locations[key].OS_ID), self.Locations[key].Center,
                       self.Locations[key].rdf_syntax_ns_type, self.Locations[key].area)))
        return neighbors

    def find_neighbors_2(self, loc):
        neighbors = []
        for key in self.Locations[loc].Closest_Location_by_Latitude_dampened_weight:
            neighbors.append(
                tuple((key, self.Locations[loc].Closest_Location_by_Latitude_dampened_weight[key],
                       int(self.Locations[key].OS_ID), self.Locations[key].Center,
                       self.Locations[key].rdf_syntax_ns_type, self.Locations[key].area)))

        for key in self.Locations[loc].Closest_Location_by_Longitude_dampened_weight:
            neighbors.append(
                tuple((key, self.Locations[loc].Closest_Location_by_Longitude_dampened_weight[key],
                       int(self.Locations[key].OS_ID), self.Locations[key].Center,
                       self.Locations[key].rdf_syntax_ns_type, self.Locations[key].area)))
        for key in self.Locations[loc].Within:
            neighbors.append(
                tuple((key, 0, int(self.Locations[key].OS_ID), self.Locations[key].Center,
                       self.Locations[key].rdf_syntax_ns_type, self.Locations[key].area)))
        for key in self.Locations[loc].Includes:
            neighbors.append(
                tuple((key, 0, int(self.Locations[key].OS_ID), self.Locations[key].Center,
                       self.Locations[key].rdf_syntax_ns_type, self.Locations[key].area)))
        for key in self.Locations[loc].Touches:
            neighbors.append(
                tuple((key, 0, int(self.Locations[key].OS_ID), self.Locations[key].Center,
                       self.Locations[key].rdf_syntax_ns_type, self.Locations[key].area)))
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
            type_list.append(item.rdf_syntax_ns_type)
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
        df.to_csv('../datasets/locations_csv/locations_1.csv')

        temp_dict.pop("asWKT")
        df = pd.DataFrame.from_dict(temp_dict)
        df.to_csv('../datasets/locations_csv/locations_2.csv')

    #################################
    #   returns OS_type of the given location
    #################################
    def get_os_type(self, loc):
        return self.Locations[loc].rdf_syntax_ns_type

    #################################
    #   splits data in training and testing set, 90%-10% respectively
    #   doesn;t do the split randomly
    #################################
    def separate_data(self):
        len_d2 = len(self.Locations.items()) // 10
        len_d1 = len(self.Locations.items()) - len_d2

        i = iter(self.Locations.items())

        # self.training_set = dict(itertools.islice(i, len_d1))  # grab first len_d1 items
        # self.test_set = dict(i)                                   # last len_d2 items to test test

        self.test_set = dict(itertools.islice(i, len_d2))  # grab first len_d2 items
        self.training_set = dict(i)                                   # last len_d1 items to train test

        print("train_set ", len(self.training_set), " , test_set ", len(self.test_set), " = locs ", len(self.Locations))

        print("    train set   ")
        utils.dict_info(self.training_set)

        print("\n     test set   ")
        utils.dict_info(self.test_set)

        count = 0
        for k, v in self.test_set.items():
            if k in self.training_set:
                count = count + 1
        print(count, " duplicate")

    def print_info(self):
        print("COUNT : ", str(self.count))
        print("DICT_COUNT : ", len(self.Locations))
        index = 0
        for x, y in self.Locations.items():
            y.print_info()
            index = index + 1

    def print_statistics(self):
        utils.dict_info(self.Locations)

    def get_statistics_csv(self):
        utils.dict_info_to_csv(self.Locations)

    def location_exists(self, name):
        return name in self.Locations

    def add_within(self, subject_name, obj_name):
        self.Locations[subject_name].Within.append(obj_name)
        self.Locations[obj_name].Includes.append(subject_name)

    def add_touches(self, subject_name, obj_name):
        self.Locations[subject_name].Touches.append(obj_name)
        self.Locations[obj_name].Touches.append(subject_name)


def read_RDF_Graph_and_store_Locations(main_graph):
    weighted_graph = KGraph()
    for subject, predicate, obj in main_graph:
        args = [subject, predicate, obj]
        temp_location = Location(args)
        weighted_graph.insert_node(temp_location)

    return weighted_graph


def sort_Locations(weighted_graph):
    # sorted by Latitude
    weighted_graph.Locations_sorted_by_Latitude = {k: v for k, v in sorted(weighted_graph.Locations.items(),
                                                                           key=lambda item: item[1].Lat)}
    # sorted by Longitude
    weighted_graph.Locations_sorted_by_Longitude = {k: v for k, v in sorted(weighted_graph.Locations.items(),
                                                                            key=lambda item: item[1].Lon)}


def get_locations_from_csv(file):
    weighted_graph = KGraph()
    df = pd.read_csv(file)

    for index, row in df.iterrows():
        args = [row['name'], row['geometry'], row['id'], row['type'], row['asWKT']]
        temp_location = Location(args)
        weighted_graph.insert_node(temp_location)

    return weighted_graph


# for center distance
def find_center_distances(weighted_graph, window_size):
    # Latitude
    index = 0
    for node1 in weighted_graph.Locations_sorted_by_Latitude.items():
        # print("\n\n 1 -----------   ", node1[1].Location.resource, "( ", node1[1].Location.Lat, ", ", node1[1].Location.Lon, ")     --------   ")
        start, end = utils.find_start_end(index, len(weighted_graph.Locations_sorted_by_Latitude), window_size)
        # print(index, " (", start, ",", end, ")")
        i = 0
        for node2 in weighted_graph.Locations_sorted_by_Latitude.items():
            if i in range(int(start), int(end) + 1):
                if node1[1].resource != node2[1].resource:
                    node1[1].compute_distance_from_closest_by_Latitude(node2[1])
            i = i + 1
        index = index + 1

    # Longitude
    index = 0
    for node1 in weighted_graph.Locations_sorted_by_Longitude.items():
        # print("\n 2 -----------   ", node1[1].Location.resource, "( ", node1[1].Location.Lat, ", ", node1[1].Location.Lon, ")    --------   ")
        start, end = utils.find_start_end(index, len(weighted_graph.Locations_sorted_by_Longitude), window_size)
        # print(index, " (", start, ",", end, ")")
        i = 0
        for node2 in weighted_graph.Locations_sorted_by_Longitude.items():
            if i in range(int(start), int(end) + 1):
                if node1[1].resource != node2[1].resource:
                    node1[1].compute_distance_from_closest_by_Longitude(node2[1])
            i = i + 1
        index = index + 1

        node1[1].compute_dampened_weights_Latitude()  # we call it here because we want the total weight
        node1[1].compute_dampened_weights_Longitude()


# for polygon distance
def find_polygon_distances(weighted_graph, window_size):
    # Latitude
    index = 0
    for node1 in weighted_graph.Locations_sorted_by_Latitude.items():
        print('\t', str(index), ' / ', str(len(weighted_graph.Locations_sorted_by_Latitude)))
        # print("\n\n 1 -----------   ", node1[1].Location.resource, "( ", node1[1].Location.Lat, ", ", node1[1].Location.Lon, ")     --------   ")
        start, end = utils.find_start_end(index, len(weighted_graph.Locations_sorted_by_Latitude), window_size)
        # print(index, " (", start, ",", end, ")")
        i = 0
        for node2 in weighted_graph.Locations_sorted_by_Latitude.items():
            if i in range(int(start), int(end) + 1):
                if node1[1].resource != node2[1].resource:
                    if node1[1].resource in node2[1].Closest_Location_by_Latitude:
                        print("lat 1")
                        d = node2[1].Closest_Location_by_Latitude[node1[1].resource]
                        w = compute_dampened_weight(d)

                        node1[1].Closest_Location_by_Latitude_dampened_weight[node2[1].resource] = w
                        node1[1].Closest_Location_by_Latitude[node2[1].resource] = d

                        node1[1].dampened_weight_for_closest_by_Latitude_sum = node1[1].dampened_weight_for_closest_by_Latitude_sum + w
                        node1[1].total_weight_sum = node1[1].total_weight_sum + w
                    else:
                        node1[1].compute_distance_from_closest_by_Latitude_2(node2[1])
            i = i + 1
        index = index + 1

    # Longitude
    index = 0
    for node1 in weighted_graph.Locations_sorted_by_Longitude.items():
        print('\t', str(index), ' / ', str(len(weighted_graph.Locations_sorted_by_Longitude)))
        # print("\n 2 -----------   ", node1[1].Location.resource, "( ", node1[1].Location.Lat, ", ", node1[1].Location.Lon, ")    --------   ")
        start, end = utils.find_start_end(index, len(weighted_graph.Locations_sorted_by_Longitude), window_size)
        # print(index, " (", start, ",", end, ")")
        i = 0
        for node2 in weighted_graph.Locations_sorted_by_Longitude.items():
            if i in range(int(start), int(end) + 1):
                if node1[1].resource != node2[1].resource:
                    if node1[1].resource in node2[1].Closest_Location_by_Longitude:
                        print("lon 1")
                        d = node2[1].Closest_Location_by_Longitude[node1[1].resource]
                        w = compute_dampened_weight(d)

                        node1[1].Closest_Location_by_Longitude_dampened_weight[node2[1].resource] = w
                        node1[1].Closest_Location_by_Longitude[node2[1].resource] = d

                        node1[1].dampened_weight_for_closest_by_Longitude_sum = \
                            node1[1].dampened_weight_for_closest_by_Longitude_sum + w
                        node1[1].total_weight_sum = node1[1].total_weight_sum + w
                    elif node1[1].resource in node2[1].Closest_Location_by_Latitude:
                        print("lon 2")
                        d = node2[1].Closest_Location_by_Latitude[node1[1].resource]
                        w = compute_dampened_weight(d)

                        node1[1].Closest_Location_by_Longitude_dampened_weight[node2[1].resource] = w
                        node1[1].Closest_Location_by_Longitude[node2[1].resource] = d

                        node1[1].dampened_weight_for_closest_by_Longitude_sum = \
                            node1[1].dampened_weight_for_closest_by_Longitude_sum + w
                        node1[1].total_weight_sum = node1[1].total_weight_sum + w
                    else:
                        node1[1].compute_distance_from_closest_by_Longitude_2(node2[1])
            i = i + 1
        index = index + 1

        node1[1].compute_dampened_weights_Latitude()  # we call it here because we want the total weight
        node1[1].compute_dampened_weights_Longitude()


def store_distances(weighted_graph, vectors_type, distance_type, window_size):
    path = '../datasets/' + distance_type + '/vectors_' + str(vectors_type) + '/window_size_' + str(window_size) \
           + '/distances/'
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        print("\tDistances exist")
        return

    vectors = {}
    for key, value in weighted_graph.Locations.items():
        temp = []
        temp.append(key)    # name of current location
        for x, y in value.Closest_Location_by_Latitude.items():
            temp.append(x)  # name
            temp.append(y)  # distance
            temp.append(value.Closest_Location_by_Latitude_dampened_weight[x])  # dampened distance
        temp.append(value.dampened_weight_for_closest_by_Latitude_sum)          # dampened_weight_sum
        vectors[key] = temp
    df = pandas.DataFrame.from_dict(vectors, orient='index')
    df.rows = None
    df.to_csv(path + 'distances_lat.csv', index=False)

    vectors = {}
    for key, value in weighted_graph.Locations.items():
        temp = []
        temp.append(key)    # name of current location
        for x, y in value.Closest_Location_by_Longitude.items():
            temp.append(x)  # name
            temp.append(y)  # distance
            temp.append(value.Closest_Location_by_Longitude_dampened_weight[x])  # dampened distance
        temp.append(value.dampened_weight_for_closest_by_Longitude_sum)          # dampened_weight_sum
        vectors[key] = temp
    df = pandas.DataFrame.from_dict(vectors, orient='index')
    df.rows = None
    df.to_csv(path + 'distances_lon.csv', index=False)


def get_distances_from_csv(weighted_graph, lat_file, lon_file):
    df_lat = pd.read_csv(lat_file)
    df_lon = pd.read_csv(lon_file)

    for index, row in df_lat.iterrows():
        current_location = row['0']
        for i in range(1, len(row)-2, 3):
            neighbor_name = row[str(i)]
            j = i + 1
            d = row[str(j)]  # distance
            j = j + 1
            w = row[str(j)]  # dampened weight
            # print("\t" + str(i) + str(neighbor_name) + " - " + str(d) + " - " + str(w))
            weighted_graph.Locations[current_location].Closest_Location_by_Latitude_dampened_weight[neighbor_name] = w
            weighted_graph.Locations[current_location].Closest_Location_by_Latitude[neighbor_name] = d

        dampened_weight_lat_sum = row[str(len(row)-1)]
        weighted_graph.Locations[current_location].dampened_weight_for_closest_by_Latitude_sum = \
            dampened_weight_lat_sum
        weighted_graph.Locations[current_location].total_weight_sum = dampened_weight_lat_sum
        # print(current_location + " - " + str(dampened_weight_sum))

    for index, row in df_lon.iterrows():
        current_location = row['0']
        for i in range(1, len(row)-2, 3):
            neighbor_name = row[str(i)]
            j = i + 1
            d = row[str(j)]     # distance
            j = j + 1
            w = row[str(j)]     # dampened weight
            # print("\t" + str(i) + str(neighbor_name) + " - " + str(d) + " - " + str(w))
            weighted_graph.Locations[current_location].Closest_Location_by_Longitude_dampened_weight[neighbor_name] = w
            weighted_graph.Locations[current_location].Closest_Location_by_Longitude[neighbor_name] = d

        dampened_weight_lon_sum = row[str(len(row)-1)]
        weighted_graph.Locations[current_location].dampened_weight_for_closest_by_Longitude_sum = \
            dampened_weight_lon_sum
        weighted_graph.Locations[current_location].total_weight_sum = \
            weighted_graph.Locations[current_location].total_weight_sum + dampened_weight_lon_sum
        # print(current_location + " - " + str(dampened_weight_sum))


def empty_distance_dicts(weighted_graph):
    for key, value in weighted_graph.Locations.items():
        value.Closest_Location_by_Latitude.clear()
        value.Closest_Location_by_Latitude_dampened_weight.clear()
        value.dampened_weight_for_closest_by_Latitude_sum = 0.0

        value.Closest_Location_by_Longitude.clear()
        value.Closest_Location_by_Longitude_dampened_weight.clear()
        value.dampened_weight_for_closest_by_Longitude_sum = 0.0

        value.total_weight_sum = 0.0
