import os

print("../datasets/yago2geo_uk/os/OS_extended.ttl")
fp1 = open("../datasets/yago2geo_uk/os/OS_extended.ttl", "r")
num_lines = sum(1 for line in fp1)
print("lines : ", num_lines)
fp1.close()
a1 = os.stat("../datasets/yago2geo_uk/os/OS_extended.ttl")
print("stat  : ", a1)
a2 = os.stat("../datasets/yago2geo_uk/os/OS_extended.ttl").st_size
print("size  : ", a2, "\n")

for i in range(1,5):
    print("OS_extended_p"+str(i)+".ttl")
    fp1 = open("../datasets/yago2geo_uk/os/OS_extended_p"+str(i)+".ttl", "r")
    num_lines = sum(1 for line in fp1)
    print("lines : ", num_lines)
    fp1.close()
    a1 = os.stat("../datasets/yago2geo_uk/os/OS_extended_p"+str(i)+".ttl")
    print("stat  : ", a1)
    a2 = os.stat("../datasets/yago2geo_uk/os/OS_extended_p"+str(i)+".ttl").st_size
    print("size  : ", a2, "\n")
