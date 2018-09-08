#!/usr/bin/python

import cloudconvert
import argparse

import os

# CLI init
parser = argparse.ArgumentParser(description = 'Convert certain image file formats',
                                  epilog = 'Uses cloudconvert API')

parser.add_argument('input_file', help = 'Input file relative to current path')
parser.add_argument('output_extension', help = 'Output file relative to current path')
parser.add_argument('-d', '--depth', help = 'Define depth if looking into a folder', type = int, default = 1)

args = parser.parse_args()

# API init, put a key in the API_KEY.txt file
API_KEY_TXT = open("API_KEY.txt", 'r')
API_KEY = API_KEY_TXT.read()
API_KEY_TXT.close()

api = cloudconvert.Api(API_KEY)

# Get only extension of file, return no dot
def get_extension(filename):
    names = filename.split('.')

    if len(names) == 1 and not names[0]:
        return get_files(input)
    elif len (names) > 1:
        return names[-1]

# Get files, uses os.walk to walk all the subtrees. 
# All file paths are appended to paths. Returns this list plus a list of extensions of the paths 
def get_files(input):
    paths = []
    
    if (os.path.isdir(input)):
        base_count = input.count(os.path.sep)

        for root, folders, files in os.walk(input):
            if (root.count(os.path.sep) - base_count >= args.depth):
                break

            paths.extend([os.path.join(root, file) for file in files])
    elif (os.path.isfile(input)):
        paths.append(input)

    exts = [get_extension(path) for path in paths]
    print(paths)
    return paths, exts

# Actual conversion using the cloudconvert api, simply a for loop over all the paths
def convert():
    paths, exts = get_files(args.input_file)
    
    for i in range(len(paths)):
        path = paths[i]
        ext = exts[i]
        
        path_out = ''.join(path.split('.')[:-1]) + '.' + args.output_extension
        if (os.path.isfile(path_out)):
            print("File exists: {}\n".format(path_out))
        else:
            p = api.convert({
                'inputformat' : ext,
                'outputformat' :args.output_extension,
                'input' : 'upload',
                'file' : open(path, 'rb')           
            })

            print ("Processing {}".format(path_out))
            p.wait()

            print ("Downloading {}\n".format(path_out))
            p.download(path_out)

if __name__ == '__main__':
    convert()

