#!/usr/bin/env python
import os
import re

from subprocess import Popen, PIPE

def opened():
  git_query = ['git', 'status']
  re_match_tracked = re.compile('^\t([^:]*):\s*(.*)')
  re_match_untracked = re.compile('^\t(.*)')
  process = Popen(git_query, stdout=PIPE)
  retval = []
  for line in process.stdout.readlines():
    match = re.search(re_match_tracked, line)
    if match:
      retval.append( (os.path.abspath(match.group(2)), match.group(1)) )
    else:
      match = re.search(re_match_untracked, line)
      if match:
        retval.append( (os.path.abspath(match.group(1)), 'untracked') )

  return retval

print opened()
