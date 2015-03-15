__author__ = 'shreyas'

import numpy as np
import ipdb
'''
class Item:
    def __init__(self, value, weight):

        self.weight = weight
        self.value = value


    def display(self):
        print "The value fo the item is {0}".format(self.value)
'''


def fill_table(table, item, item_index):

    # col_index is same as the item index
    knapsack_capacity = table.shape[0]-1  # Since we have 1 extra row for 0 capacity

    index_item_add = int(np.ceil(item.weight))  # place where item could be added to Knapsack

    if item.weight <= knapsack_capacity:     # We will consider this item only if its weight is less than the capacity else just copy the previous row
        if item_index == 0:
            # We have no ref. from behind
            table[index_item_add:, item_index] = item.value
        else:
                # We can copy the entries from before as till this point we can not add this item
                table[:index_item_add, item_index] = table[:index_item_add, item_index-1]

                # Now we have to fill the dynamic table sequentially
                for index in np.arange(index_item_add, knapsack_capacity+1):

                    # We don't add the item so we use the previous value
                    value_1 = table[index, item_index-1]

                    # We do add item, s
                    remaining_capacity = index - item.weight
                    if remaining_capacity < 0:
                        value_2 = item.value
                    else:
                        value_2 = item.value + table[remaining_capacity, item_index-1]

                    # Assigning the max value
                    table[index, item_index] = max(value_1, value_2)
    else:
        table[:, item_index] = table[:, item_index-1]


def get_soltuion_from_table(table,all_items,item_selector):
    rows = table.shape[0]-1
    cols = table.shape[1]

    item_index = np.arange(1, cols)  # We don't go to case of 0 items
    item_index = item_index[::-1]  # We will traverse the items from back

    # Initialization
    row_index = rows

    for temp_item_index in item_index:

        temp_item = all_items[temp_item_index-1]

        current_value = table[row_index, temp_item_index]
        previous_value = table[row_index, temp_item_index-1]

        if previous_value<current_value:
            # this means we used the current variable
            item_selector[temp_item_index-1] = 1

            # Error check
            assert int(temp_item_index-1) == temp_item.index

            # Updating the row index for next iteration
            row_index = row_index-temp_item.weight


def solve_it(all_items, knapsack_capacity):
    # NOTE: Here all_items is a namedtuple
    debug = True
    number_items = len(all_items)

    # We have to initialize the table
    # We want an extra row for 0 capacity and extra column for zero item
    table_DP = np.zeros((knapsack_capacity+1,number_items+1), dtype=np.dtype('i4'))
    table_DP[:,0]=0  # We know when we have no item, all the values are zero
    item_index=1
    for temp_item in all_items:
        fill_table(table_DP, temp_item, item_index)
        item_index = item_index+1

    # Computing the assingment score
    item_selector = np.zeros(number_items, dtype=int)
    get_soltuion_from_table(table_DP, all_items,item_selector)
    value = table_DP[-1,-1]
    solution = item_selector

    if debug is True:
        #ipdb.set_trace()
        zipped_data = zip(solution, all_items)
        calculated_value = sum((temp_item.value for temp_select,temp_item in zipped_data if temp_select == 1))
        calculated_weight = sum((temp_item.weight for temp_select, temp_item in zipped_data if temp_select == 1))
        debug_string = "Debugging: \n"
        debug_string += "-------------\n"
        debug_string += "Value recomputed from selection indices: {} \n".format(calculated_value)
        debug_string += "Weight of selection indices: {} \n".format(calculated_weight)
        debug_string += "Knapsack capacity given: {}\n".format(knapsack_capacity)
        debug_string += "-------------\n"
        print debug_string


    # Printing the result in a string
    output_data = str(value) + ' ' + str(1) + '\n'
    output_data += ' '.join(map(str, solution))
    return output_data



if __name__ == '__main__':
    from collections import namedtuple


    # better than defining a class in this case
    Item = namedtuple("Item", ['index', 'value', 'weight'])

    # Initialization
    #all_items = [Item(0,16,2), Item(1,19,3), Item(2,23,4), Item(3,28,5)]
    #knapsack_capacity = 7

    # Example from slide 8 for Branch and Bound
    all_items = [Item(0, 45, 5), Item(1, 48, 8), Item(2, 35, 3)]
    knapsack_capacity = 10
    ipdb.set_trace()
    # Calling our solver
    print(solve_it(all_items, knapsack_capacity))





