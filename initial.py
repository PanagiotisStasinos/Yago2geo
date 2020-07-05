from rdflib.graph import Graph
from location.KGraph import read_RDF_Graph_and_store_Locations, find_center_distances
import time

################################
#   does everything from the beginning
################################
from preprocess import get_topological_info, get_statistics_of_topological_and_matches_files, store_random_walks2

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
end = time.time()

print("Processor time (in seconds):", end)
print("Time elapsed:", end - start)
# NO MATCHES NEEDED
# weighted_graph.concat_matches()

weighted_graph.concat_geo()
weighted_graph.print_statistics()

print("read topological")
get_topological_info(weighted_graph)
weighted_graph.print_statistics()
get_statistics_of_topological_and_matches_files(weighted_graph)
# exit(1)
print("find distances")
find_center_distances(weighted_graph)
weighted_graph.print_statistics()

#########################################################################################
print("separate data")
weighted_graph.separate_data()
weighted_graph.print_statistics()
##########################################################################################

print("random walk")
# store_random_walks(weighted_graph)
store_random_walks2(weighted_graph)
weighted_graph.print_statistics()

from network import simple_nn
simple_nn.simple_nn_7()     # 0.98

# bayesian_opt.optimize()

end = time.time()

print("Processor time (in seconds):", end)
print("Time elapsed:", end - start)
print("END")