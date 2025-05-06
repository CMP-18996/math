from evolve_partition import *

def all_set_partitions(n):
    def helper(seq):
        if not seq:
            return [[]]
        first = seq[0]
        rest_partitions = helper(seq[1:])
        result = []
        for partition in rest_partitions:
            for i in range(len(partition)):
                new_partition = partition[:i] + [partition[i] + [first]] + partition[i+1:]
                result.append(new_partition)
            result.append([[first]] + partition)
        return result

    elements = list(range(1, n+1))
    return helper(elements)

# int -> partition
def partitions_dict(n):
    return {n: all_set_partitions(n)}

def num_to_binary_list(num):
    l = []
    while num != 0:
        l.append(num % 2)
        num = num // 2
    return l

int_to_partition_dictionary = partitions_dict(4)

print(evolve_partition([[1,2],[3]],[1,0,0]))
print(new_component([[1,2],[3]],[1,0,0]))
print(int_to_partition_dictionary)