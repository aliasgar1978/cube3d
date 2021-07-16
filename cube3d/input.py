
import pandas as pd
from .base import *

def read_cube_from_excel(file):
	d = {}
	for side, ax in axis_map.items():
		transpose_for = (front, bottom, top, back)
		df = pd.read_excel(file, sheet_name=side, header=None).fillna("")
		if side in transpose_for:
			d[side] = df.T.to_dict()
		else:
			d[side] = df.to_dict()
	return d

def get_cube(file):
	d = read_cube_from_excel(file)
	P000 = Point(x=-1 ,y=-1  ,z=-1 , x_color=d[left][2][2], y_color=d[bottom][0][0], z_color=d[front][2][0])
	P001 = Point(x=0  ,y=-1  ,z=-1 , x_color=None, y_color=d[bottom][0][1], z_color=d[front][2][1])
	P002 = Point(x=1  ,y=-1  ,z=-1 , x_color=d[right][0][2], y_color=d[bottom][0][2], z_color=d[front][2][2])
	P010 = Point(x=-1 ,y=0  ,z=-1 , x_color=d[left][2][1], y_color=None, z_color=d[front][1][0])
	P011 = Point(x=0  ,y=0  ,z=-1 , x_color=None, y_color=None, z_color=d[front][1][1])
	P012 = Point(x=1  ,y=0  ,z=-1 , x_color=d[right][0][1], y_color=None, z_color=d[front][1][2])
	P020 = Point(x=-1 ,y=1  ,z=-1 , x_color=d[left][2][0], y_color=d[top][2][0], z_color=d[front][0][0])
	P021 = Point(x=0  ,y=1  ,z=-1 , x_color=None, y_color=d[top][2][1], z_color=d[front][0][1])
	P022 = Point(x=1  ,y=1  ,z=-1 , x_color=d[right][0][0], y_color=d[top][2][2], z_color=d[front][0][2])

	P100 = Point(x=-1 ,y=-1  ,z=0 , x_color=d[left][1][2], y_color=d[bottom][1][0], z_color=None)
	P101 = Point(x=0  ,y=-1  ,z=0 , x_color=None, y_color=d[bottom][1][1], z_color=None)
	P102 = Point(x=1  ,y=-1  ,z=0 , x_color=d[right][1][2], y_color=d[bottom][1][2], z_color=None)
	P110 = Point(x=-1 ,y=0  ,z=0 , x_color=d[left][1][1], y_color=None, z_color=None)
	P111 = Point(x=0  ,y=0  ,z=0 , x_color=None, y_color=None, z_color=None)
	P112 = Point(x=1  ,y=0  ,z=0 , x_color=d[right][1][1], y_color=None, z_color=None)
	P120 = Point(x=-1 ,y=1  ,z=0 , x_color=d[left][1][0], y_color=d[top][1][0], z_color=None)
	P121 = Point(x=0  ,y=1  ,z=0 , x_color=None, y_color=d[top][1][1], z_color=None)
	P122 = Point(x=1  ,y=1  ,z=0 , x_color=d[right][1][0], y_color=d[top][1][2], z_color=None)

	P200 = Point(x=-1 ,y=-1  ,z=1 , x_color=d[left][0][2], y_color=d[bottom][2][0], z_color=d[back][2][2])
	P201 = Point(x=0  ,y=-1  ,z=1 , x_color=None, y_color=d[bottom][2][1], z_color=d[back][2][1])
	P202 = Point(x=1  ,y=-1  ,z=1 , x_color=d[right][2][2], y_color=d[bottom][2][2], z_color=d[back][2][0])
	P210 = Point(x=-1 ,y=0  ,z=1 , x_color=d[left][0][1], y_color=None, z_color=d[back][1][2])
	P211 = Point(x=0  ,y=0  ,z=1 , x_color=None, y_color=None, z_color=d[back][1][1])
	P212 = Point(x=1  ,y=0  ,z=1 , x_color=d[right][2][1], y_color=None, z_color=d[back][1][0])
	P220 = Point(x=-1 ,y=1  ,z=1 , x_color=d[left][0][0], y_color=d[top][0][0], z_color=d[back][0][2])
	P221 = Point(x=0  ,y=1  ,z=1 , x_color=None, y_color=d[top][0][1], z_color=d[back][0][1])
	P222 = Point(x=1  ,y=1  ,z=1 , x_color=d[right][2][0], y_color=d[top][0][2], z_color=d[back][0][0])

	B00 = Band(P000, P001, P002)
	B01 = Band(P010, P011, P012)
	B02 = Band(P020, P021, P022)
	B10 = Band(P100, P101, P102)
	B11 = Band(P110, P111, P112)
	B12 = Band(P120, P121, P122)
	B20 = Band(P200, P201, P202)
	B21 = Band(P210, P211, P212)
	B22 = Band(P220, P221, P222)

	SQZ0 = Square(B00, B01, B02)
	SQZ1 = Square(B10, B11, B12)
	SQZ2 = Square(B20, B21, B22)

	return Cube(SQZ0, SQZ1, SQZ2)


