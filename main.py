from transition_matrix import *

size = 3
power = 3
transition_matrix = make_transition_matrix(size)

powered = poly_matrix_power(transition_matrix, power)
print(powered)

gen_poly = poly_dot(powered[0, :], np.ones(len(powered[0, :])))
print(gen_poly)

print(poly.polyval(1, poly.polyder(poly.polymulx(gen_poly))) / (8 ** power) + size + power - 1)