# In this code we are going to implement branch and bound method
# We are going to use a deque for implementing the DFS traversal
from __future__ import division
import ipdb
from collections import deque
import copy
import numpy as np
import matplotlib.pyplot as plt
__author__ = 'shreyas'
class Node:
    def __init__(self, evaluation, capacity, optimum_value, height):
        self.evaluation = evaluation
        self.capacity = capacity
        self.optimum_value = optimum_value
        self.height = height
        self.selected_item = None    # This is a list containing the selected items
        self.left_child = None       # variables to help the traversal
        self.right_child = None

    def __str__(self):
        output = "Stats for the node are as follows:"
        output += "\n -------------------------------"
        output += "\n Left child:{}".format(self.left_child)
        output += "\n Right child:{}".format(self.right_child)
        output += "\n Height:{}".format(self.height)
        output += "\n -------------------------------"
        output += "\n Details for the optimization"
        output += "\n Evaluation: {}".format(self.evaluation)
        output += "\n Remaining capacity is: {}".format(self.capacity)
        output += "\n Optimum value: {}".format(self.optimum_value)
        output += "\n Selected items: {}".format(self.selected_item)
        return output


def generate_child(node, item, side, list_items):

    if side is "left":
        # Left node is formed by selecting the item
        # In this case the optimum value remains the same
        child_node = Node(evaluation=node.evaluation + item.value, capacity=node.capacity - item.weight, optimum_value=node.optimum_value, height=node.height + 1)
        child_node.selected_item = copy.deepcopy(node.selected_item)
        child_node.selected_item[node.height] = 1

    elif side is "right":
        # Right node is formed by not selecting the item
        # In this case we have to recompute the optimum value by considering:
        # Items avaiable on this node

        #ipdb.set_trace()
        # Since this element was not selected while branching right
        items_could_be_selected = list_items[node.height+1:]

        optimum_value = compute_optimistic_value(items_could_be_selected, node.capacity)
        # Also we have to include the value of items we already selected in the tree before
        optimum_value += node.evaluation

        child_node= Node(evaluation=node.evaluation, capacity=node.capacity, optimum_value=optimum_value, height=node.height + 1)
        child_node.selected_item = copy.deepcopy(node.selected_item)
        child_node.selected_item[node.height] = 0

    return child_node


def perform_DFS(tree, items):
    number_items = len(items)
    depth = copy.deepcopy(number_items)
    max_value_obatined = (0, None) # We will store (max_value, selected_items)
    #ipdb.set_trace()

    while tree:                         # Checks if deque is empty or not
        current_node = tree.pop()

        flag = current_node.height >= depth or current_node.capacity <= 0 or current_node.optimum_value < max_value_obatined[0]
        # We will prune if:
        # 1) We have covered all items
        # 2) Capacity is full
        # 3) Optimum value is less than the max_value_obtained
        # 4) Item which can be added right now is heavier than the knapsack

        if flag is not True:
            # Item which we can add or not add at this level
            temp_item = items[current_node.height]    # IMP: Indexing of items starts at 0, and for height it starts at 1

            if current_node.left_child is None:
                # We will have to pop this later to explore the right child
                current_node.left_child = "Explored"
                tree.append(current_node)

                # Check if we can add this item
                if temp_item.weight <= current_node.capacity:
                    child = generate_child(current_node, temp_item, "left", items)

                    if child.evaluation > max_value_obatined[0]:
                        max_value_obatined = (child.evaluation, child.selected_item)

                    # Appending the child node to stack
                    tree.append(child)
                    # Error check (We shouldn't have explored the right side by mistake first)
                    assert current_node.right_child is None

            elif current_node.right_child is None:
                # We do not append the current node back, as it is explored on both ends
                child = generate_child(current_node, temp_item, "right", items)

                if child.evaluation > max_value_obatined[0]:
                    max_value_obatined = (child.evaluation, child.selected_item)

                # Appending the child node to stack
                tree.append(child)

    return max_value_obatined



def compute_entropy_field(sequence, field):


    if field is 'value_per_weight':
        data = [r.value/r.weight for r in sequence]
    elif field:
        data = [getattr(r, field) for r in sequence]

    n_bins = np.floor(np.sqrt(len(sequence)))
    hist, bins = np.histogram(data, n_bins, density=True)
    debug = False

    if debug is True:
        width = 0.7 * (bins[1] - bins[0])
        center = (bins[:-1] + bins[1:]) / 2
        plt.bar(center, hist, align='center', width=width)
        plt.show()

    # Converting into probability vector
    hist = hist / sum(hist)
    entropy_values = -sum([np.log(r)*r for r in hist if r > 0])
    return entropy_values

def compute_field_to_sort(item_list):
    # We choose a attribute which minimizes the entropy of the PDF, which means
    # the attribute values are far from uniform or being similar
    field = ['value', 'weight', 'value_per_weight']
    def temp_func(x):
        return compute_entropy_field(item_list, x)

    temp_eval = map(temp_func, field)
    index = np.array(temp_eval).argmin()
    return field[index]



def solve_it_depth_first(all_items, knapsack_capacity, sort_with='automatic'):
    # NOTE: Here all_items is a namedtuple
    # Root node corresponds to no selected variable
    # Initialization
    # We will auto-select the field with which we should sort the input
    # We are going to compute the entropy of the probability distribution generated by the three cases
    if sort_with is 'automatic':
        print "Computing the field we will sort the input with. \n"
        print "Warning: This might not always be the optimal value \n"
        sort_with = compute_field_to_sort(all_items)


    print "Sorting with {}".format(sort_with)
    if sort_with is 'weight':
        sort_indices = sorted(range(len(all_items)), key=lambda x: all_items[x].weight, reverse=True)
    elif sort_with is 'value':
        sort_indices = sorted(range(len(all_items)), key=lambda x: all_items[x].value, reverse=True)
    elif sort_with is 'value_per_weight':
        sort_indices = sorted(range(len(all_items)), key=lambda x: all_items[x].value/all_items[x].weight, reverse=True)
    else:
        sort_indices = range(len(all_items))

    reverse_sort_indices = sorted(range(len(all_items)), key=lambda x: sort_indices[x])
    all_items_sorted = [all_items[r] for r in sort_indices]


    debug = False
    max_possible_value = compute_optimistic_value(all_items_sorted, knapsack_capacity)
    root_node = Node(evaluation=0, capacity=knapsack_capacity, optimum_value=max_possible_value, height=0)
    root_node.selected_item = [0]*len(all_items_sorted)
    tree_nodes = deque([root_node])

    # Performing depth first search
    solution = perform_DFS(tree_nodes, all_items_sorted)
    temp_max, temp_selection_index = solution

    # Mapping the solution to original sort order
    solution = (temp_max, [temp_selection_index[r] for r in reverse_sort_indices])

    #ipdb.set_trace()
    # Checking if the solution returned is correct or not
    if debug is True:
        #ipdb.set_trace()
        zipped_data = zip(solution[1], all_items)
        calculated_value = sum((temp_item.value  for temp_select, temp_item in zipped_data if temp_select == 1))
        calculated_weight = sum((temp_item.weight  for temp_select, temp_item in zipped_data if temp_select == 1))
        debug_string = "Debugging: \n"
        debug_string += "-------------\n"
        debug_string += "Value recomputed from selection indices: {} \n".format(calculated_value)
        debug_string += "Weight of selection indices: {} \n".format(calculated_weight)
        debug_string += "Knapsack capacity given: {}\n".format(knapsack_capacity)
        debug_string += "-------------\n"
        print debug_string
    # Printing the result in a string
    output_data = str(solution[0]) + ' ' + str(1) + '\n'
    output_data += ' '.join(map(str, solution[1]))
    return output_data


def compute_optimistic_value(item_list, capacity):
    # This function computes the optimistic value for the knapsack
    #ipdb.set_trace()
    value_and_weight = ((temp_item.value, temp_item.weight) for temp_item in item_list)
    sorted_sol = sorted(value_and_weight, key=lambda x: x[0]/x[1], reverse=True)

    # Finding how many things we can pack
    temp_capacity = 0
    optimistic_estimate = 0
    flag = False
    for index, (value, weight) in enumerate(sorted_sol):
        temp = temp_capacity + weight
        if temp > capacity:
            flag = True
            break
            # Fault occurs at index
        else:
            optimistic_estimate += value
            temp_capacity += weight

    # This part should only occur if we have violate the capacity
    # (otherwise, this used to occur also when all items can fit)
    if flag is True:
        remain_capacity = capacity - temp_capacity
        optimistic_estimate += remain_capacity*sorted_sol[index][0]/sorted_sol[index][1]

    return optimistic_estimate



if __name__ == '__main__':
    from collections import namedtuple

    # better than defining a class in this case
    Item = namedtuple("Item", ['index', 'value', 'weight'])

    # Initialization
    # Example from slide 8 for Dynamic programming
    #all_items = [Item(0, 16, 2), Item(1, 19, 3), Item(2, 23, 4), Item(3, 28, 5)]
    #knapsack_capacity = 7

    # Example from slide 8 for Branch and Bound
    items = [Item(0, 45, 5), Item(1, 48, 8), Item(2, 35, 3)]
    capacity = 10
    sort_with_var = 'value_per_weight'

    # Calling our solver
    print solve_it_depth_first(items, capacity, sort_with_var)







