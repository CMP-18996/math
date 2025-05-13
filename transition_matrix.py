from evolve_partition import *
import numpy as np
import numpy.polynomial.polynomial as poly

def num_to_binary_list(num, length):
    l = []
    while num != 0:
        l.append(num % 2)
        num = num // 2
    while len(l) < length:
        l.append(0)
    return l

def set_partition_generator(p, size, counter):
    for i in range(counter, len(p)):
        for num in range(2 ** size):
            rule = num_to_binary_list(num, size)
            new = sorted([sorted(p) for p in evolve_partition(p[i], rule)], key=lambda subset: subset[0])
            if not new in p:
                newp = p
                newp.append(new)
                set_partition_generator(newp, size, i)
    return {j: p[j] for j in range(len(p))}

def find_index(partition, dictionary):
    def normalize(arr):
        return sorted([sorted(inner) for inner in arr])
    partition = normalize(partition)
    for i, p in dictionary.items():
        if normalize(p) == partition:
            return i
    return None

def make_transition_matrix(size):
    int_to_partition_dictionary = set_partition_generator([[list(range(1, size + 1))]], size, 0)

    int_to_partition_dictionary = dict(enumerate(int_to_partition_dictionary.values()))
    print(int_to_partition_dictionary)
    dict_length = len(int_to_partition_dictionary)

    transition_matrix = np.empty((dict_length, dict_length), dtype=poly.Polynomial)
    for i in range(dict_length):
        for j in range(dict_length):
            transition_matrix[i, j] = np.zeros(1)

    for i in range(dict_length):
        for j in range(2 ** size):
            rule = num_to_binary_list(j, size)
            new_partition = evolve_partition(int_to_partition_dictionary[i], rule)
            new_poly = poly.polypow([0, 1], new_component(int_to_partition_dictionary[i], rule))
            index = find_index(new_partition, int_to_partition_dictionary)
            '''
            print(int_to_partition_dictionary[i])
            print(rule)
            print(new_partition)
            print(new_poly)
            print(index)
            '''
            transition_matrix[i, index] = poly.polyadd(transition_matrix[i, index], new_poly)
    return transition_matrix

def poly_dot(vector1, vector2):
    sum = poly.polyzero
    for i in range(len(vector1)):
        sum = poly.polyadd(sum, poly.polymul(vector1[i], vector2[i]))
    return sum

def poly_matrix_power(matrix, pow):
    M = matrix
    dim = matrix.shape[0]

    def sq_multiply(m1, m2):
        M = np.zeros((dim, dim), dtype=poly.Polynomial)
        for i in range(dim):
            for j in range(dim):
                M[i, j] = poly_dot(m1[i, :], m2[:, j])
        return M

    for i in range(pow - 1):
        M = sq_multiply(M, matrix)

    return M
