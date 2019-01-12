#!/usr/bin/env python3
# coding: utf-8

#https://misc.flogisoft.com/bash/tip_colors_and_formatting

import argparse
from datetime import datetime
import os
import sys

# gen_prompt_text [T|F] $? GREEN,BOLD BLUE,UNDER origin/master 

esc_format = '\\[\\033[{}m\\]'
esc_format = '\[\033[{}m\]'
esc_format = '\033[{}m'
esc_format = '\\033[{}m'
#esc_format = '[{}]'
#esc_format = 'ESC[{}m'

codes = {
    'BLACK':       30,
    'RED':         31,
    'GREEN':       32,
    'BROWN':       33,
    'BLUE':        34,
    'PURPLE':      35,
    'CYAN':        36,
    'WHITE':       37,
    'UNDER':       4,
    'NO_UNDER':    24,
    'BOLD':        1,
    'NO_BOLD':     21,
    'DARK':        2,
    'NO_DARK':     22
}

in_color = sys.argv[1] == 'T'
previous_retval = sys.argv[2]
no_error_format = sys.argv[3]
error_format = sys.argv[4]
context_info = sys.argv[5:]

stack = [
    {'color': codes['WHITE'], 'bold': codes['NO_BOLD'],
    'dark': codes['NO_DARK'], 'under': codes['NO_UNDER']}
]

prompt_col = ''
prompt_bnw = ''
def concat(str, color_only=False):
    global prompt_col
    global prompt_bnw
    prompt_col += str
    if not color_only:
        prompt_bnw += str

def top_of_stack_to_result():
    #The order the're written seems to matter. Bold won't work
    #unless at the end.
    e = stack[-1]
    sequence = '{};{};{};{}'.format(
            e['color'], e['dark'], e['under'], e['bold'])
    concat(esc_format.format(sequence), True)

def push_state(**kwargs):
    entry = stack[-1].copy()
    entry.update(kwargs)
    stack.append(entry)
    top_of_stack_to_result()

def push_state_from_string(str):
    args = {}
    for fmt in str.split(','):
        if 'BOLD' in fmt:
            args['bold'] = codes[fmt]
        elif 'UNDER' in fmt:
            args['under'] = codes[fmt]
        elif 'DARK' in fmt:
            args['dark'] = codes[fmt]
        elif fmt in codes:
            args['color'] = codes[fmt]
    push_state(**args)

def pop_state():
    stack.pop()
    top_of_stack_to_result()

#I don't like underlined spaces, so this is an easy way to write
#one without the underline.
def space():
    push_state(under=24)
    concat(' ')
    pop_state()

def context():
    space()
    if context_info:
        concat('(')
        formats = context_info[::2]
        strings = context_info[1::2]
        for i, (fmt, str) in enumerate(zip(formats, strings)):
            push_state_from_string(fmt)
            concat(str)
            if i != len(formats) - 1:
                space()
            pop_state()
        concat(')')
        space()

clock = datetime.now().strftime('%H:%M')
pwd = os.environ['PWD']
if len(pwd) > 37:
    pwd = '...' + pwd[-37:]

concat('╓', True)

if previous_retval == '0':
    push_state_from_string(no_error_format)
else:
    push_state_from_string(error_format)

concat(clock, True)
context()
concat(pwd)
pop_state()
concat('\\n╙', True)
top_of_stack_to_result()

if in_color:
    esc_format.format(0)

filename = (os.environ['HOME'] + '/tmp/prompt_' +
        str(os.getppid()) + '.sh')
with open(filename, 'w') as fd:
    fd.write('export PROMPT_COL="' + prompt_col + '"' + '\n')
    fd.write('export PROMPT_BNW="' + prompt_bnw + '"' + '\n')
