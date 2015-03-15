__author__ = 'shreyas'
# In this code we are going to implement branch and bound method
# We are going to use a deque for implementing the DFS traversal
import ipdb
from collections import deque
import copy


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


def generate_child(node, item, side):

    if side is "left":
        # Left node is formed by selecting the item
        child_node = Node(evaluation=node.evaluation + item.value, capacity=node.capacity - item.weight, optimum_value=node.optimum_value, height=node.height + 1)
        child_node.selected_item = copy.deepcopy(node.selected_item)
        child_node.selected_item[node.height] = 1

    elif side is "right":
        # Right node is formed by not selecting the item
        child_node= Node(evaluation=node.evaluation, capacity=node.capacity, optimum_value=node.optimum_value - item.value, height=node.height + 1)
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
                    child = generate_child(current_node, temp_item, "left")

                    if child.evaluation > max_value_obatined[0]:
                        max_value_obatined = (child.evaluation, child.selected_item)

                    # Appending the child node to stack
                    tree.append(child)
                    # Error check (We shouldn't have explored the right side by mistake first)
                    assert current_node.right_child is None

            elif current_node.right_child is None:
                # We do not append the current node back, as it is explored on both ends
                child = generate_child(current_node, temp_item, "right")

                if child.evaluation > max_value_obatined[0]:
                    max_value_obatined = (child.evaluation, child.selected_item)

                # Appending the child node to stack
                tree.append(child)

    return max_value_obatined


def solve_it_depth_first(all_items, knapsack_capacity):
    # NOTE: Here all_items is a namedtuple
    # Root node corresponds to no selected variable

    # Initialization
    debug = True
    max_possible_value = sum([temp_item.value for temp_item in all_items])
    root_node = Node(evaluation=0, capacity=knapsack_capacity, optimum_value=max_possible_value, height=0)
    root_node.selected_item = [0]*len(all_items)
    tree_nodes = deque([root_node])

    # Performing depth first search
    solution = perform_DFS(tree_nodes, all_items)

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




if __name__ == '__main__':
    from collections import namedtuple

    # better than defining a class in this case
    Item = namedtuple("Item", ['index', 'value', 'weight'])

    # Initialization
    # Example from slide 8 for Dynamic programming
    #all_items = [Item(0, 16, 2), Item(1, 19, 3), Item(2, 23, 4), Item(3, 28, 5)]
    #knapsack_capacity = 7

    # Example from slide 8 for Branch and Bound
    all_items = [Item(0, 45, 5), Item(1, 48, 8), Item(2, 35, 3)]
    knapsack_capacity = 10
    #ipdb.set_trace()

    # Calling our solver
    print solve_it_depth_first(all_items, knapsack_capacity)








'''
        if flag is not True:
            if current_node.child_left is None:
                # Means the left node was not yet explored
                # Create the left child, by selecting the item
                if current_node.capacity >= temp_item.weight:
                    left_expanded = Node(evaluation=current_node.evaluation + temp_item.value, capacity=knapsack_capacity - temp_item.weight, optimum_value=current_node.optimum_value, height=current_node.height + 1)
                    left_expanded.selected_item = current_node.selected_item
                    left_expanded.selected_item[current_node.height] = 1
                    tree.appendleft(left_expanded)

                    # Updating max-value we have achieved so far
                    if max_value_obatined < left_expanded.evaluation:
                        max_value_obatined = (left_expanded.evaluation, left_expanded.selected_item)
            else:
                # Means we have to explore the right side of the tree
                # Create the right child by not selecting the item
                if current_node.capacity >= temp_item.weight:
                    right_expanded = Node(evaluation=current_node.evaluation, capacity=knapsack_capacity, optimum_value=current_node.optimum_value - temp_item.value, height=current_node.height + 1)
                    right_expanded.selected_item = current_node.selected_item
                    right_expanded.selected_item[current_node.height] = 0
                    tree.appendleft(right_expanded)

                    # Updating max-value we have achieved so far
                    if max_value_obatined < right_expanded.evaluation:
                        max_value_obatined = (right_expanded.evaluation, right_expanded.selected_item)



   '''

