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
# Create a Cube using Excel file input
# ----------------------------------------------------------------------------- #
CB = get_cube("cube.xlsx")

# ----------------------------------------------------------------------------- #
# Another way to create a cube with static points: 
# (instead of providing Excel file as input)
# ----------------------------------------------------------------------------- #
# 1. Create 27 x "Point" objects
#    ex: P1 = Point(x=-1 ,y=-1  ,z=-1 , x_color='yellow', y_color='blue', z_color='red')
# 2. Create  9 x "Band"  objects using set of three-three Point objects
#    ex: B1 = Band(P1, P2, P3)
# 3. Create  3 x "Square" objects using set of three-three Band objects
#    ex: SQ1 = Square(B1, B2, B3)
# 4. Create  cube using three Square objects created above.
#    ex: CB = Cube(SQ1, SQ2, SQ3)
# ----------------------------------------------------------------------------- #


# ----------------------------------------------------------------------------- #
# use below rotate_square method to Rotate a square/face/view to a direction
# view = defines the face which require to be rotated
# clockwise = direction looking from front of the view 
#             ( True=Clockwise direction, False=Anticlockwise direction ), 
#             default=clockwise (i.e: True)
# ----------------------------------------------------------------------------- #
CB.rotate_square(view=front, clockwise=False)


# ----------------------------------------------------------------------------- #
# use below change_to method to Change the Cube view to another direction
# view = defines the face to which we want to face.
# ----------------------------------------------------------------------------- #
CB = CB.change_to(view=left)


# ----------------------------------------------------------------------------- #
# Verification/Display - parameters
# ----------------------------------------------------------------------------- #

# ### print if the cube is solved or not ###
print(CB.is_solved())

# ### print a view/face side ###
pprint(CB.show(front))

# ### print side of the face for a particular direction ###
face = back
direction = "y"

for band in CB.views[face]:
	for piece in band:
		print(piece.members[direction])

# ----------------------------------------------------------------------------- #
