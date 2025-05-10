from transition_matrix import *

size = 4
power = 2
transition_matrix = make_transition_matrix(size)

powered = poly_matrix_power(transition_matrix, power)
print(powered)

gen_poly = poly_dot(powered[0, :], np.ones(len(powered[0, :])))
print(gen_poly)

print(poly.polyval(1, poly.polyder(poly.polymulx(gen_poly))) / ((2 ** size) ** power) + size + power - 1)