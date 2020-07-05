from rdflib.graph import Graph
from location.KGraph import read_RDF_Graph_and_store_Locations
import time

################################
#   reads OS_extended and OS_new files, get the locations
#   and stores them in the datasets/locations_csv/locations_1.csv and .json
################################
start = time.time()

extended_part1_file_RDF_graph = Graph()
extended_part1_file_RDF_graph.parse("C:/Users/panai/Desktop/yago2geo_uk/os/OS_extended_p1.ttl", format="n3")
print("len", len(extended_part1_file_RDF_graph))
#
extended_part2_file_RDF_graph = Graph()
extended_part2_file_RDF_graph.parse("C:/Users/panai/Desktop/yago2geo_uk/os/OS_extended_p2.ttl", format="n3")
print("len", len(extended_part2_file_RDF_graph))
# #
extended_part3_file_RDF_graph = Graph()
extended_part3_file_RDF_graph.parse("C:/Users/panai/Desktop/yago2geo_uk/os/OS_extended_p3.ttl", format="n3")
print("len", len(extended_part3_file_RDF_graph))
# # #
extended_part4_file_RDF_graph = Graph()
extended_part4_file_RDF_graph.parse("C:/Users/panai/Desktop/yago2geo_uk/os/OS_extended_p4.ttl", format="n3")
print("len", len(extended_part4_file_RDF_graph))
# # # #
new_file_RDF_graph = Graph()
new_file_RDF_graph.parse("C:/Users/panai/Desktop/yago2geo_uk/os/OS_new.ttl", format="n3")
print("len", len(new_file_RDF_graph))
# # # # #
# main_graph = extended_part1_file_RDF_graph + extended_part2_file_RDF_graph + extended_part3_file_RDF_graph + \
#              extended_part4_file_RDF_graph
main_graph = extended_part1_file_RDF_graph + extended_part2_file_RDF_graph + extended_part3_file_RDF_graph + \
             extended_part4_file_RDF_graph + new_file_RDF_graph
# main_graph = new_file_RDF_graph

print("len", len(main_graph))


weighted_graph = read_RDF_Graph_and_store_Locations(main_graph)
# weighted_graph.print_statistics()

# NO MATCHES NEEDED
# weighted_graph.concat_matches()

weighted_graph.concat_geo()
weighted_graph.print_statistics()

weighted_graph.write_to_csv()
weighted_graph.print_statistics()

weighted_graph.clear()
main_graph.close()

end = time.time()

print("Processor time (in seconds):", end)
print("Time elapsed:", end - start)
print("END")
