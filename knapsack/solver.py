#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
import time

Item = namedtuple("Item", ['index', 'value', 'weight'])


def old_solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')
    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))

    # a trivial greedy algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    value = 0
    weight = 0
    taken = [0]*len(items)

    for item in items:
        if weight + item.weight <= capacity:
            taken[item.index] = 1
            value += item.value
            weight += item.weight
    
    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(1) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data


def solve_it_diff_methods(input_data, solver):
    # Modify this code to run your optimization algorithm
    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))

    #ipdb.set_trace()
    # this is where we are going to call our code
    if solver is "DynamicProgramming":
        start_time = time.time()
        result = dp.solve_it(items, capacity)
        print "Execution with DP took {} seconds".format(time.time()-start_time)

    elif solver is "BranchBound":
        start_time = time.time()
        result = BB.solve_it_depth_first(items, capacity)
        print "Execution with BB DFS took {} seconds".format(time.time()-start_time)

    elif solver is "BranchBound_relaxed":
        start_time = time.time()
        result = BB_relaxed.solve_it_depth_first(items, capacity, 'weight')
        print "Execution with BB DFS with relaxation took {} seconds".format(time.time()-start_time)

    return result

def solve_it(input_data):
    # Modify this code to run your optimization algorithm
    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))

    # this is where we are going to call our code
    start_time = time.time()
    result = BB_relaxed.solve_it_depth_first(items, capacity, 'automatic')
    print "Execution with BB DFS with relaxation took {} seconds".format(time.time()-start_time)
    return result


import sys
import ipdb
import dynamic_programming as dp
import branch_and_bound as BB
import branch_and_bound_v3 as BB_relaxed

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        input_data_file = open(file_location, 'r')
        input_data = ''.join(input_data_file.readlines())
        input_data_file.close()
        #ipdb.set_trace()
        #print old_solve_it(input_data)
        #print solve_it_diff_methods(input_data, "DynamicProgramming")
        #print solve_it_diff_methods(input_data, "BranchBound")
        print solve_it_diff_methods(input_data, "BranchBound_relaxed")

    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)'

