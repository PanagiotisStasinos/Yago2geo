import os

fp1 = open("C:/Users/panai/Desktop/yago2geo_uk/os/OS_extended_part1.ttl", "r")
num_lines = sum(1 for line in fp1)
print(num_lines)
fp1.close()
a1 = os.stat('C:/Users/panai/Desktop/yago2geo_uk/os/OS_extended_part1.ttl')
print(a1)
a2 = os.stat('C:/Users/panai/Desktop/yago2geo_uk/os/OS_extended_part1.ttl').st_size
print(a2)


fp2 = open("C:/Users/panai/Desktop/yago2geo_uk/os/OS_extended_part2.ttl", "r")
num_lines = sum(1 for line in fp2)
print(num_lines)
fp2.close()
a1 = os.stat('C:/Users/panai/Desktop/yago2geo_uk/os/OS_extended_part2.ttl')
print(a1)
a2 = os.stat('C:/Users/panai/Desktop/yago2geo_uk/os/OS_extended_part2.ttl').st_size
print(a2)
