"""
This Python file contains the code for creation and traversing Binary Search Tree(BST).
This file is imported by the bst_Visualizer.py to access the node creation and search algorithms for the
visualisation purpose.
"""


# This class is used to create a node for a tree
class Node:
    def __init__(self, data, parent=None, pos=None):
        self.data = data
        self.left = None
        self.right = None
        self.parent = parent
        # The self.pos holds the value left or right denotes its position respective to its parent.
        self.pos = pos
        self.length = 0
        # The x and y are the coordinate values which are used in the visualization process
        # I assigned modified values so that the nodes don't overlap on each other while visualising
        if self.parent is None:
            self.x = 50
            self.y = 50
        else:
            self.x = self.parent.x*0.8
            self.y = self.parent.y*0.8


# The search_data variable is a dictionary that stores the search element as key and the path as value
# Which are used when the search is used in visualizer.
# Path is used to store the path for a particular search temporarily which is then stored in search_data.
search_data = {}
path = []


# This function is used to insert new data into the BST
def insert(root, data, parent=None, pos=None):
    if root is None:
        return Node(data, parent, pos)
    else:
        if root.data == data:
            return root
        elif root.data < data:
            root.right = insert(root.right, data, root, "right")
        else:
            root.left = insert(root.left, data, root, "left")
    return root


""" 
This is used to search if a particular element is present in the BST or not by using the search_func().
This function first checks if the element is already searched previously,if so then the path is extracted 
from the search_data variable else the search_func function is called and the path is stored and then sent 
to the visualizer.
"""


def search(root, data):
    global path
    if data in search_data:
        return search_data[data]
    else:
        search_data[data] = search_func(root, data)
        path = []
        return search_data[data]


# Actual function that finds if the given element is present in the BST or not.
def search_func(root, data):
    if root:
        path.append(root)
        if root.data == data:
            return path
        elif root.data < data:
            return search(root.right, data)
        else:
            return search(root.left, data)


# This function is used to travel the BST level wise or BFS(Breadth First Search) manner.
def level_order_traversal(root):
    queue = [root]
    traversed_path = [root]
    while queue:
        z = queue.pop(0)
        if z.left is not None:
            queue.append(z.left)
            traversed_path.append(z.left)
        if z.right is not None:
            queue.append(z.right)
            traversed_path.append(z.right)
    return traversed_path
