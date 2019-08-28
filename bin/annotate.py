#!/usr/bin/env python3

#TODO:
# if no args, process stdin
# if getting from stdin, -- shouldn't be required
# You can't print red for both stdout and stderr

from collections import defaultdict

import os
import selectors
import subprocess
import sys
import time

command_name = sys.argv.pop(0) # the command name

def usage():
    print(command_name, ' [-e x.y] [-c x.y] [-s sleep_time] --')
    print('\t-e change elapsed-time formatting to printf-style floats. (%8.2f => "-s 8.2")')
    print('\t-c change current-time formatting to printf-style floats. (%8.2f => "-s 8.2")')
    print('\t-s resolution of the timer & update rate (a positive float.)')
    exit(0)

time_per_line = False
found_end_of_args = False
timer_resolution = 0.1
elapsed_now_format = '{:6.2f}'
current_now_format = '{:6.2f}'
if '--' in sys.argv:
    while sys.argv and not found_end_of_args:
        arg = sys.argv.pop(0)
        if arg == '--':
            found_end_of_args = True
        else:
            if arg == '-e':
                elapsed_now_format = '{:' + sys.argv.pop(0) + 'f}'
            elif arg == '-c':
                current_now_format = '{:' + sys.argv.pop(0) + 'f}'
            elif arg == '-s':
                timer_resolution = float(sys.argv.pop(0))
            else:
                usage()

buffers = defaultdict(lambda: '')
first_line_printed = defaultdict(lambda: False)

print('sys.argv: ' + str(sys.argv))
proc = subprocess.Popen(sys.argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1)

outfiles = {proc.stdout: sys.stdout, proc.stderr: sys.stderr}

sel = selectors.DefaultSelector()
sel.register(proc.stdout, selectors.EVENT_READ)
sel.register(proc.stderr, selectors.EVENT_READ)

start_time = time.time()
last_line_end_time = start_time
next_update_time = start_time

done = False
while not done:
  active_buffs = 0
  active_fds = sel.select(timeout=0)
  now = time.time()
  now_formatted = (
      elapsed_now_format.format(now-start_time) + ' ' +
      current_now_format.format(now-last_line_end_time))
  if active_fds:
    for key, _ in active_fds:
      data = key.fileobj.read1(1).decode()
      if data != '':
        active_buffs += 1
        buffers[key.fileobj] += data
      if data == '\n':
        last_line_end_time = now
        if key.fileobj == proc.stderr:
            now_formatted = '\033[31m' + now_formatted + '\033[0m'
        print('\r', now_formatted, buffers[key.fileobj], end="", file=outfiles[key.fileobj])
        buffers[key.fileobj] = ''
  else:
    if now > next_update_time:
      next_update_time = now + timer_resolution
      print ('\r', now_formatted, end='', file=sys.stdout, flush=True)
      print ('\r', now_formatted, end='', file=sys.stderr, flush=True)
      time.sleep(timer_resolution/4.0)

  done = proc.poll() is not None and active_buffs == 0 and active_fds
