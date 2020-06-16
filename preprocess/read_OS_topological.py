from rdflib.graph import Graph
import utils


###############################################
#   >   prints the total number of
#       RDFs in OS_topological.nt file
#   >   reads RDFs of OS_topological and
#           - if predicate is #sfTouches adds to object's Touches
#           list the subject location and vice versa
#           - if predicate is #sfWithin adds to subject's Within
#           list the object location and adds to object's Includes
#           list the subject location
###############################################
def get_topological_info(weighted_graph):
    print("\t TOPOLOGICAL")
    g = Graph()
    g.parse("../datasets/yago2geo_uk/os/OS_topological.nt", format="nt")  # works
    print("graph has %s statements." % len(g))
    for subject, predicate, obj in g:
        subject_name = utils.get_url_value(subject)
        obj_name = utils.get_url_value(obj)
        if weighted_graph.location_exists(utils.get_url_value(subject)) and weighted_graph.location_exists(
                utils.get_url_value(obj)):
            if str(predicate) == "http://www.opengis.net/ont/geosparql#sfTouches":
                weighted_graph.add_touches(subject_name, obj_name)
            else:
                weighted_graph.add_within(subject_name, obj_name)


###############################################
#   MATCHES
#   >   prints the total number of RDFs in OS_matches.nt file
#   >   prints number of objects that exist in graph and the number of those that don't
#  TOPOLOGICAL
#   >   prints the total number of RDFs in OS_topological.nt file
#   >   subject
#         - number of subjects exist in locations_csv
#         - number of subjects exist in matches file
#         - number of subjects exist in objects
#         - number of subjects that don't exist in objects
#   >   object
#         - number of objects exist in locations_csv
#         - number of objects exist in matches file
#         - number of objects exist in objects
#         - number of objects that don't exist in objects
#   >   garbage
#         - number of subjects , number of those that exist in matches
#         - number of objects , number of those that exist in matches
###############################################
def get_statistics_of_topological_and_matches_files(weighted_graph):
    print("\t MATCHES ")
    matches_object = {}
    object_exists = {}
    object_doesnt_exists = {}
    g = Graph()
    g.parse("../datasets/yago2geo_uk/os/OS_matches.nt", format="nt")  # works
    print("graph has %s statements." % len(g))
    obj_count = 0   # count of objects that exist in graph
    for subject, predicate, obj in g:
        if weighted_graph.location_exists(utils.get_url_value(obj)):    # if object exists in graph
            obj_count = obj_count + 1
            object_exists[utils.get_url_value(obj)] = utils.get_url_value(subject)
        else:
            object_doesnt_exists[utils.get_url_value(obj)] = utils.get_url_value(subject)
        matches_object[utils.get_url_value(obj)] = utils.get_url_value(subject)
    print("total number of objects in OS_matches ", len(matches_object), " , ", obj_count, " of those exist in graph")
    print(len(object_exists), " exist in graph - ", len(object_doesnt_exists), " don't exist in graph")

    print("\t TOPOLOGICAL")
    g = Graph()
    g.parse("../datasets/yago2geo_uk/os/OS_topological.nt", format="nt")  # works
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

    print("subject\n\t exists in locations_csv ", subject_count_2, "\n\t exists in matches file ", s_count,
          "\n\t exists in objects ", count, "\n\t doesnt exist in objects ", s1_count)
    print("obj\n\t exists in locations_csv ", obj_count_2, "\n\t exists in matches file ", o1_count,
          "\n\t exists in objects ", o_count, "\n\t doesnt exist in objects ", o2_count)
    print("garbage sub ", garbage_s, " exists ", s_garbage_count, "\n\tobj ", garbage_o, " exists ", o_garbage_count)
