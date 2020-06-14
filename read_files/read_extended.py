from rdflib import Namespace, Literal, URIRef
from rdflib.graph import Graph, ConjunctiveGraph
from rdflib.plugins.memory import IOMemory
from collections import Counter


class OS_extended_RDF_graph:
    def __init__(self):
        self.count = 0
        self.count_subject = 0
        self.g = Graph()

    def print_info(self):
        print("subject : " + self.count)
        print("predicate : " + self.count_subject)

    def store_data(self, file):
        # self.g = Graph()
        # g.parse("C:/Users/panai/Desktop/yago2geo_uk/os/OS_extended_small.ttl", format="n3")       # not working (maybe very large file)

        self.g.parse("../datasets/yago2geo_uk/os/OS_extended_p1.ttl", format="n3")  # works 1/4
        print("1) graph has %s statements" % len(self.g))
        prev = len(self.g)
        self.g.parse("../datasets/yago2geo_uk/os/OS_extended_p2.ttl", format="n3")  # works 2/4
        print("2) graph has ", len(self.g), " statements, new", (len(self.g) - prev))
        prev = len(self.g)
        self.g.parse("../datasets/yago2geo_uk/os/OS_extended_p3.ttl", format="n3")  # works 3/4
        print("3) graph has ", len(self.g), " statements, new", (len(self.g) - prev))
        prev = len(self.g)
        self.g.parse("../datasets/yago2geo_uk/os/OS_extended_p4.ttl", format="n3")  # works 4/4
        print("4) graph has ", len(self.g), " statements, new", (len(self.g) - prev))
        prev = len(self.g)

        # g.parse("C:/Users/panai/Desktop/yago2geo_uk/os/OS_matches.nt", format="nt")           # works
        # g.parse("C:/Users/panai/Desktop/yago2geo_uk/os/OS_new.ttl", format="turtle")          # works
        # g.parse("C:/Users/panai/Desktop/yago2geo_uk/os/OS_ontology.ttl", format="turtle")     # works
        # g.parse("C:/Users/panai/Desktop/yago2geo_uk/os/OS_topological.nt", format="nt")       # works

        # test
        # g.parse("C:/Users/panai/Desktop/yago2geo_uk/os/OS_extended_small.ttl", format="n3")

        print("graph has %s statements." % len(self.g))
        # prints graph has 79 statements.
        # import pprint
        #
        # for stmt in g:
        #     pprint.pprint(stmt)

        print("--- printing count POLYGON ---")
        # i = 0
        # subject_list = []
        #
        # subject_with_Literal_list = []
        # subject_with_URIRef_list = []
        #
        # subject_Literal_with_POLYGON_list = []
        # subject_Literal_with_MULTIPOLYGON_list = []
        #
        # subject_URIRef_with_POLYGON_list = []
        # subject_URIRef_with_MULTIPOLYGON_list = []
        #
        # object_type_list = []
        #
        # for subject, predicate, obj in self.g:
        #     #     print((subject,predicate,object))
        #     subject_list.append(subject)
        #     object_type_list.append(str(type(obj)))
        #
        #     if str(type(obj)) == "<class 'rdflib.term.Literal'>":
        #         subject_with_Literal_list.append(obj)
        #         if " POLYGON " in obj:
        #             subject_Literal_with_POLYGON_list.append(obj)
        #         elif " MULTIPOLYGON " in obj:
        #             subject_Literal_with_MULTIPOLYGON_list.append(obj)
        #
        #         # print(object)
        #         # print((i, type(object)))
        #
        #     # if str(type(object)) == "<class 'rdflib.term.URIRef'>":
        #     else:
        #         subject_with_URIRef_list.append(obj)
        #         if " POLYGON " in obj:
        #             subject_URIRef_with_POLYGON_list.append(obj)
        #         elif " MULTIPOLYGON " in obj:
        #             subject_URIRef_with_MULTIPOLYGON_list.append(obj)
        #
        #         # print(object)
        #         # print((i, type(object)))
        #     i = i + 1
        #
        # from collections import Counter
        #
        # print("unique subjects : ", len(Counter(subject_list).keys()), " / ", len(subject_list))
        # print("unique types of objects / total objects: ", len(Counter(object_type_list).keys()), " / ",
        #       len(object_type_list),
        #       "\n")
        #
        # print("unique_Literal_object / total_Literal_object: ", len(Counter(subject_with_Literal_list).keys()), " / ",
        #       len(subject_with_Literal_list))
        # print("POLYGON_Literal_object / total_Literal_object: ", len(Counter(subject_Literal_with_POLYGON_list)), " / ",
        #       len(subject_with_Literal_list))
        # print("MULTIPOLYGON_Literal_object / total_Literal_object: ",
        #       len(Counter(subject_Literal_with_MULTIPOLYGON_list)),
        #       " / ", len(subject_with_Literal_list), "\n")
        #
        # print("unique_URIRef_object / total_URIRef_object: ", len(Counter(subject_with_URIRef_list).keys()), " / ",
        #       len(subject_with_URIRef_list))
        # print("POLYGON_URIRef_object / total_URIRef_object: ", len(Counter(subject_URIRef_with_POLYGON_list)), " / ",
        #       len(subject_with_URIRef_list))
        # print("MULTIPOLYGON_URIRef_object / total_URIRef_object: ", len(Counter(subject_URIRef_with_MULTIPOLYGON_list)),
        #       " / ",
        #       len(subject_with_URIRef_list))
        i = 0
        subject_list = []
        predicate_list = []
        object_list = []

        aswkt_counter = 0
        hasOS_Name_Counter = 0
        hasGeometry_Counter = 0
        syntax_type_counter = 0
        hasOS_ID_counter = 0

        aswkt_obj_list = []
        hasOS_Name_list = []
        hasGeometry_list = []
        syntax_type_list = []
        hasOS_ID_list = []

        subject_with_Literal_list = []
        subject_with_URIRef_list = []

        subject_Literal_with_POLYGON_list = []
        subject_Literal_with_MULTIPOLYGON_list = []

        subject_URIRef_with_POLYGON_list = []
        subject_URIRef_with_MULTIPOLYGON_list = []

        object_type_list = []

        count_uriref = 0

        for subject, predicate, obj in self.g:
            #     print((subject,predicate,object))
            subject_list.append(subject)
            predicate_list.append(predicate)
            object_list.append(obj)

            object_type_list.append(str(type(obj)))

            if str(predicate) == "http://www.opengis.net/ont/geosparql#asWKT":
                aswkt_counter = aswkt_counter + 1
                aswkt_obj_list.append(obj)
            elif str(predicate) == "http://kr.di.uoa.gr/yago2geo/ontology/hasOS_Name":
                hasOS_Name_Counter = hasOS_Name_Counter + 1
                hasOS_Name_list.append(obj)
            elif str(predicate) == "http://www.opengis.net/ont/geosparql#hasGeometry":
                hasGeometry_Counter = hasGeometry_Counter + 1
                hasGeometry_list.append(obj)
            elif str(predicate) == "http://www.w3.org/1999/02/22-rdf-syntax-ns#type":
                syntax_type_counter = syntax_type_counter + 1
                syntax_type_list.append(obj)
                # print(type(obj))
            elif str(predicate) == "http://kr.di.uoa.gr/yago2geo/ontology/hasOS_ID":
                hasOS_ID_counter = hasOS_ID_counter + 1
                hasOS_ID_list.append(obj)

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
                count_uriref = count_uriref + 1
                subject_with_URIRef_list.append(obj)
                if " POLYGON " in obj:
                    subject_URIRef_with_POLYGON_list.append(obj)
                elif " MULTIPOLYGON " in obj:
                    subject_URIRef_with_MULTIPOLYGON_list.append(obj)

                # print(object)
                # print((i, type(object)))
            i = i + 1

        print("unique subjects : ", len(Counter(subject_list).keys()), " / ", len(subject_list))
        print("unique predicates : ", len(Counter(predicate_list).keys()), " / ", len(predicate_list))
        for pred in Counter(predicate_list).keys():
            print(pred)
        for types in Counter(syntax_type_list).keys():
            print(types)

        print("-> aswkt ", aswkt_counter, " ", len(aswkt_obj_list), " ", len(Counter(aswkt_obj_list).keys()))
        count1 = 0
        count2 = 0
        for wkt in aswkt_obj_list:
            if str(type(wkt)) == "<class 'rdflib.term.Literal'>":
                count1 = count1 + 1
            else:
                count2 = count2 + 1
        print("AWK Literal ", count1, " URIRef ", count2, "\n")
        # for wkt in Counter(aswkt_obj_list).keys():
        #     print(wkt.n3())

        print("-> hasOS_Name ", hasOS_Name_Counter, " ", len(hasOS_Name_list), " ",
              len(Counter(hasOS_Name_list).keys()))
        count1 = 0
        count2 = 0
        for name in hasOS_Name_list:
            if str(type(name)) == "<class 'rdflib.term.Literal'>":
                count1 = count1 + 1
            else:
                count2 = count2 + 1
        print("Name Literal ", count1, " URIRef ", count2, "\n")
        # for name in hasOS_Name_list:
        #     print(name)

        print("-> hasGeometry ", hasGeometry_Counter, " ", len(hasGeometry_list), " ",
              len(Counter(hasGeometry_list).keys()))
        count1 = 0
        count2 = 0
        for geo in hasGeometry_list:
            if str(type(geo)) == "<class 'rdflib.term.Literal'>":
                count1 = count1 + 1
            else:
                count2 = count2 + 1
        print("hasGeometry Literal ", count1, " URIRef ", count2, "\n")

        print("-> type ", syntax_type_counter, " ", len(syntax_type_list), " ", len(Counter(syntax_type_list).keys()))
        count1 = 0
        count2 = 0
        for s in syntax_type_list:
            if str(type(s)) == "<class 'rdflib.term.Literal'>":
                count1 = count1 + 1
            else:
                count2 = count2 + 1
        print("syntax_type Literal ", count1, " URIRef ", count2, "\n")

        print("-> hasOS_ID ", hasOS_ID_counter, " ", len(hasOS_ID_list), " ", len(Counter(hasOS_ID_list).keys()))
        count1 = 0
        count2 = 0
        for s in hasOS_ID_list:
            if str(type(s)) == "<class 'rdflib.term.Literal'>":
                count1 = count1 + 1
            else:
                count2 = count2 + 1
        print("hasOS_ID Literal ", count1, " URIRef ", count2, "\n")

        print("unique objects : ", len(Counter(object_list).keys()), " / ", len(object_list))


a = OS_extended_RDF_graph()
a.store_data("name")
