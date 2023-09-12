#!/usr/bin/env python3

matrix = []
solutions = []
with open('0082_matrix.txt') as fd:
  for line in fd.readlines():
    row = [int(x.strip()) for x in line.split(',')]
    matrix.append(row)
    solutions.append([999999] * 80)

for i in range(80):
  solutions[i][79] = matrix[i][79]

for j in range(78, -1, -1):
  for i in range(0, 80):
    solutions[i][j] = solutions[i][j+1] + matrix[i][j]
  dirty = True
  while dirty:
    dirty = False
    for i in range(0, 80):
      if i > 0:
        pathlen = solutions[i-1][j] + matrix[i][j]
        if pathlen < solutions[i][j]:
          solutions[i][j] = pathlen
          dirty = True
      if i < 79:
        pathlen = solutions[i+1][j] + matrix[i][j]
        if pathlen < solutions[i][j]:
          solutions[i][j] = pathlen
          dirty = True

print(min([row[0] for row in solutions]))
