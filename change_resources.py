#!/usr/bin/env python3

import os
import sys
import argparse as ap

if __name__ == '__main__':
  parser = ap.ArgumentParser(description = 'Program to change ' + \
    'resource requests in gaussian programs')
  parser.add_argument('--cores', type=int,
    help = 'number of cores to request')
  parser.add_argument('--mem', type=int,
    help = 'number of megabytes of memory to request')
  parser.add_argument('files', nargs='+',
    help = 'list of .com files to change the resources of')
  args = parser.parse_args()

  if args.cores is None and args.mem is None:
    print('No change to cores or memory, exiting')
    sys.exit(0)

  for com_file in args.files:
    # Read in the file completely.
    com_lines = list()
    with open(com_file, 'r') as f:
      com_lines = f.readlines()

    # If there is a change to the number of cores, find the 
    # line with %nprocsshared and change it.
    if args.cores is not None:
      cores_line = -1
      for i in range(len(com_lines)):
        line = com_lines[i]
        core_idx = line.find('%nprocshared')
        if core_idx != -1:
          cores_line = i
          break
      if cores_line > -1:
        com_lines[cores_line] = '%nprocshared=' + str(args.cores) + '\n'

    # If there is a change to the amount of memory, find the 
    # line with %mem and replace it.
    if args.mem is not None:
      mem_line = -1
      for i in range(len(com_lines)):
        line = com_lines[i]
        mem_idx = line.find('%mem')
        if mem_idx != -1:
          mem_line = i
          break
      if mem_line > -1:
        com_lines[mem_line] = '%mem=' + str(args.mem) + 'MB\n'

    # Write out the new version of the file.
    with open(com_file, 'w') as f:
      f.writelines(com_lines)

