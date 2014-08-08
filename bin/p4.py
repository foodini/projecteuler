import os
import re
from subprocess import Popen, PIPE

def p4_base_cmd(action):
  if os.getcwd().find('/google/src/cloud') == 0:
    base_cmd = ['g4']
    base_cmd.append(action)
  else:
    p4_host = os.environ['FITHOST']
    base_cmd = [os.environ['P4_BINARY_LOCATION'],
		'-p', 'ssl:%s:1666'%p4_host,
		'-c', os.environ['P4CLIENT'],
		'-u', 'ronb']
    if action == 'pending':
      base_cmd.extend(['changes', '-s', 'pending'])
    else:
      base_cmd.append(action)
  return base_cmd

# Convert the depot specs (//depot/..) to file specs (/google/src/...)
def _depot_specs_to_file_specs(depot_specs):
  if depot_specs == []:
    return []

  p4_where_cmd = p4_base_cmd('where')

  # p4_where_cmd += depot_specs
  p4_where_cmd.extend(depot_specs)
  process = Popen(p4_where_cmd, stdout=PIPE)
  file_specs = []
  for line in process.stdout.readlines():
    line = line.strip()
    #'p4 where' responses are in 3 columns; depotspec client-relative filespec
    file_specs.append(line.split(' ')[2])

  return file_specs

# Get a list of all the open depot specs.  This will include deleted files,
# which I like, so I don't filter them.  It would be easy enough to reject
# lines that have ' - delete' in them
def opened():
  p4_query = p4_base_cmd('opened')

  opened_depot_specs = []
  opened_depot_spec_descriptions = []
  re_get_depotspec = re.compile('^([^#]*)#\d* - \S*\s*(\S*)\s*(\S*)')
  process = Popen(p4_query, stdout=PIPE)
  for line in process.stdout.readlines():
    match = re.search(re_get_depotspec, line)
    if match:
      opened_depot_specs.append(match.group(1))
      if match.group(2) == 'default':
	opened_depot_spec_descriptions.append(match.group(2))
      else:
	opened_depot_spec_descriptions.append(match.group(3))

  return zip(_depot_specs_to_file_specs(opened_depot_specs),
	     opened_depot_spec_descriptions)

def pending():
  p4_query = p4_base_cmd('pending')

  pending_changelists = []
  re_get_change = re.compile('(\* )?Change (\d*)( :)? (.*)')
  process = Popen(p4_query, stdout=PIPE)
  for line in process.stdout.readlines():
    match = re.match(re_get_change, line)
    if match:
      pending_changelists.append((match.group(2), match.group(4)))

  return pending_changelists
