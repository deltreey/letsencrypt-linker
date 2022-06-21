#! /usr/bin/python3

import argparse
import os.path
from os.path import relpath
import re


def main(input, output):
    if not os.path.isdir(input) or not os.path.isdir(output):
        print('Input and Output folders must both be directories')
        return
    print('Creating Folders in Output Directory...')
    # Create same folders in output folder
    input_directories = [dir for dir in os.listdir(input) if os.path.isdir(os.path.join(input, dir))]
    print(input_directories)
    for directory in input_directories:
        try:
            os.mkdir(os.path.join(output, directory))
        except Exception as e:
            print(e)
    print('Creating Symlinks to Latest file in Each Folder...')
    # Create Symlinks
    for directory in input_directories:
        cert_files = [file for file in os.listdir(os.path.join(input, directory)) if 'cert' in file]
        # Find highest cert file
        highest = 1
        for cert_file in cert_files:
            regex = r'cert(\d+)\.pem' # https://rubular.com/r/5jWqydh86aXWUR
            matches = re.search(regex, cert_file)
            number = matches.group(1)
            if int(matches.group(1)) > highest:
                highest = int(matches.group(1))
        os.symlink(relpath(os.path.join(input, directory, f'cert{highest}.pem'),
                           os.path.join(output, directory)),
                   os.path.join(output, directory, 'cert.pem'))
        os.symlink(relpath(os.path.join(input, directory, f'chain{highest}.pem'),
                           os.path.join(output, directory)),
                   os.path.join(output, directory, 'chain.pem'))
        os.symlink(relpath(os.path.join(input, directory, f'fullchain{highest}.pem'),
                           os.path.join(output, directory)),
                   os.path.join(output, directory, 'fullchain.pem'))
        os.symlink(relpath(os.path.join(input, directory, f'privkey{highest}.pem'),
                           os.path.join(output, directory)),
                   os.path.join(output, directory, 'privkey.pem'))
    print('Done.')



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create Symlinks for LetsEncrypt Keys')
    parser.add_argument('-i', '--input', required=True)
    parser.add_argument('-o', '--output', required=True)
    args = parser.parse_args()
    main(args.input, args.output)
