# imports required for the project
import turtle
import bst
from time import sleep

# Creating the turtle screen
screen = turtle.Screen()
screen.title("BST-Graphics")

# Creating turtles
pen = turtle.Turtle()
pen1 = turtle.Turtle()
search_node_pen = turtle.Turtle()
search_edge_pen = turtle.Turtle()
button_pen = turtle.Turtle()
button_text_pen = turtle.Turtle()

# Initializing the buttons and the output text related variables
start_Button_x = -270
start_Button_y = -300
reset_Button_x = 150
reset_Button_y = -300
search_Button_x = -60
search_Button_y = -300
result_x = -200
result_y = -250

ButtonLength = 100
ButtonWidth = 50

root = None
# root node coordinates
root_org_x = 0
root_org_y = 200
edge_length = 150


# Function to read the input data from the user for the BST
def read_input():
    global root
    try:
        data = screen.textinput('Read Data', 'Enter the data with comma separation: ').split(',')
        if data:
            root = bst.Node(int(data[0]))
            for i in data[1:]:
                bst.insert(root, int(i))
        return 1
    except AttributeError:
        message = "Please Enter Data to Create BST"
        pen.goto(result_x, result_y)
        pen.write(message, font=('Arial', 25, 'bold'))
        # To fade away the message after 3 seconds
        sleep(3)
        pen.undo()
        return 0


# This function is used to set the pen attribute values to their default values
def set_pen_props():
    # pen props
    pen.color('black')
    pen.fillcolor('white')
    pen.hideturtle()
    pen.pensize(3)
    pen.speed(9)
    # pen1 props
    pen1.color('black')
    pen1.fillcolor('blue')
    pen1.pensize(3)
    pen1.speed(9)
    pen1.hideturtle()
    # search_node_pen props
    search_node_pen.pensize(3)
    search_node_pen.fillcolor('purple')
    search_node_pen.color('purple')
    search_node_pen.speed(9)
    search_node_pen.hideturtle()
    # search_edge_pen props
    search_edge_pen.color('red')
    search_edge_pen.pensize(3)
    search_edge_pen.speed(9)
    search_edge_pen.hideturtle()
    # Button_pen props
    button_pen.color('black')
    button_pen.fillcolor('white')
    button_pen.hideturtle()
    button_pen.pensize(3)
    button_pen.speed(9)
    # Button_text_pen props
    button_text_pen.color('black')
    button_text_pen.fillcolor('blue')
    button_text_pen.hideturtle()
    button_text_pen.pensize(3)
    button_text_pen.speed(9)


# This function Draws the buttons based on the given coordinates and name
def draw_button(x, y, name='Start'):
    button_pen.penup()
    button_pen.begin_fill()
    button_pen.goto(x, y)
    button_pen.pendown()
    button_pen.goto(x + ButtonLength, y)
    button_pen.goto(x + ButtonLength, y + ButtonWidth)
    button_pen.goto(x, y + ButtonWidth)
    button_pen.goto(x, y)
    button_pen.end_fill()
    button_pen.penup()
    button_text_pen.penup()
    button_text_pen.goto(x + 15, y + 15)
    button_text_pen.write(name, font=('Arial', 15, 'normal'))


# This function is used to clear what all the pens have drawn till now
def clear_pen_drawings():
    pen.clear()
    pen1.clear()
    clear_search_pen_drawings()


# This function is used to clear what search_pens have drawn till now
def clear_search_pen_drawings():
    search_edge_pen.clear()
    search_node_pen.clear()


# This handles the button clicks in the window
def button_click(x, y):
    global edge_length, root
    length = edge_length
    set_pen_props()
    # search_node_pen.clear()
    # search_edge_pen.clear()
    # This block is executed when Start button is clicked
    if start_Button_x <= x <= start_Button_x + ButtonLength:
        if start_Button_y <= y <= start_Button_y + ButtonWidth:
            if read_input():
                clear_pen_drawings()
                user_input = bst.level_order_traversal(root)
                for i in range(len(user_input)):
                    draw_bst(user_input[i], length)
                    if i > 0 and i % 2 == 0:
                        length *= 0.8
            else:
                return
    # This block is executed when Reset button is clicked
    elif reset_Button_x <= x <= reset_Button_x + ButtonLength:
        if reset_Button_y <= y <= reset_Button_y + ButtonWidth:
            screen.reset()
            root = None
            start()
    # This block is executed when Search button is clicked
    elif search_Button_x <= x <= search_Button_x + ButtonLength:
        if search_Button_y <= y <= search_Button_y + ButtonWidth:
            if root is None:
                pen.penup()
                pen.goto(result_x, result_y)
                pen.write("Sorry There is no BST to search data", font=('Arial', 25, 'bold'))
                # To fade away the message after 3 seconds
                sleep(3)
                pen.undo()
                pen.pendown()
                return
            clear_search_pen_drawings()
            key = turtle.textinput("Input", "Search Value:")
            message = " Found in the BST"
            input_data = bst.search(root, int(key))
            if input_data is None:
                message = str(key) + " Not" + message
            else:
                message = str(key) + message
                input_data = input_data[-3:]
                len_of_data = len(input_data)
                for i in range(len_of_data):
                    search_node_pen.color('red')
                    search_node_pen.fillcolor('purple')
                    if i == len_of_data - 1:
                        search_node_pen.color('red')
                        search_node_pen.fillcolor('green')
                    draw_search_path(input_data[i], input_data[i].length)
            search_node_pen.color('black')
            search_node_pen.penup()
            search_node_pen.goto(result_x, result_y)
            search_node_pen.write(message, font=('Arial', 25, 'bold'))


# This functions Draws the search path obtained for the given element
def draw_search_path(node, length):
    if node.parent is None:
        draw_node(root_org_x, root_org_y, node.data, search_node_pen)
        node.x = root_org_x
        node.y = root_org_y
    else:
        draw_edge(node, search_edge_pen, length)
        pos = search_edge_pen.pos()
        draw_node(pos[0], pos[1], node.data, search_node_pen)


# This function is used to draw the nodes of the BST
def draw_node(x, y, data, pen_to_use):
    pen_to_use.penup()
    pen_to_use.begin_fill()
    pen_to_use.goto(x, y)
    pen_to_use.pendown()
    c = 0
    if x == root_org_x and y == root_org_y:
        c = 1
        pen_to_use.circle(30)
    else:
        pen_to_use.circle(-30)
    pen_to_use.end_fill()
    pen_to_use.penup()
    pen_to_use.goto(x, y)
    if c:
        pen_to_use.goto(x - 5, y + 15)
    else:
        pen_to_use.goto(x - 7, y - 45)
    pen_to_use.color('white')
    pen_to_use.write(data, font=('Arial', 20, 'normal'))
    pen_to_use.color('black')
    pen_to_use.fillcolor('blue')


# This function is used to draw the Edges between nodes of the BST
def draw_edge(node, pen_to_use, length):
    pen_to_use.penup()
    if node.parent is None:
        pen_to_use.goto(root_org_x, root_org_y)
    else:
        pen_to_use.goto(node.parent.x, node.parent.y)
        if node.pos == 'left':
            pen_to_use.setheading(-150)
        elif node.pos == 'right':
            pen_to_use.setheading(-30)
        pen_to_use.pendown()
        pen_to_use.forward(length)
        node.length = length


# This is used to draw the BST based on given data
def draw_bst(node, length):
    if node.parent is None:
        draw_node(root_org_x, root_org_y, node.data, pen1)
        node.x = root_org_x
        node.y = root_org_y
    else:
        draw_edge(node, pen, length)
        pos = pen.pos()
        draw_node(pos[0], pos[1], node.data, pen1)
        node.x = pos[0]
        node.y = pos[1] - 60


# This function is the main function that is executed first or when reset button is clicked
def start():
    set_pen_props()
    draw_button(start_Button_x, start_Button_y)
    draw_button(reset_Button_x, reset_Button_y, "Reset")
    draw_button(search_Button_x, search_Button_y, "Search")
    screen.onclick(button_click)


# The code for calling drawing_functions for buttons and visualizer
start()
turtle.done()
