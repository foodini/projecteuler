#!/usr/bin/env python3

from math import gcd
import time

'''
TODO: Took 12 minutes to run on my MacBook Pro.

(See image.)
Instead of mirror bounces, lets lay out space as a grid. Each mirror becomes
one line on the grid. (For the sake of easy graphing, I've sheared space so
we get a grid of right triangles, but it helped me think through the
problem.)

Each black dot represents where a 'C' vertex is reflected. I've labeled a
number of these black dots with numbers. These are the number of lines you
have to cross to get from the bottom left (where the beam enters the grid)
to the dot in question.

Some of the black dots have squares around them. These are unreachable dots,
as a line from the 0,0 point to those dots passes through a nearer point.

The number of lines you have to pass through to reach a dot is computable
using the numbers along the side and bottom of the grid. Let's say we're
trying to get the number of lines crossed to get to (6,3). The total is the
sum of:
    5 vertical lines (or, x-1)
    2 horizontal lines (or, y-1)
    8 diagonal lines, which you can find by following the previous diagonal
      down/right to its ID, which is 8.

This gives us a total of 15. The equation for this is:
    ((x-1) + (y-1)) * 2 + 1

It turns out that all of the diagonals have the same sum. This means that we
need to find where 12017639147's diagonal is and traverse along it, skipping
any 'C' points where the beam would have hit a previous exit. This turns out to
be fairly easy. For any (x,y), if gcd(x,y) isn't 1, there would have been a
previous vertex. For example, you can see a square at (15,6).  The gcd of 15
and 6 is 3. The gcd of 3 tells us that there was a previous hit at (x/3,y/3) or
(5,2), which you can see shows a hit with a reflection count of 11.

What about (6,3)? Had the laser been aimed in that direction, it would have
intersected the grid at points (2,1) and (4,2). The gcd of 6 and 3 is not 1,
which tells us we had a previous point to exit the map and we reject this point.

For an example of a clean exit, let's look at (14,5). You can see that there
are a couple of close passes (like at 11,4), but there are no intersections
with grid points. 14 and 5 have a gcd of 1.

So all we have to do is figure out what (x,y) to start at for the
12017639147 diagonal. Easy enough. x = (12017639147 + 3)/2, y=0 is our start
point. We just have to figure out where the first 'C' along that diagonal is.

Our first point is off the y=0 line by 3-(x%3), so we start at:
    (x-offset, offset) or .... yeah. Look at the code.

From there we just decrease x by 3 and increase y by 3 as long as y<x, and do
our gcd test. (We stop where y>x, instead of continuing until y<0 because the
space is symetric about the x=y line. When we terminate, we multiply the count
by 2 to account for this.)

I was hoping that projecteuler had chosen this particular line because it
had very few repeats.... maybe something related to the number of prime
factors of the starting number. Had that been the case, I could simply have
counted up the number of 'C' points on that line and subtracted the number of
prime factors and been done. I suspect there's something I'm missing.
'''

x = (12017639147 + 3)//2
#x = (1000001 + 3)//2
#x = (37 + 3)//2
y = 0

count = 0
repeats = 0
offset = 3-(x%3)
x -= offset
y = offset
next_output_time = 0
while(y < x):
  now = time.time()
  if now > next_output_time:
    next_output_time = now + 1
    print(count, repeats, y/x)
  common = gcd(x, y)
  if common == 1:
    #print('hit0: (%d,%d), common: %d' % (x, y, common))
    count += 1
  else:
    #print('miss: (%d,%d), common: %d' % (x, y, common))
    repeats += 1
  x -= 3
  y += 3

#print(count, repeats, count+repeats)
print(count * 2)
