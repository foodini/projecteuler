#!/usr/bin/env python3

# I feel no remorse, whatsoever, for doing this. I wrote a sudoku solver
# in Java many, many years ago and I have no intention of ever doing it again.
from sudoku import Sudoku #https://pypi.org/project/py-sudoku/

grids = []
with open('0096_sudoku.txt') as fd:
  for line_id, line in enumerate(fd.readlines()):
    if line_id%10 == 0:
      grids.append([])
      continue
    grids[-1].append([int(c) for c in [*line.strip()]])

total = 0

for g in grids:
  problem = Sudoku(3, 3, g)
  solution = problem.solve()
  #solution.show()
  #print(solution.board)
  total += (solution.board[0][0] * 100 + solution.board[0][1] * 10 + solution.board[0][2])

print(total)
