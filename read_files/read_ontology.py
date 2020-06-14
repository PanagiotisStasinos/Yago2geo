from rdflib import Namespace, Literal, URIRef
from rdflib.graph import Graph, ConjunctiveGraph
from rdflib.plugins.memory import IOMemory

g = Graph()
g.parse("C:/Users/panai/Desktop/yago2geo_uk/os/OS_ontology.ttl", format="turtle")          # works

print("graph has %s statements." % len(g))

print("--- printing count POLYGON ---")
i = 0
subject_list = []

subject_with_Literal_list = []
subject_with_URIRef_list = []

subject_Literal_with_POLYGON_list = []
subject_Literal_with_MULTIPOLYGON_list = []

subject_URIRef_with_POLYGON_list = []
subject_URIRef_with_MULTIPOLYGON_list = []

object_type_list = []

for subject, predicate, obj in g:
    #     print((subject,predicate,object))
    subject_list.append(subject)
    object_type_list.append(str(type(obj)))

    if str(type(obj)) == "<class 'rdflib.term.Literal'>":
        subject_with_Literal_list.append(obj)
        if " POLYGON " in obj:
            subject_Literal_with_POLYGON_list.append(obj)
        elif " MULTIPOLYGON " in obj:
            subject_Literal_with_MULTIPOLYGON_list.append(obj)

        # print(object)
        # print((i, type(object)))


    # if str(type(object)) == "<class 'rdflib.term.URIRef'>":
    else:
        subject_with_URIRef_list.append(obj)
        if " POLYGON " in obj:
            subject_URIRef_with_POLYGON_list.append(obj)
        elif " MULTIPOLYGON " in obj:
            subject_URIRef_with_MULTIPOLYGON_list.append(obj)

        # print(object)
        # print((i, type(object)))
    i = i + 1

from collections import Counter
print("unique subjects : ", len(Counter(subject_list).keys()), " / ", len(subject_list))
print("unique types of objects / total objects: ", len(Counter(object_type_list).keys()), " / ", len(object_type_list), "\n")

print("unique_Literal_object / total_Literal_object: ", len(Counter(subject_with_Literal_list).keys()), " / ", len(subject_with_Literal_list))
print("POLYGON_Literal_object / total_Literal_object: ", len(Counter(subject_Literal_with_POLYGON_list)), " / ", len(subject_with_Literal_list))
print("MULTIPOLYGON_Literal_object / total_Literal_object: ", len(Counter(subject_Literal_with_MULTIPOLYGON_list)), " / ", len(subject_with_Literal_list), "\n")

print("unique_URIRef_object / total_URIRef_object: ", len(Counter(subject_with_URIRef_list).keys()), " / ", len(subject_with_URIRef_list))
print("POLYGON_URIRef_object / total_URIRef_object: ", len(Counter(subject_URIRef_with_POLYGON_list)), " / ", len(subject_with_URIRef_list))
print("MULTIPOLYGON_URIRef_object / total_URIRef_object: ", len(Counter(subject_URIRef_with_MULTIPOLYGON_list)), " / ", len(subject_with_URIRef_list))