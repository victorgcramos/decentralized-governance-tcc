from random import sample, choice
from math import floor, trunc
import numpy as np
import matplotlib.pyplot as plt
import datetime


histogram = lambda M: np.histogram(np.squeeze(np.asarray(M)))
now = datetime.datetime.now()

def init(x, percentage_occupied):
  # possible values for occupied places
  v = [1, 2]
  matrix_size = pow(x, 2)
  occupied = floor(matrix_size * percentage_occupied);
  # random matrix definition
  array = [choice(v) if i <= occupied else 0 for i in range(matrix_size)]
  np.random.shuffle(array)
  matrix = np.reshape(array, (x, x))
  return(matrix);

def nbhd_analysis(elem, matrix, lin, col, nbhd_side, threshold = 0.5):
  '''
    Gets left and right interval based on nbhd_side.
    for example: if nbhd_side is 3 (which means a 3x3 neighborhood),
    the current neighborhood should be: 
    
    [(i-1, j-1), (i-1, j) ,(i-1, j+1)] 
    [( i,  j-1), ( i,  j) ,( i,  j+1)] 
    [(i+1, j-1), (i+1, j) ,(i+1, j+1)]
    
    However, if "i" or "j" are edges, the neighborhood is reduced.
  '''
  left = floor(nbhd_side/2)
  right = round(nbhd_side/2)
  left_disp = lambda x: x-left if x-left >= 0 else x
  right_disp = lambda x: x+right if x+right <= len(matrix) else x + 1
  next_lin = lin - left_disp(lin)
  next_col = col - left_disp(col)
  nbhd = matrix[
    left_disp(lin) : right_disp(lin),
    left_disp(col) : right_disp(col)
  ]
  counter = [0 for i in range(3)]
  for i in range(len(nbhd)):
    for j in range(len(nbhd[0])):
      curr = nbhd[i][j]
      # import ipdb; ipdb.set_trace()
      if curr == 0:
        next_lin = lin - left_disp(lin) + i
        next_col = col - left_disp(col) + j
      counter[curr] += 1
  counter[elem] -= 1
  total = len(nbhd)*len(nbhd[0]) - 1 - counter[0]
  similar = counter[elem]
  similarity = similar/total if total > 0 else 1
  # if similarity is less than similarity threshold, the current element changes its spot
  # with the nearest empty
  is_satisfied = similarity >= threshold
  if not(is_satisfied):
    aux = matrix[next_lin][next_col]
    matrix[next_lin][next_col] = matrix[lin][col]
    matrix[lin][col] = aux
  return matrix


if __name__ == '__main__':
  n = int(input("Please insert the N for a NxN matrix: "))
  percentage_occupied = float(input("Pergentage occupied (0 to 1): "))
  n_of_iterations = int(input("Number of iterations: "))
  nbhd_size = int(input("Neighborhood size (N for NxN): "))
  population = init(n, percentage_occupied)
  
  # plot chart data
  plt.matshow(population)
  plt.colorbar()
  plt.savefig("images/temp/%s-before.png"% now.isoformat())
  
  # iterates over matrix 
  iteration = 0
  while iteration < n_of_iterations:
    for i in range(n):
      for j in range(n):
        elem = population[i][j]
        # elements of type 0 are considered free spaces, so they don't change spots
        if elem != 0:
          population = nbhd_analysis(elem, population, i, j, nbhd_size)
    iteration += 1
  # plot chart data
  plt.matshow(population)
  plt.colorbar()
  plt.savefig("images/temp/%s-after.png"% now.isoformat())