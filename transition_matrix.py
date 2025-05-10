from evolve_partition import *
import numpy as np
import numpy.polynomial.polynomial as poly

def all_set_partitions_dict(n):
    def helper(seq):
        if not seq:
            return [[]]
        first = seq[0]
        rest_partitions = helper(seq[1:])
        result = []
        for partition in rest_partitions:
            # Insert 'first' into each existing subset
            for i in range(len(partition)):
                new_partition = partition[:i] + [partition[i] + [first]] + partition[i+1:]
                result.append(new_partition)
            # Or put 'first' in a new subset
            result.append([[first]] + partition)
        return result

    elements = list(range(1, n + 1))
    partitions = helper(elements)

    # Store in a dictionary with integer keys
    partition_dict = {i: partitions[i] for i in range(len(partitions))}
    return partition_dict

def num_to_binary_list(num, length):
    l = []
    while num != 0:
        l.append(num % 2)
        num = num // 2
    while len(l) < length:
        l.append(0)
    return l

def find_index(partition, dictionary):
    def normalize(arr):
        return sorted([sorted(inner) for inner in arr])
    partition = normalize(partition)
    for i, p in dictionary.items():
        if normalize(p) == partition:
            return i
    return None

def make_transition_matrix(size):
    int_to_partition_dictionary = all_set_partitions_dict(size)

    def check_valid_partition(partition):
        for s in partition:
            if not 1 in s:
                parity = s[0] % 2
                for i in range(1, len(s)):
                    if s[i] % 2 != parity:
                        return False

        return True

    illegal = [len(int_to_partition_dictionary) - 1]
    for key, partition in int_to_partition_dictionary.items():
        if not check_valid_partition(partition):
            illegal.append(key)
    for key in illegal:
        del int_to_partition_dictionary[key]

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
            transition_matrix[i, index] = poly.polyadd(transition_matrix[i, index], new_poly)

            '''
            print(int_to_partition_dictionary[i])
            print(rule)
            print(new_partition)
            print(new_poly)
            print(index)
            '''
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
