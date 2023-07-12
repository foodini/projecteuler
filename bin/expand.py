# A module to handle all the headache of reading and writing the current comamnd
# line.

# TODO: make the underlining a little more friendly for anyone who doesn't have
# a terminal that supports it.  It should work easily with the tools that
# already exist, but shouldn't depend upon them, in case someone wants to
# pick up this tool set, but not everything else.

import os
import sys
import re
import subprocess

def _get_token_offset(tokens, point):
  accum=0
  token_offset = 0
  for token in tokens:
    accum += len(token)
    if point <= accum:
      return token_offset
    token_offset += 1
    accum += 1
  return -1

def _strip_tuples(tuples):
  stripped = []
  for entry in tuples:
    if isinstance(entry, tuple):
      entry_name, unused = entry
      stripped.append(entry_name)
    else:
      stripped.append(entry)
  return stripped

def _format_option(option, prefix_len, option_number):
  if isinstance(option, tuple):
    option_name, option_description = option
    return ("%4s %s\033[4m%s\033[24m : %s" % (
        option_number, option_name[:prefix_len],
        option_name[prefix_len:], option_description))
  else:
    return ("%4s %s\033[4m%s\033[24m" % (
        option_number, option[:prefix_len], option[prefix_len:]))

# When you are editing a command line, the state of your terminal is a bit
# wonky: it's in raw mode.  Normally, when you hit enter, the terminal is
# switched to cooked mode, so under normal circumstances, your scripts are run
# with the tty cooked. When your prompt is generated and control is handed
# back to you, your terminal is set back to raw again and this tennis match
# continues forever.  The world is a very happy place when we are all blissfully
# unaware of this psychotic mess.
#
# Unfortunately, bind doesn't give target programs the same consideration.  When
# you hit [Alt-O] (or whatever you've used to activate your script), you stay
# in raw mode - the mode that the commandline editor lives in. If we don't
# manually switch you to cooked, you will not be able to enter any input.  While
# we're at it, we have to force the terminal to do echo for us.  If we don't
# revert these changes when we're done, our command line editor will be a mess
# when we get back.  (Try it.  It's about as useful as doing a headstand on a
# roller coaster.)
#
# http://linux.about.com/od/ttl_howto/a/hwtttl15t04_2.htm
# http://stackoverflow.com/questions/16928761/why-will-a-script-not-accept- \
#      input-on-stdin-when-invoked-from-bashs-bind
def _get_terminal_settings():
  proc = subprocess.Popen(['/bin/stty', '-g'], stdout=subprocess.PIPE)
  settings = proc.communicate()[0]
  os.system('stty cooked echo')
  return settings.decode()

def _set_terminal_settings(settings):
  os.system('stty %s' % settings)

# Given a list of strings, return the starting substring common to all of them.
def get_common_base(strings):
  strings = _strip_tuples(strings)

  if len(strings) == 0:
    return ''
  if len(strings) == 1:
    return strings[0]

  # Create one iter for each string.  We'll walk them
  iters = []
  for s in strings:
    iters.append(iter(s))

  common_base = ''
  try:
    while True:
      current_char = next(iters[0])
      for i in iters[1:]:
        if next(i) != current_char:
          return common_base
      common_base += current_char
  except:
    return common_base

def filter_for_matches(preamble, candidates):
  matches = []
  for candidate in candidates:
    if isinstance(candidate, tuple):
      candidate_name, unused = candidate
    else:
      candidate_name = candidate
    if candidate_name.find(preamble) == 0:
      matches.append(candidate)
  return matches

#Given a set of options and the user's "choice" - whatever they entered at the
#prompt - reduce the options list to just what matches the new information.
def _get_filtered_options(options, common_base, choice):
  required_common_base = common_base + choice
  required_common_base_len = len(required_common_base)
  filtered_options = []
  strings_only = []
  for option in options:
    if isinstance(option, tuple):
      option_name, option_description = option
      if option_name[0:required_common_base_len] == required_common_base:
        strings_only.append(option_name)
        filtered_options.append(option)
    else:
      if option[0:required_common_base_len] == required_common_base:
        strings_only.append(option)
        filtered_options.append(option)
  new_common_base = get_common_base(strings_only)
  return (filtered_options, new_common_base)

# There's no way for a child process to affect the environment of a parent
# process, so to change READLINE_LINE or READLINE_POINT (the env variables that
# we have to change to affect the command line,) I write a file that the parent
# (bash) process can source to make these changes.  The sourcing of that file is
# built into the bind command.
#
# I open this file early so that it is guaranteed to be empty if processing
# terminates before generating any updates.  Otherwise, I'll end up sourcing an
# old version of the temp file.

#TODO: write some tests?

class Expand():
  def __init__(self, tmp_file_name):
    self.tmp_file_handle = open(tmp_file_name, "w")

    self.command_tokens = os.environ['READLINE_LINE'].split(' ')
    self.command_point = int(os.environ['READLINE_POINT'])
    self.token_offset = _get_token_offset(self.command_tokens,
        self.command_point)
    self.token_to_expand = self.command_tokens[self.token_offset]
    self.selected_option = -1

    delimiter_location = self.token_to_expand.find('\x16')
    if delimiter_location > -1:
      selected_option = self.token_to_expand[delimiter_location+1:]
      if len(selected_option):
        self.selected_option = int(selected_option)
        self.token_to_expand = self.token_to_expand[:delimiter_location]
        self.command_tokens[self.token_offset] = self.token_to_expand

  def __del__(self):
    self.tmp_file_handle.close()

  def append_output(self, line):
    self.tmp_file_handle.write(line)

  # Get the thing at the user's cursor:
  def get_token(self, index=None):
    if index != None:
      return self.command_tokens[index]
    else:
      return self.token_to_expand

  #TODO: Rename this to get_token_index. (Needs to change in clients, as well.)
  def get_token_offset(self, index=None):
    return self.token_offset

  def get_selected_option(self, options, common_base):
    if self.selected_option > -1:
      return self.selected_option

    self._print_prompt_line()
    option_number = 0;
    for option in options:
      print(_format_option(option, len(common_base), option_number))
      option_number += 1

    sys.stdout.write("> ")
    sys.stdout.flush()

    # https://groups.google.com/forum/?fromgroups#!searchin/gnu.bash.bug/bind/
    #     gnu.bash.bug/0WsXBN1Amb4/zxbwQb7H-e0J
    #More helpful? http://linux.about.com/od/ttl_howto/a/hwtttl15t04_2.htm
    settings = _get_terminal_settings()
    try:
      choice = sys.stdin.readline()
    except KeyboardInterrupt:
      choice = ''
    finally:
      _set_terminal_settings(settings)

    match = re.search('(\d+)', choice)
    choice = choice[0:-1]   #Strip the end of line from the choice.
    if len(choice) == 0:
      return common_base
    if not match:
      filtered_options, new_common_base = _get_filtered_options(
          options, common_base, choice[0])
      if len(filtered_options) == 0:
        return common_base
      elif len(filtered_options) == 1:
        #When the user has unambiguosly specified an option, the completion
        #should include a trailing space, to match behavior with bash complete.
        return new_common_base + " "
      else:
        return self.get_selected_option(filtered_options, new_common_base)

    selected_option = options[int(match.group(0))]
    if isinstance(selected_option, tuple):
      selected_option, _ = selected_option

    #When the user has unambiguosly specified an option, the completion
    #should include a trailing space, to match behavior with bash complete.
    return selected_option + " "

  def update_command_line(self, expanded_token):
    self.command_tokens[self.token_offset] = expanded_token
    readline_line_command = (
        'export READLINE_LINE=\'' + ' '.join(self.command_tokens) + '\'')
    self.append_output(readline_line_command + '\n')
    new_point = len(' '.join(self.command_tokens[:self.token_offset+1]))
    self.append_output('export READLINE_POINT=%s\n' % new_point)

  def display(self, expanded_token):
    if self.command_tokens[self.token_offset] != expanded_token:
      self.command_tokens[self.token_offset] = expanded_token
      readline_line_command = (
          'export READLINE_LINE=\'' + ' '.join(self.command_tokens) + '\'')
      self.append_output(readline_line_command + '\n')
    new_point = len(' '.join(self.command_tokens[:self.token_offset+1]))
    self.append_output('export READLINE_POINT=%s\n' % new_point)

  def _get_prompt(self):
    prompt = os.environ['PS1']

    prompt = re.sub(r'\x1b[^m]*m', '', prompt)
    prompt = re.sub(r'\\033[^m]*m', '', prompt)
    prompt = re.sub(r'\\[[\]]', '', prompt)
    prompt = re.sub(r'\\n', '\n', prompt)

    #remove characters only used by bash:
    #prompt = re.sub(r'\[.*;', '', prompt)

    return prompt + ' '.join(self.command_tokens)

  def _print_prompt_line(self):
    print(self._get_prompt())

  def _append_prompt_line(self):
    self.append_output('echo -e "%s"\n' % self._get_prompt())
