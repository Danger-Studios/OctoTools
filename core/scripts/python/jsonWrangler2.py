import os
import sys
import json
import random


# Write json dictionary to file
def write_json(json_dict, json_file):
    with open(json_file, 'w') as outfile:
        json.dump(json_dict, outfile, indent=4)
    return

# Read json dictionary from file
def read_json(json_file):
    with open(json_file, 'r') as infile:
        json_dict = json.load(infile)
        # If file is not empty, return json dictionary
        if json_dict:
            return json_dict
        else:
            write_json(create_json(), json_file)

