#!/usr/bin/env python3

# Improved script to change the header of a g09 com file.
# Options are to modify number of cores, memory, or computation.

import os
import sys
import argparse as ap

if __name__ == '__main__':
  p = ap.ArgumentParser(description = \
    'Modify the header of one or more g09 files')
  parser.add_argument('--cores', type = int,
    help = 'Number of cores for g09 to use')
  parser.add_argument('--mem', type = int,
    help = 'Amount of memory, in megabytes, to use')
  parser.add_argument('--param', type = str,
    help = 'g09 job parameters. Use quotes to enclose spaces')
  parser.add_argument('files', nargs='+',
    help = 'list of .com files to modify the headers of')
  args = parser.parse_args()
  
  if args.cores is None and args.mem is None and args.param is None:
    print('No changes to files specified, exiting')
    sys.exit(0)
  
  for com_file in args.files:
    com_lines = list()
    with open(com_file, 'r') as f:
      com_lines = f.readlines()
    
  
  


