import base64
from copy import deepcopy
import os
import random
import shutil
from subprocess import Popen, PIPE
import sys
import termios
import time
import tty

#cursor_to
#print_to_status_line
#set_background_image?
#read_value_at? (If I can do this, I can underline stuff on-screen. a bit.)
#Given an image in a buffer, print to screen. (Currently requires b64 first.)

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

# txt can be filename (if not already_encoded) or the b64 encoded text of the image (see return val)
# pos - if None, prints inline. Otherwise pos is taken to be an x, y pair
# width is in screen characters, a percentage of screen width, or pixel count:
#  iterm2_print_image(txt, 100, 100, False, True)
#  iterm2_print_image(txt, '100%', '200px', True, False)
# RETURN VALUE: the base64 encoded version of the image, in case you want to cache it.
def iterm2_print_image(txt, pos, width, height, preserve_aspect_ratio, already_encoded):
  if not already_encoded:
    fd = open(txt, 'rb')
    data = fd.read()
    b64_bytes = base64.b64encode(data)
    # This isn't a base64 decode. Some idiot decided to have b64's encode return a byte string
    # instead of a character string, so you have to do this step to get a properly formatted b64:
    txt = b64_bytes.decode()

  if preserve_aspect_ratio:
    formatted = '\033]1337;File=inline=1;width=%s;height=%s:%s\a' % (width, height, txt)
  else:
    formatted = '\033]1337;File=inline=1;width=%s;height=%s;preserveAspectRatio=0:%s\a' % (
        width, height, txt)

  if pos is not None:
    print_at(pos[0], pos[1], formatted)
  else:
    sys.stdout.write(formatted)

  return txt

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
    flush()
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

def set_foreground_rgb(r, g, b):
  sys.stdout.write('\033[38;2;%s;%s;%sm' % (r, g, b))

def set_background_rgb(r, g, b):
  sys.stdout.write('\033[48;2;%s;%s;%sm' % (r, g, b))

old_settings=None

def init_getch_immediate():
  global old_settings
  old_settings = termios.tcgetattr(sys.stdin)
  new_settings = termios.tcgetattr(sys.stdin)
  new_settings[3] = new_settings[3] & ~(termios.ECHO | termios.ICANON) # lflags
  new_settings[6][termios.VMIN] = 0  # cc
  new_settings[6][termios.VTIME] = 0 # cc
  termios.tcsetattr(sys.stdin, termios.TCSADRAIN, new_settings)

def terminate_getch_immediate():
  global old_settings
  if old_settings:
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

def getch_immediate():
  if old_settings is None:
    init_getch_immediate()
  ch = os.read(sys.stdin.fileno(), 1).decode()

  return ch

# THERE'S A BUG in iterm that causes it to have trouble drawing these unicode characters
# just to the right of an image. If you've filled a column with an image, don't try
# to draw a grid line in the next column over.
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
  '''
  grid_width = 1 + x_step * x_divs
  grid_height = 1 + y_step * y_divs
  top_row = '█' * grid_width
  bottom_row = '█' * grid_width
  line_row = '█' * grid_width
  left_col = '█' * grid_height
  line_col = '█' * grid_height
  right_col = '█' * grid_height
  '''

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

def set_pixel(buffer, width, height, x, y, r, g, b):
  pixel_start_offset = y * width * 3 + x * 3
  buffer[pixel_start_offset] = r
  buffer[pixel_start_offset + 1] = g
  buffer[pixel_start_offset + 2] = b

def inc_pixel(buffer, width, height, x, y, r, g, b):
  try:
    pixel_start_offset = y * width * 3 + x * 3
    buffer[pixel_start_offset] = min(255, buffer[pixel_start_offset] + r)
    buffer[pixel_start_offset + 1] = min(255, buffer[pixel_start_offset] + g)
    buffer[pixel_start_offset + 2] = min(255, buffer[pixel_start_offset] + b)
  except:
    import ipdb; ipdb.set_trace()
    pass

cached_watermarks = dict()
figlet_location = None
no_figlet = False

def _cache_watermark(text, width, height, buffer):
  global cached_watermarks
  now = time.time()
  cached_watermarks[(text, width, height)] = {
      'buffer': deepcopy(buffer),
      'timestamp': now
  }

  #TODO: this should be based on total size
  if len(cached_watermarks) > 12:
    oldest_timestamp = now + 1
    for k, v in cached_watermarks.items():
      if v['timestamp'] < oldest_timestamp:
        oldest_timestamp = v['timestamp']
        oldest_key = k
    del(cached_watermarks[k])

def _watermark(width, height, text):
  global no_figlet
  global figlet_location
  global cached_watermarks

  if text in cached_watermarks:
    return deepcopy(cached_watermarks[(text, width, height)]['buffer'])

  if no_figlet or text is None:
    return bytearray(width * height * 3)

  if figlet_location is None:
    figlet_location = shutil.which('figlet')

  if figlet_location is None:
    no_figlet = True
    return bytearray(width * height * 3)

  stream = Popen([figlet_location, '-w', '99999', '-f', 'banner', text], stdout=PIPE)
  lines = stream.stdout.readlines()
  nonempty_lines = []
  for i, line in enumerate(lines):
    line = line.decode().rstrip()
    line = line[:width]
    if line:
      nonempty_lines.append(line)

  nonempty_lines = nonempty_lines[:height]

  buffer = bytearray(width * height * 3)
  for i, y in enumerate(range(height-len(nonempty_lines), height)):
    try:
      for x, c in enumerate(nonempty_lines[i]):
        if x < width:
          if c != ' ':
            set_pixel(buffer, width, height, x, y, 48, 48, 48)
    except:
      import ipdb; ipdb.set_trace()
      pass

  _cache_watermark(text, width, height, buffer)

  return buffer

def timeseries2(x0, y0, width, height, maxval, header_strings, buckets, colors, watermark=None):
  # Make room for the headers:
  chart_height = height - len(header_strings)
  chart_top_y = y0 + len(header_strings)
  chart_width = width

  for i, s in enumerate(header_strings):
    print_at(x0, y0 + i, ' ' * chart_width)
    print_at(x0, y0 + i, header_strings[i][:chart_width])

  legend_len = -1
  for k, c in colors.items():
    set_foreground_rgb(c[0], c[1], c[2])
    legend_len += (len(k) + 1) # the +1 is making room for a space between stats
    print_at(x0 + chart_width - legend_len, y0, k)

  bucket_pixel_width = 2
  pixels_per_character_height = 7
  image_width = bucket_pixel_width * len(buckets)
  image_height = chart_height * pixels_per_character_height

  pixels = _watermark(image_width, image_height, watermark)
  for i, bucket in enumerate(buckets):
    if 'no_data' in bucket:
      continue
    for stat_name, color in colors.items():
      datapoint = bucket[stat_name]
      if not maxval:
        scaled_height = 0
      else:
        scaled_height = int(
            pixels_per_character_height * chart_height * 0.999 * (1.0 - datapoint / maxval))

      start_x = image_width - bucket_pixel_width * (i + 1)
      for x in range(start_x, start_x + bucket_pixel_width):
        inc_pixel(pixels, image_width, image_height, x, scaled_height, color[0], color[1], color[2])

  header = bytearray('P6 %d %d 255\n' % (image_width, image_height), 'ascii')
  image = header + pixels
  b64_image = base64.b64encode(image)
  # Some idiot decided that a base64 encode would return a byte array. This isn't a b64 decode, it's
  # the translation from a bytearray to a string.
  b64_str = b64_image.decode()

  iterm2_print_image(b64_str, [x0, chart_top_y], chart_width, chart_height, False, True);

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

