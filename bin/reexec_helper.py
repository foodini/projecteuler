#!/usr/bin/env python3

import glob
import os
import sys

#Get rid of the call to this script:
arg = sys.argv.pop(0)

files = []
command = []
while sys.argv:
  arg = sys.argv.pop(0)
  if arg == '--':
    command = sys.argv
    break
  else:
    files.append(arg)

if not command:
  command = files
  files = [files[0]]

if not command:
  sys.stdout.write("No command found to reexec")
  exit(1)

all_files = []
for file in files:
  expanded = glob.glob(file)
  all_files.extend(expanded)

newest_file = max(all_files, key=os.path.getmtime)
newest_file_mod_time = os.path.getmtime(newest_file)

print(int(newest_file_mod_time))
for arg in command:
  print(arg)

