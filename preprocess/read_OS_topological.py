from rdflib.graph import Graph, ConjunctiveGraph
from collections import Counter
from preprocess import utils
from termcolor import colored


def get_topological_info(weighted_graph):
    print("\t TOPOLOGICAL")
    g = Graph()
    g.parse("C:/Users/panai/Desktop/yago2geo_uk/os/OS_topological.nt", format="nt")  # works
    print("graph has %s statements." % len(g))
    for subject, predicate, obj in g:
        subject_name = utils.get_url_value(subject)
        obj_name = utils.get_url_value(obj)
        if weighted_graph.location_exists(utils.get_url_value(subject)) and weighted_graph.location_exists(utils.get_url_value(obj)):
            if str(predicate) == "http://www.opengis.net/ont/geosparql#sfTouches":
                weighted_graph.add_touches(subject_name, obj_name)
            else:
                weighted_graph.add_within(subject_name, obj_name)


def get_topological_statistics(weighted_graph):
    print("\t MATCHES ")
    matches_object = {}
    object_exists = {}
    object_doesnt_exists = {}
    g = Graph()
    g.parse("C:/Users/panai/Desktop/yago2geo_uk/os/OS_matches.nt", format="nt")  # works
    print("graph has %s statements." % len(g))
    obj_count = 0
    for subject, predicate, obj in g:
        if weighted_graph.location_exists(utils.get_url_value(obj)):
            obj_count = obj_count + 1
            object_exists[utils.get_url_value(obj)] = utils.get_url_value(subject)
        else:
            object_doesnt_exists[utils.get_url_value(obj)] = utils.get_url_value(subject)
        matches_object[utils.get_url_value(obj)] = utils.get_url_value(subject)
    print("object matches len ", len(matches_object), " count ", obj_count)
    print(len(object_exists), " - ", len(object_doesnt_exists))

    print("\t TOPOLOGICAL")
    g = Graph()
    g.parse("C:/Users/panai/Desktop/yago2geo_uk/os/OS_topological.nt", format="nt")  # works
    print("graph has %s statements." % len(g))
    subject_name_list_top = []
    object_name_list_top = []
    subject_count_2 = 0
    s_count = 0
    s1_count = 0
    obj_count_2 = 0
    count = 0
    o1_count = 0
    o_count = 0
    o2_count = 0
    garbage_s = 0
    garbage_o = 0
    s_garbage_count = 0
    o_garbage_count = 0
    for subject, predicate, obj in g:
        subject_name_list_top.append(utils.get_url_value(subject))
        object_name_list_top.append(utils.get_url_value(obj))
        if weighted_graph.location_exists(utils.get_url_value(subject)):
            subject_count_2 = subject_count_2 + 1
            if utils.get_url_value(subject) in matches_object:
                s_count = s_count + 1
            if utils.get_url_value(subject) in object_exists:
                count = count + 1
            else:
                s1_count = s1_count + 1
        else:
            garbage_s = garbage_s + 1
            if utils.get_url_value(subject) in matches_object:
                s_garbage_count = s_garbage_count + 1
        if weighted_graph.location_exists(utils.get_url_value(obj)):
            obj_count_2 = obj_count_2 + 1
            if utils.get_url_value(obj) in matches_object:
                o1_count = o1_count + 1
            if utils.get_url_value(obj) in object_exists:
                o_count = o_count + 1
            else:
                o2_count = o2_count + 1
        else:
            garbage_o = garbage_o + 1
            if utils.get_url_value(obj) in matches_object:
                o_garbage_count = o_garbage_count + 1

    print("subject\n\t exists in locations ", subject_count_2, "\n\t exists in matches file ", s_count,
          "\n\t exists in objects ", count, "\n\t doesnt exist in objects ", s1_count)
    print("obj\n\t exists in locations ", obj_count_2, "\n\t exists in matches file ", o1_count,
          "\n\t exists in objects ", o_count, "\n\t doesnt exist in objects ", o2_count)
    print("garbage sub ", garbage_s, " exists ", s_garbage_count, "\n\tobj ", garbage_o, " exists ", o_garbage_count)
