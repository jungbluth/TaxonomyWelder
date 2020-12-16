#!/usr/bin/env python3

import random
import subprocess
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
  #epost -input list.txt -db assembly | elink -target taxonomy | efetch
  # epost -input list.txt -db assembly | elink -target taxonomy | efetch -format uid
  # esearch -db assembly -query GCF_001305965.1 | elink -target taxonomy | efetch
  
  # shuffle list because otherwise identical entires collapsed, want to minimize
  print("Fetching NCBI TaxIDs from GTDB-used NCBI Assembly IDs")
  print("To number of IDs to link: {}".format(len(assembly_id_list)))
  random.shuffle(assembly_id_list)
  if (len(assembly_id_list) != 0) and (len(assembly_id_list) > size):
    input_list = assembly_id_list.pop(size)
    with open("list.txt", "w") as output:
      output.write('\n'.join((input_list)))
    command = "epost -input list.txt -db assembly | elink -target taxonomy | efetch -format uid > temp"
    out, err = _run_command(command)
