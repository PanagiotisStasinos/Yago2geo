from urllib.parse import urlparse

###########################################
#
#
#
###########################################
import numpy as np

WINDOW_SIZE = 11

OS_TYPES = {
    "OS_CivilParishorCommunity": 0,
    "OS_DistrictWard": 1,
    "OS_UnitaryAuthorityWard": 2,
    "OS_District": 3,
    "OS_MetropolitanDistrict": 4,
    "OS_MetropolitanDistrictWard": 5,
    "OS_LondonBorough": 6,
    "OS_UnitaryAuthority": 7,
    "OS_LondonBoroughWard": 8,
    "OS_County": 9,
    "OS_EuropeanRegion": 10,
    "OS_GreaterLondonAuthority": 11,

    "OS_COMMUNITYWARD": 12,
    "OS_COMMUNITY": 13,
    "OS_CCOMMUNITY": 14
}


def find_start_end(index, size):
    if index < ((WINDOW_SIZE - 1) / 2):
        start = 0
        end = WINDOW_SIZE - 1
    elif index > size - 1 - ((WINDOW_SIZE - 1) / 2):
        start = size - WINDOW_SIZE
        end = size - 1
    else:
        start = index - ((WINDOW_SIZE - 1) / 2)
        end = index + ((WINDOW_SIZE - 1) / 2)
    return start, end


def print_vectors(vectors):
    for loc in vectors:
        print(loc)
        for walk in vectors[loc]:
            print(walk, vectors[loc][walk])


def get_url_value(subject):
    o = urlparse(subject)
    x = str(o.path).split("/")
    value = x[len(x) - 1]
    return value


def get_value_of_type(os_type):
    return OS_TYPES[os_type]


def dict_info(temp_dict):
    wkt_count = 0
    geo_count = 0
    id_count = 0
    name_count = 0
    type_count = 0

    within_counter = 0
    within_average_len = 0
    includes_counter = 0
    includes_average_len = 0
    touches_counter = 0
    touches_average_len = 0

    count = 0
    dif_types_count = np.zeros(len(OS_TYPES))
    for k, v in temp_dict.items():
        if v.asWKT is not None:
            wkt_count = wkt_count + 1
        if v.OS_Geometry is not None:
            geo_count = geo_count + 1
        if v.OS_ID is not None:
            id_count = id_count + 1
        if v.OS_Name is not None:
            name_count = name_count + 1
        if v.rdf_syntax_ns_type is not None:
            type_count = type_count + 1
        if v.Touches:  # not empty
            touches_counter = touches_counter + 1
            touches_average_len = touches_average_len + len(v.Touches)
        if v.Within:  # not empty
            within_counter = within_counter + 1
            within_average_len = within_average_len + len(v.Within)
        if v.Includes:  # not empty
            includes_counter = includes_counter + 1
            includes_average_len = includes_average_len + len(v.Includes)
        count = count + 1
        # print(" -> ", v.rdf_syntax_ns_type)
        dif_types_count[get_value_of_type(v.rdf_syntax_ns_type)] = \
            dif_types_count[get_value_of_type(v.rdf_syntax_ns_type)] + 1

    print("#\t\ttotal ", count)
    print("#\twkt ", wkt_count)
    print("#\tgeo ", geo_count)
    print("#\tid ", id_count)
    print("#\tname ", name_count)
    print("#\ttype ", type_count)
    print("#\twithin ", within_counter, " average len ", within_average_len/(max(1, within_counter)))
    print("#\tincludes ", includes_counter, " average len ", includes_average_len/(max(1, includes_average_len)))
    print("#\ttouches ", touches_counter, " average len ", touches_average_len/(max(1, touches_counter)))
    print("#\tOS_CivilParishorCommunity ", dif_types_count[get_value_of_type("OS_CivilParishorCommunity")])
    print("#\tOS_DistrictWard ", dif_types_count[get_value_of_type("OS_DistrictWard")])
    print("#\tOS_UnitaryAuthorityWard ", dif_types_count[get_value_of_type("OS_UnitaryAuthorityWard")])
    print("#\tOS_District ", dif_types_count[get_value_of_type("OS_District")])
    print("#\tOS_MetropolitanDistrict ", dif_types_count[get_value_of_type("OS_MetropolitanDistrict")])
    print("#\tOS_MetropolitanDistrictWard ", dif_types_count[get_value_of_type("OS_MetropolitanDistrictWard")])
    print("#\tOS_LondonBorough ", dif_types_count[get_value_of_type("OS_LondonBorough")])
    print("#\tOS_UnitaryAuthority ", dif_types_count[get_value_of_type("OS_UnitaryAuthority")])
    print("#\tOS_LondonBoroughWard ", dif_types_count[get_value_of_type("OS_LondonBoroughWard")])
    print("#\tOS_County ", dif_types_count[get_value_of_type("OS_County")])
    print("#\tOS_EuropeanRegion ", dif_types_count[get_value_of_type("OS_EuropeanRegion")])
    print("#\tOS_GreaterLondonAuthority ", dif_types_count[get_value_of_type("OS_GreaterLondonAuthority")])
    print("#\tOS_COMMUNITYWARD ", dif_types_count[get_value_of_type("OS_COMMUNITYWARD")])
    print("#\tOS_COMMUNITY ", dif_types_count[get_value_of_type("OS_COMMUNITY")])
    print("#\tOS_CCOMMUNITY ", dif_types_count[get_value_of_type("OS_CCOMMUNITY")])


# GeeksforGeeks, Python | Print all the common elements of two lists
# https://www.geeksforgeeks.org/python-print-common-elements-two-lists/
def common_member(a, b):
    a_set = set(a)
    b_set = set(b)
    if a_set & b_set:
        print(a_set & b_set)
        c = a_set & b_set
        print(len(c))
        return list(c)
    else:
        print("No common elements")
