__doc__ = "3-Dimention rubic Cube"

"""
Virtual Three-Dimention Rubic cube.

Cube is expected to be visualized as below

						Back = TOP + TOP					
											
						O222	O221	O220			
						O212	O211	O210			
						O202	O201	O200			
						G220	G221	G222			
						G120	G121	G122			
						G020	G021	G022			
Y220	Y120	Y020	R020	R021	R022	W022	W122	W222
Y210	Y110	Y010	R010	R011	R012	W012	W112	W212
Y200	Y100	Y000	R000	R001	R002	W002	W102	W202
						B000	B001	B002			
						B100	B101	B102			
						B200	B201	B202			


all faces should be input in excel in each separate sheet named
( front, back, left, right, top, bottom )
refer  input sample excel file for the same.

===============================
SAMPLE EXECUTIONS:
===============================
from cube3d import get_cube

CB = get_cube("cube.xlsx")
pprint(CB.show(front))
print (CB.is_solved())
... and so on 
===============================


"""

__ver__ = "0.0.1"

__all__ = [ 
	'Point', 'Band', 'Cube',
	'get_cube'
	]

from .base import Point, Band, Cube
from .input import get_cube

