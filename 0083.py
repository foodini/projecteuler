#!/usr/bin/env python3

matrix = []
solutions = []
huge = 9999 * 80 * 80
with open('0083_matrix.txt') as fd:
  for line in fd.readlines():
    row = [int(x.strip()) for x in line.split(',')]
    matrix.append(row)
    solutions.append([huge] * 80)

solutions[79][79] = matrix[79][79]

def pathlen(i, j, di, dj):
  return matrix[i][j] + solutions[i+di][j+dj]

while True:
  dirty = False
  for i in range(80):
    for j in range(80):
      if i > 0:
        candidate_len = pathlen(i, j, -1, 0)
        if candidate_len < solutions[i][j]:
          solutions[i][j] = candidate_len
          dirty = True
      if i < 79:
        candidate_len = pathlen(i, j, 1, 0)
        if candidate_len < solutions[i][j]:
          solutions[i][j] = candidate_len
          dirty = True
      if j > 0:
        candidate_len = pathlen(i, j, 0, -1)
        if candidate_len < solutions[i][j]:
          solutions[i][j] = candidate_len
          dirty = True
      if j < 79:
        candidate_len = pathlen(i, j, 0, 1)
        if candidate_len < solutions[i][j]:
          solutions[i][j] = candidate_len
          dirty = True
  if not dirty:
    break
print(solutions[0][0])
