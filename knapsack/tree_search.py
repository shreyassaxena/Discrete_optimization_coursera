__author__ = 'shreyas'
# In this code we are going to implement different search methods
import ipdb

class Node:
    def __init__(self, parent_node,height,index):

        #parent_node, child_left, child_right are pointers to the location in the list

        # Tree variables
        self.parent_node = parent_node
        self.child_left = None
        self.child_right = None
        self.height = height
        self.index = index

    def __str__(self):
        output = "Stats for the node are as follows:"
        output += "\n -------------------------------"
        #output += "\n Parent node: {}".format(self.parent_node)
        output += "\n Node index: {}".format(self.index)
        if isinstance(self.child_left, Node):
            output += "\n Left child:{}".format(self.child_left.index)
        else:
            output += "\n Right child:{}".format(self.child_left)
        if isinstance(self.child_right, Node):
            output += "\n Right child:{}".format(self.child_right.index)
        else:
            output += "\n Right child:{}".format(self.child_right)

        output += "\n Height:{}".format(self.height)
        return output

    def generate_tree(self, total_nodes, tree_depth):
        if self.height+1 >= tree_depth:
            self.child_left = None
            self.child_right = None
        else:
            self.child_left = Node(self.index, self.height+1, index=total_nodes[0]+1)
            self.child_right = Node(self.index, self.height+1, index=total_nodes[0]+2)
            total_nodes[0] += 2

            # Generating more nodes
            self.child_left.generate_tree(total_nodes, tree_depth)
            self.child_right.generate_tree(total_nodes, tree_depth)



def DFS(temp_tree,depth):
    print "We are going to traverse this tree in depth first search manner"



if __name__ == '__main__':

    # We will maintain a list of nodes created
    total_nodes = [1]
    tree_depth = 4

    Tree = Node(None, height=0, index=1)
    print root_node
    Tree.generate_tree(total_nodes,tree_depth)
    print "The tree is generated"
    ipdb.set_trace()

    # Now we want to visit the nodes in DFS
    DFS(Tree,tree_depth)




