
import os

file_string = "CODE:"

file_order_string = ""



file_count = 0

directory = 'projects/final/'
for dirpath, dirnames, filenames in os.walk(directory):
    for filename in filenames:
        if filename.endswith('.py')  or  filename.endswith('.json'):
            with open(os.path.join(dirpath, filename)) as f:
                file_string += "\n\n\n\nFile: " + dirpath + '/' + filename + "\n"
                file_string += f.read()
                file_count += 1
                #print(f.read())

file_string += f"\n\n\n\nTotal files: {file_count}\n"

#print(file_string)

with open("projects/final/saved_text.txt", 'w') as f:
    f.write(file_string)




# directories
# rptree.py

#"""This module provides RP Tree main module."""

import os
import pathlib

PIPE = "│"
ELBOW = "└──"
TEE = "├──"
PIPE_PREFIX = "│   "
SPACE_PREFIX = "    "


