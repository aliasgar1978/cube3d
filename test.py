# ----------------------------------------------------------------------------- #
# Imports
# ----------------------------------------------------------------------------- #
from pprint import pprint
from cube3d import *

# ----------------------------------------------------------------------------- #
# static variables
# ----------------------------------------------------------------------------- #
front, back, top, bottom, left, right = ('front', 'back', 'top', 'bottom', 'left', 'right')

# ----------------------------------------------------------------------------- #
# Create a Cube
# ----------------------------------------------------------------------------- #
CB = get_cube("cube.xlsx")

# ----------------------------------------------------------------------------- #
# Rotate the square face/view to a direction
# view = defines the face which require to be rotated
# clockwise = direction looking from front of the view 
#             ( True=Clockwise direction, False=Anticlockwise direction ), 
#             default=clockwise (i.e: True)
# ----------------------------------------------------------------------------- #
# CB.rotate_square(view=front, clockwise=False)


# ----------------------------------------------------------------------------- #
# Change the Cube view to another direction
# view = defines the face to which we want to face.
# ----------------------------------------------------------------------------- #
# CB = CB.change_to(view=left)


# ----------------------------------------------------------------------------- #
# Displaying various parameters
# ----------------------------------------------------------------------------- #

# ### print if the cube is solved or not ###
# print(CB.is_solved())

# ### print a view/face side ###
# pprint(CB.show(front))

# ### print side of the face for a particular direction ###
# face = back
# direction = "y"

# for band in CB.views[face]:
# 	for piece in band:
# 		print(piece.members[direction])

# ----------------------------------------------------------------------------- #
