import sys
import json
import os
import struct


def bytes_to_int_list(bytes_str):
    tp = struct.unpack("<{}B".format(len(bytes_str)), bytes_str)
    return list(tp)


file_name = sys.argv[1]
file = open(file_name, "a+")
for path in sys.argv[2:]:
    with open(path, "rb") as input:
         code = input.read()
         #code = json.dumps(bytes_to_int_list(code))
         file.write("\"")
         file.write(os.path.basename(path)[:-3])
         file.write("\"")
         file.write(": ")
         file.write(str(code))
         file.write(",\n")
