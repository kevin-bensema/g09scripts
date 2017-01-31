#!/usr/bin/env python3

import os
import sys
import argparse as ap
import glob

if __name__ == '__main__':
  parser = ap.ArgumentParser(description = 
    'create slurm .sh files for sbatch to submit to the queue')
  parser.add_argument('files', nargs = '+', 
                      help = '.com files to wrap into .sh files')
  parser.add_argument('--sbatch-file', default = 'submit_all.sh',
                      help = 'Name of batch file to call sbatch on ' + \
                      'all jobs wrapped by this script. ' \
                      'Default: submit_all.sh')
  parser.add_argument('--partition', '-p', default='shortrun',
    help = 'Partition to run the jobs in. longrun or shortrun. Shortrun default.\n' + \
           'Longrun runs the job on the server-grade hardware for > several days runs')
  args = parser.parse_args()

  # Do expansion of any * or ? characters using glob.
  lists = [glob.glob(f) for f in args.files]
  expanded_files = list()
  for l in lists:
    expanded_files += l

  # For each expanded [name].com file, create a [name].sh file that
  # calls srun -N1 g09 [name].com on it.
  # The .sh file names will be stored in script_files
  script_files = list()
  for com_file in expanded_files:
    base_name = com_file.split('.')[0]
    script_name = base_name + '.sh'
    with open(script_name, 'w') as f:
      f.write('#!/bin/bash\n')
      f.write('#SBATCH --partition=' + args.partition + '\n')
      f.write('srun -N1 g09 ' + com_file + '\n')
    script_files.append(script_name)

  # Create the submit-all script.
  with open(args.sbatch_file, 'w') as f:
    for script in script_files:
      f.write('sbatch ' + script + '\n')

  # add execute permissions to the submit-all script.
  os.chmod(args.sbatch_file, 0o777)

