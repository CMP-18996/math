from collections import defaultdict

#given a set partition, find the index of the set which contains num
def find_set_index(set, num):
    for i, sets in enumerate(set):
        if num in sets:
            return i
    return -1

#credit: https://stackoverflow.com/questions/71966710/python3-join-lists-that-have-same-value-in-list-of-lists
def merge_common(lists):
    neigh = defaultdict(set)
    visited = set()
    for each in lists:
        for item in each:
            neigh[item].update(each)
    def comp(node, neigh = neigh, visited = visited, vis = visited.add):
        nodes = set([node])
        next_node = nodes.pop
        while nodes:
            node = next_node()
            vis(node)
            nodes |= neigh[node] - visited
            yield node
    for node in neigh:
        if node not in visited:
            yield sorted(comp(node))

#main function, takes in one partition and a row and spits out the next
def evolve_partition(partition, rule):
    #will put each num into a set corresponding to a set in the partition
    echo = []
    for i in range(0, len(partition)):
        echo.append([])
    #1 automatically stays with 1
    for i in range(0, len(echo)):
        if 1 in partition[i]:
            echo[i].append(1)

    #actual work
    for i, num in enumerate(rule):
        if num == 1 and i < len(rule) - 1:
            index = find_set_index(partition, i + 2)
            echo[index].append(i + 1)
        elif num == 1 and i == len(rule) - 1:
            index = find_set_index(partition, 1)
            echo[index].append(i + 1)
        elif num == 0 and i < len(rule) - 1:
            index = find_set_index(partition, i + 1)
            echo[index].append(i + 2)
        elif num == 0 and i == len(rule) - 1:
            index = find_set_index(partition, i + 1)
            echo[index].append(1)
        #print(echo)
    #remove duplicates
    echo = merge_common(echo)

    result = []
    for s in echo:
        result.append(list(set(s)))

    #numbers not in echo must be new individual sets
    for i in range(1, len(rule) + 1):
        included = False
        for s in result:
            if i in s:
                included = True
        if not included:
            result.append([i])

    return result

def new_component(partition, rule):
    count = 0
    for s in partition:
        if len(s) == 1 and s[0] != 1 and rule[s[0] - 1] == 1 and rule[s[0] - 2] == 0:
            count += 1
    return count

#print(evolve_partition([[1,2],[3]],[1,1,0]))