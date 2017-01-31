#!/usr/bin/env python3

# Split a single mol2 file into several .com files
# Optionally with a given param, mem, and cores resources.

import argparse
import re

# Function read through the lines of a mol2 file and return the starting and
# ending line numbers of each molecule, based off the @<TRIPOS>MOLECULE tags
# Input: list of lines of the mol2 file
# Output: List of slices into the list for each molecule 
#   These slices can be used as array indices
def get_molecule_slices(mol2_lines):
  start_idx = None
  end_idx = None
  output = list()
  # calculate the first start idx.
  for idx, line in enumerate(mol2_lines):
    moltag_idx = line.find('@<TRIPOS>MOLECULE')
    if moltag_idx != -1:
      # Found the molecule tag, now three cases.
      if start_idx is None:
        start_idx = idx
      else:
        end_idx = idx
        output.append( slice(start_idx, end_idx) )
        start_idx = end_idx
  output.append( slice(end_idx, len(mol2_lines) - 1) )
  return output

# Give a list of lines from a molecule section of a mol2 file
# (starting with a @<TRIPOS>MOLECULE tag), get the index of the 
# line after the @<TRIPOS>ATOM tag
def get_atom_start(molecule_lines):
  for idx, line in enumerate(molecule_lines):
    if line.find('@<TRIPOS>ATOM') != -1:
      return idx + 1

# Find and return the atom name within an atom name/number composite string.
def get_atom_name(atom_name_token):
  digit_idx = re.search('\d', atom_name_token).start()
  return atom_name_token[:digit_idx]
  
class Mol2Molecule:
  def __init__(self, lines):
    self.conf_name = lines[1].strip()
    count_tokens = lines[2].strip().split()
    self.atom_count = int(count_tokens[0])
    self.bond_count = int(count_tokens[1])
    self.atom_positions = list() # 3-tuples of floats.
    self.atom_names = list()  # single-character strings.
    atom_start = get_atom_start(lines)
    for i in range(atom_start, atom_start + self.atom_count):
      atom_tokens = lines[i].strip().split()
      atom_name = get_atom_name(atom_tokens[1].strip())
      self.atom_names.append(atom_name)
      atom_pos = tuple([float(token.strip()) for token in atom_tokens[2:5]])
      self.atom_positions.append(atom_pos)

def create_com_file(molecule, filename, route, cores,
                    memory, charge, multiplicity):
  with open(filename, 'w') as f:
    # Write the link-0 commands - cores and memory
    f.write('%nprocshared={0}\n'.format(cores))
    f.write('%mem={0}\n'.format(memory))
    # Write the route card
    f.write('# {0} \n'.format(route))
    # Required blank line, title card, required blank line
    f.write('\n{0}\n\n'.format(molecule.conf_name))
    # charge and multiplicity, molecule spec.
    f.write('{0} {1}\n'.format(charge, multiplicity))
    # the atom positions.
    for idx, name in enumerate(molecule.atom_names):
      x, y, z = molecule.atom_positions[idx][:]
      f.write(' {0}  {1:08f}  {2:08f}  {3:08f}\n'.format(name, x, y, z))
    # Required final newline
    f.write('\n')
    

if __name__ == '__main__':
  p = argparse.ArgumentParser(description = \
    'Split up a mol2 file into .com g09 input files')
  p.add_argument('mol2', help = 'mol2 file to split')
  p.add_argument('--mem', type = str, default = '4GB',
    help = 'Memory, including unit, for each created .com file')
  p.add_argument('--cores', type = int, default = 8,
    help = 'Cores for each created .com file')
  p.add_argument('--route', type = str, 
    default = 'COMPUTATIONAL PARAMETERS HERE',
    help = 'computational parameters string. Used quotes to enclose spaces')
  p.add_argument('--charge', type = int, default = 0,
    help = 'Charge for the molecular input specification. Default 0')
  p.add_argument('--mult', type = int, default = 1,
    help = 'multiplicity for the molecular input specification. Default 1')
  p.add_argument('--prefix', type = str, default = 'g09_mol2_inp',
    help = 'Prefix for each .com file created.')
  args = p.parse_args()
  
  mol2_lines = list()
  with open(args.mol2, 'r') as f:
    mol2_lines = f.readlines()

  slice_list = get_molecule_slices(mol2_lines)
  molecules = [Mol2Molecule(mol2_lines[mol_slice]) for mol_slice in slice_list]
  for molecule in molecules:
    filename = '{0}_{1}.com'.format(args.prefix, molecule.conf_name)
    create_com_file(molecule, filename, args.route, args.cores,
                    args.mem, args.charge, args.mult)
      
    
    
    
  
