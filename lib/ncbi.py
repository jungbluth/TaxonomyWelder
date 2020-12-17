#!/usr/bin/env python3

import random
import subprocess
import math
import pandas as pd


def _run_command(command):
  """
  _run_command: run command and print result
  """
  #print('Start executing command:\n{}'.format(command))
  pipe = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
  output, stderr = pipe.communicate()
  exitCode = pipe.returncode
  if (exitCode == 0):
    pass
    #print('Executed command:\n{}\n'.format(command) +
    #  'Exit Code: {}\n'.format(exitCode))
  else:
    error_msg = 'Error running command:\n{}\n'.format(command)
    error_msg += 'Exit Code: {}\nOutput:\n{}\nStderr:\n{}'.format(exitCode, output, stderr)
    raise ValueError(error_msg)
    sys.exit(1)
  return (output, stderr)


def fetch_taxonomy_name_from_assembly_id_single(assembly_id_list):
  # shuffle list because otherwise identical entires collapsed, want to minimize
  print("Fetching NCBI TaxIDs from GTDB-used NCBI Assembly IDs")
  print("Number of IDs to link: {}".format(len(assembly_id_list)))
  output_assembly_id_list = []
  output_matched_ncbi_taxid_list = []
  input_list = assembly_id_list[:1]
  remaining_list = assembly_id_list[1:]
  while len(output_assembly_id_list) != len(assembly_id_list):
    if (len(input_list) != 0):
      print("Currently linking ID: {} ".format(input_list))
      with open("list.txt", "w") as output:
        output.write('\n'.join((input_list)))
      command = "epost -input list.txt -db assembly | elink -target taxonomy | efetch -format uid > temp"
      out, err = _run_command(command)
      count = 0
      with open('temp', 'r') as f:
        lines = [line.rstrip() for line in f]
        count = len(lines)
      output_assembly_id_list = output_assembly_id_list + input_list
      output_matched_ncbi_taxid_list = output_matched_ncbi_taxid_list + lines
      assert len(output_assembly_id_list) == len(output_matched_ncbi_taxid_list)
      percent_done = round((len(output_assembly_id_list) / len(assembly_id_list)) * 100)
      print("\nTotal number of IDs matched: {} (out of {}) ({} percent done)".format(len(output_assembly_id_list),len(assembly_id_list),percent_done))
      input_list = remaining_list[:1]
      remaining_list = remaining_list[1:]
      if isinstance(round(len(output_assembly_id_list) / 10), int):
        with open('output_incremental.txt', 'a') as f:
          for i in range(len(output_assembly_id_list)):
            f.write("{} {}\n".format(output_assembly_id_list[i], output_matched_ncbi_taxid_list[i]))
      continue
  with open('output_all.txt', 'a') as f:
    for i in range(len(output_assembly_id_list)):
      f.write("{} {}\n".format(output_assembly_id_list[i], output_matched_ncbi_taxid_list[i]))




def fetch_taxonomy_name_from_assembly_id_batch(assembly_id_list, size):
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
    if current_size > len(input_list):
      current_size = len(input_list)
    print("\nTrying with IDs in chunks of {}".format(current_size))
    if (len(input_list) != 0) and (len(assembly_id_list) > current_size):
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
        percent_done = round((len(output_assembly_id_list) / len(assembly_id_list)) * 100)
        print("\nTotal number of IDs matched: {} (out of {}) ({} percent done)".format(len(output_assembly_id_list),len(assembly_id_list),percent_done))
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
  with open('output.txt', 'w') as f:
    for i in range(len(output_assembly_id_list)):
      f.write("{} {}\n".format(output_assembly_id_list[i], output_matched_ncbi_taxid_list[i]))




