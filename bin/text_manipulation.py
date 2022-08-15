import os
import sys
import time

#Text color
#bold, underline, flash, etc.
#print_at, cursor_to
#get_screen_size
#print_to_status_line
#set_background_image?
#read_value_at? (If I can do this, I can underline stuff on-screen. a bit.)
#Basic drawing functions - boxes, histograms.

def get_terminal_width():
  return os.get_terminal_size().columns

def get_terminal_height():
  return os.get_terminal_size().lines

def print_at(x, y, s):
  if x < 0:
    x = get_terminal_width() + x
  if y < 0:
    y = get_terminal_height() + y
  sys.stdout.write('\x1b7\x1b[%d;%df%s\x1b8' % (y, x, s))

def flush():
  sys.stdout.flush()

def clear_screen():
  sys.stdout.write('\033[2J')
  sys.stdout.flush()

def clear():
  clear_screen()

def clear_box(x0, y0, width, height):
  blank_line = ' ' * width
  for y in range(y0, y0+height):
    print_at(x0, y, blank_line)

def print_centered(x, y, val, fmt='%s'):
  s = fmt % val
  print_at(x - len(s)/2, y, s)

def print_vertical(x, y0, val, fmt='%s'):
  s = fmt % val
  y = y0
  for c in s:
    print_at(x, y, c)
    y += 1

def print_centered_vertical(x, y0, val, fmt='%s'):
  y = y0 - len(s)/2
  print_vertical(x, y, val)

# Thanks to: https://azrael.digipen.edu/~mmead/www/mg/ansicolors/index.html
UNDERLINE_ON = '4'
UNDERLINE_OFF = '24'
BOLD_ON = '1'
BOLD_OFF = '21'
DARK_ON = '2'
DARK_OFF = '22'
INVERSE_ON = '7'
INVERSE_OFF = '27'
BLINK_ON = '5'
BLINK_OFF = '25'
CONCEALED_ON = '8'
CONCEALED_OFF = '28'
FG_RED = '31'
FG_GREEN = '32'
FG_ORANGE = '33'
FG_BLUE = '34'
FG_PURPLE = '35'
FG_CYAN = '36'
FG_GREY = '37'
FG_DARK_GREY = '90'
FG_LIGHT_RED = '91'
FG_LIGHT_GREEN = '92'
FG_YELLOW = '93'
FG_LIGHT_BLUE = '94'
FG_LIGHT_PURPLE = '95'
FG_TURQUOISE = '96'
BG_BLACK = '40'
BG_RED = '41'
BG_GREEN = '42'
BG_ORANGE = '43'
BG_BLUE = '44'
BG_PURPLE = '45'
BG_CYAN = '46'
BG_GREY = '47'
BG_DARK_GREY = '100'
BG_LIGHT_RED = '101'
BG_LIGHT_GREEN = '102'
BG_YELLOW = '103'
BG_LIGHT_BLUE = '104'
BG_LIGHT_PURPLE = '105'
BG_LIGHT_TURQUOISE = '106'

def beep():
  sys.stdout.write('\b', flush=True)

#Can be a list or just a single attribute
def set_text_attribute(attribs):
  if type(attribs) != list:
    attribs = [attribs]

  sys.stdout.write('\033[%sm' % ';'.join(attribs))

def draw_grid(x0, y0, width, height, x_divs, y_divs, clear=False):
  internal_width = (width - 1) // x_divs - 1;
  internal_height = (height - 1) // y_divs - 1;
  x_step = internal_width + 1
  y_step = internal_height + 1

  if clear:
    line = ' ' * width
    for y in range(y0, y0+height):
      print_at(x0, y, line)
  width_str = '═' * internal_width
  height_str = '║' * internal_height
  top_row = '╔' + (width_str + '╦') * (x_divs - 1) + width_str + '╗'
  bottom_row = '╚' + (width_str + '╩') * (x_divs - 1) + width_str + '╝'
  line_row = '╠' + (width_str + '╬') * (x_divs - 1) + width_str + '╣'
  left_col = '╔' + (height_str + '╠') * (y_divs - 1 ) + height_str + '╚'
  line_col = '╦' + (height_str + '╬') * (y_divs - 1 ) + height_str + '╩'
  right_col = '╗' + (height_str + '╣') * (y_divs - 1 ) + height_str + '╝'

  locations = []
  for x in range(x0+1, x0 + width - 1, x_step):
    col = []
    for y in range(y0+1, y0 + height - 1, y_step):
      col.append( (x,y) )
    locations.append(col)

  print_at(x0, y0, top_row)
  for steps in range(1, y_divs):
    print_at(x0, y0 + steps * y_step, line_row)
  print_at(x0, y0 + y_divs * y_step, bottom_row)

  print_vertical(x0, y0, left_col)
  for steps in range(1, x_divs):
    print_vertical(x0 + steps * x_step, y0, line_col)
  print_vertical(x0 + x_divs * x_step, y0, right_col)

  return locations, internal_width, internal_height

def print_header(x, y, width, header_string):
  if len(header_string) > width:
    pos = width - 1
    while pos >= 0 and header_string[pos] != ' ':
      pos -= 1
    header_string = header_string[:pos]
  print_at(x, y, header_string)

#TODO: draw over the entire box so you don't have to call clear_box (and you elimate flash.)
def timeseries(x0, y0, width, height, maxval, header_string, data, call=max):
  print_header(x0, y0, width, header_string)

  blocks = [' ','▁','▂','▃','▄','▅','▆','▇','█']

  chart_width = width
  #TODO: include bucket width under chart?
  chart_height = height - 1 # make room for header at top
  chart_bottom_y = y0 + chart_height
  chart_left_x = x0
  num_buckets = chart_width
  buckets = [0] * num_buckets

  for i, d in enumerate(data):
    bucket = int((num_buckets * i) / len(data))
    buckets[bucket] = call(buckets[bucket], d)

  if maxval is None:
    maxval = max(buckets)

  x = chart_left_x
  for b in buckets:
    if not maxval:
      scaled_height = 0
    else:
      scaled_height = int((8 * chart_height - 1) * b / maxval)
    y = chart_bottom_y
    while scaled_height > 7:
      print_at(x, y, blocks[8])
      y -= 1
      scaled_height -= 8
    print_at(x, y, blocks[scaled_height])
    y -= 1
    while y > y0:
      print_at(x, y, ' ')
      y -= 1
    x += 1

  flush()

#TODO: draw over the entire box so you don't have to call clear_box (and you elimate flash.)
def histogram(x0, y0, width, height, header_string, data):
  print_header(x0, y0, width, header_string)
  num_buckets = height - 1
  buckets = [0] * num_buckets

  if len(data) == 0:
    return

  mini = data[0]
  maxi = data[0]
  for d in data:
    if d < mini:
      mini = d
    if d > maxi:
      maxi = d

  # You don't want the max value falling into the n+1th bucket:
  maxi += (maxi - mini) * 0.001
  rnge = maxi - mini
  bucket_width = rnge / num_buckets
  if bucket_width == 0.0:
    bucket_width = 0.001

  max_bucket_count = 0

  for d in data:
    bucket = int((d - mini) / bucket_width)
    buckets[bucket] += 1
    if buckets[bucket] > max_bucket_count:
      max_bucket_count = buckets[bucket]

  bucket_wall_left = mini
  bucket_wall_right = mini + bucket_width
  for bid, bucket in enumerate(buckets):
    scaled_height = int(width * bucket / max_bucket_count)
    text = '%6.1f→%6.1f' % (bucket_wall_left, bucket_wall_right)
    count_text = '(%d)' % bucket
    text += ' ' * (width - len(text) - 1 - len(count_text))
    text += count_text

    set_text_attribute(BG_DARK_GREY)
    for cid, c in enumerate(text):
      if cid > scaled_height:
        set_text_attribute(BG_BLACK)
      print_at(x0 + cid, y0 + bid + 1, c)
    set_text_attribute(BG_BLACK)

    bucket_wall_left = bucket_wall_right
    bucket_wall_right += bucket_width

