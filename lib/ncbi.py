#!/usr/bin/env python3

import random
import subprocess
import math
import pandas as pd


def _run_command(command):
  """
  _run_command: run command and print result
  """
  print('Start executing command:\n{}'.format(command))
  pipe = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
  output, stderr = pipe.communicate()
  exitCode = pipe.returncode
  if (exitCode == 0):
    print('Executed command:\n{}\n'.format(command) +
      'Exit Code: {}\n'.format(exitCode))
  else:
    error_msg = 'Error running command:\n{}\n'.format(command)
    error_msg += 'Exit Code: {}\nOutput:\n{}\nStderr:\n{}'.format(exitCode, output, stderr)
    raise ValueError(error_msg)
    sys.exit(1)
  return (output, stderr)

def fetch_taxonomy_name_from_assembly_id(assembly_id_list, size):
  # shuffle list because otherwise identical entires collapsed, want to minimize
  print("Fetching NCBI TaxIDs from GTDB-used NCBI Assembly IDs")
  print("Number of IDs to link: {}".format(len(assembly_id_list)))
  random.shuffle(assembly_id_list)
  current_size = size
  output_assembly_id_list = []
  output_matched_ncbi_taxid_list = []
  input_list = assembly_id_list[:current_size]
  remaining_list = assembly_id_list[current_size:]
  while len(output_assembly_id_list) != len(assembly_id_list):
    if len(output_assembly_id_list) < 100:
      print("Linking IDs in chunks of {}".format(current_size))
      if (len(assembly_id_list) != 0) and (len(assembly_id_list) > current_size):
        print("input_list is {} ".format(input_list))
        with open("list.txt", "w") as output:
          output.write('\n'.join((input_list)))
        command = "epost -input list.txt -db assembly | elink -target taxonomy | efetch -format uid > temp"
        out, err = _run_command(command)
        count = 0
        with open('temp', 'r') as f:
          lines = [line.rstrip() for line in f]
          count = len(lines)
        if count == current_size:
          print("All IDs in this set are matched")
          output_assembly_id_list = output_assembly_id_list + input_list
          output_matched_ncbi_taxid_list = output_matched_ncbi_taxid_list + lines
          assert len(output_assembly_id_list) == len(output_matched_ncbi_taxid_list)
          print("Total number of IDs matched: {}".format(len(output_assembly_id_list)))
          current_size = size
          input_list = remaining_list[:current_size]
          remaining_list = remaining_list[current_size:]
          continue
        else:
          print("Tried to link {} IDs, but found {}".format(current_size,count))
          current_size = int(math.floor(current_size/2))
          temp_input_list = input_list[:current_size]
          remaining_list = input_list[current_size:] + remaining_list
          input_list = temp_input_list
          print("Retrying with {} IDs".format(current_size))
    else:
      print("output_assembly_id_list is {}".format(output_assembly_id_list))
      print("output_matched_ncbi_taxid_list is {}".format(output_matched_ncbi_taxid_list))





