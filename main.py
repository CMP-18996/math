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

def num_to_binary_list(num):
    l = []
    while num != 0:
        l.append(num % 2)
        num = num // 2
    return l

int_to_partition_dictionary = all_set_partitions_dict(4)
dict_length = len(int_to_partition_dictionary)

transition_matrix = np.zeros((dict_length, dict_length))

print(dict_length)
print(int_to_partition_dictionary)

print(evolve_partition([[1,2],[3]],[1,0,0]))
print(new_component([[1,2],[3]],[1,0,0]))
print(transition_matrix)