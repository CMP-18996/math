from transition_matrix import *

size = 7
power = 3
transition_matrix = make_transition_matrix(size)

print(transition_matrix)
powered = poly_matrix_power(transition_matrix, power)
print(powered)

gen_poly = poly_dot(powered[0, :], np.ones(len(powered[0, :])))
print(gen_poly)

print(poly.polyval(1, poly.polyder(poly.polymulx(gen_poly))) / ((2 ** size) ** power) + size + power - 1)