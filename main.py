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

size = 3

int_to_partition_dictionary = all_set_partitions_dict(size)
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

delete = []
for i in range(dict_length):
    if transition_matrix[0, i] == np.array([0.]):
        delete.append(i)
delete.sort(reverse=True)
for j in delete:
    transition_matrix = np.delete(transition_matrix, j, axis = 0)
    transition_matrix = np.delete(transition_matrix, j, axis = 1)

print(transition_matrix)
print(int_to_partition_dictionary)