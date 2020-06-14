import os

f = open("C:/Users/panai/Desktop/yago2geo_uk/os/OS_extended.ttl", "r")
num_lines = sum(1 for line in f)
print(num_lines)
f.close()

a1 = os.stat('C:/Users/panai/Desktop/yago2geo_uk/os/OS_extended.ttl')
print(a1)
a2 = os.stat('C:/Users/panai/Desktop/yago2geo_uk/os/OS_extended.ttl').st_size
print(a2)

fp = open("C:/Users/panai/Desktop/yago2geo_uk/os/OS_extended.ttl")
fp1 = open("C:/Users/panai/Desktop/yago2geo_uk/os/OS_extended_p1.ttl", "a")
fp2 = open("C:/Users/panai/Desktop/yago2geo_uk/os/OS_extended_p2.ttl", "a")
fp3 = open("C:/Users/panai/Desktop/yago2geo_uk/os/OS_extended_p3.ttl", "a")
fp4 = open("C:/Users/panai/Desktop/yago2geo_uk/os/OS_extended_p4.ttl", "a")

for i, line in enumerate(fp):
    if i <= 40001:
        fp1.write(line)
        # print((i, line))
    elif i <= 79998:
        fp2.write(line)
        # print((i, line))
    elif i <= 120000:
        fp3.write(line)
        # print((i, line))
    else:
        fp4.write(line)
    #     print((i, line))

fp.close()
fp1.close()
fp2.close()
fp3.close()
fp4.close()
