"""Model defining 0D, 1D, 2D, 3D elements requirements for cube and its rotation methods.
"""
import numpy as np

# ---------------

AXISES = ('x', 'y', 'z')
XISCOLOR = ('x_color', 'y_color', 'z_color')
# views
front, back, top, bottom, left, right = ('front', 'back', 'top', 'bottom', 'left', 'right')
view_dir = {front:'z', back:'z', top:'y', bottom:'y', left:'x', right:'x'}
axis_map = {
	front: {'z': -1},
	back: {'z': 1},
	top: {'y': 1},
	bottom: {'y': -1},
	left: {'x': -1},
	right: {'x': 1},
}
# ---------------

class Members():
	"""Common Methods and properties defining multiple member types
	Initialize different kinds of objects by providing respective arguments.

	Common properties/methods available are:
		* len()
		* getitem
		* reversed()
		* iterate over
	"""	
	def __init__(self, *arg): self.members = np.array(arg)
	def __len__(self): return len(self.members)
	def __getitem__(self, i): return self.members[i]
	def __reversed__(self): return reversed(self.members)
	def __iter__(self): 
		if isinstance(self.members, np.ndarray):
			return (member for member in self.members)
		elif isinstance(self.members, dict):
			return ({xis: member} for xis, member in self.members.items())


class Point():
	"""A Zero-Dimentional; Single Point Object and its properties.
	"""    	

	def __init__(self, **kwargs):
		"""Initialize Point Object by providing its co-ordinates and colors.
		"""    		
		self.members = {'x':{'direction': None , 'xiscolor': None}, 
			'y':{'direction': None , 'xiscolor': None}, 
			'z':{'direction': None , 'xiscolor': None} }
		self.set(**kwargs)
	
	def set(self, **kwargs):
		"""set the Point objects co-ordinates and colors.
		"""    		
		for k, v in kwargs.items():
			if k in XISCOLOR: self.members[k[0]]['xiscolor'] = v
			if k in AXISES: self.members[k[0]]['direction'] = v

class Band(Members): 
	"""A One-Dimentional; Line object and its properties
	"""	
	pass
class Square(Members): 
	"""A Two-Dimentional; Square object and its properties
	"""	
	pass

class Cube(Members):
	"""A Three-Dimentional; Cube object and its properties 
	"""    	

	def __init__(self, *arg):
		"""Initialize Cube object by providing its members as in arguments. which will be numpy array of arrays
		"""    		
		super().__init__(*arg)
		self.set_initial_views()

	def set_initial_views(self):
		"""set all six faces of cube. faces are (front, back, left, right, top, bottom)
		"""    		
		self.views = {
			front: 	self[0],
			back: 	np.flip(np.flip(self[2]), 1),
			left: 	np.flip(self[...,0].T, 1),
			right: 	self[...,2].T,
			top: 	self[[0,1,2], 2],
			bottom: np.flip(np.flip(self[[0,1,2], 0]), 1),
		}

	def show(self, view):
		"""return the face of cube. view=face=side  faces are (front, back, left, right, top, bottom)

		Args:
			view (str): face of a cube

		Returns:
			list: Two dimentional Square Object detail
		"""    		
		op_dic = []
		xis = view_dir[view]
		for band in self.views[view]:
			for piece in band:
				op_dic.append(piece.members[xis])
		op_dic = np.array(op_dic)
		op_dic.resize(3,3)
		return op_dic

	def update_view(self, view, updated_sqr):
		"""update face of cube with given updated Square

		Args:
			view (str): face of a cube
			updated_sqr (Square): Square object, numpy array of array
		"""    		
		for i, band in enumerate(self.views[view]):
			for j, piece in enumerate(band):
				
				self.views[view][i, j] = updated_sqr.members.flat[i*3+j]


	def is_solved(self):
		"""check is cube in solved position

		Returns:
			bool: True if solved, else False
		"""    		
		for view, xis in view_dir.items():
			for band in self.views[view]:
				if not self._all_points_same(band, xis): return False
		return True

	@staticmethod
	def _all_points_same(band, xis):
		"""to check the provided axis color remain unchanged or not.

		Args:
			band (Square): Square 2D object
			xis (str): axis (x,y,z)

		Returns:
			bool: True if all colors are same as previous, else False
		"""    		
		xiscolor = ''
		for piece in band:
			piece_color = piece.members[xis]['xiscolor']#[:3]		# enable [:3] to match only first 3 characters of color
			if xiscolor == '':
				xiscolor = piece_color
				continue
			elif xiscolor != piece_color:
				return False
		return True

	# Rotation of Cube --------------------------------

	def change_to_bottom(cube):
		"""Turn the whole cube, i.e. Turn cube such face it faces now towards bottom Square.

		Returns:
			Cube: updated cube after move
		"""    		
		l = [cube[[2,1,0], i] for i in range(3)]
		return _rotate_cube(l, swap_axis=('y', 'z'), inverse_axis='z')

	def change_to_top(cube):
		"""Turn the whole cube, i.e. Turn cube such face it faces now towards top Square.

		Returns:
			Cube: updated cube after move
		"""    		
		l = [cube[[0,1,2], i] for i in reversed(range(3))]
		return _rotate_cube(l, swap_axis=('y', 'z'), inverse_axis='y')

	def change_to_left(cube):
		"""Turn the whole cube, i.e. Turn cube such face it faces now towards left Square.

		Returns:
			Cube: updated cube after move
		"""    		
		l = np.array([cube[...,j][[2,1,0], i] for j in range(3) for i in range(3)])
		l.resize(3,3,3)
		return _rotate_cube(l, swap_axis=('x', 'z'), inverse_axis='z')

	def change_to_right(cube):
		"""Turn the whole cube, i.e. Turn cube such face it faces now towards right Square.

		Returns:
			Cube: updated cube after move
		"""    		
		l = np.array([cube[...,j][[0,1,2], i] for j in reversed(range(3)) for i in range(3)])
		l.resize(3,3,3)
		return _rotate_cube(l, swap_axis=('x', 'z'), inverse_axis='x')

	def change_to_back(cube):
		"""Turn the whole cube, i.e. Turn cube such face it faces now towards back Square.

		Returns:
			Cube: updated cube after move
		"""    		
		_cube = cube.change_to_top()
		return _cube.change_to_top()

	def change_to(cube, view):
		"""Turn the whole cube, i.e. Turn cube such face it faces now towards give view side.

		Args:
			view (str): face name to turn towards

		Returns:
			Cube: updated cube after move
		"""    		
		maps = {
			left: cube.change_to_left(),
			right: cube.change_to_right(),
			top: cube.change_to_top(),
			bottom: cube.change_to_bottom(),
			back: cube.change_to_back(),
		}
		return maps[view]

	# Rotation of a Square --------------------------------

	def rotate_square(cube, view, clockwise=True):
		"""rotate a side/view of cube in given direction perspective to that face.

		Args:
			view (str): face name to be rotated
			clockwise (bool, optional): True will rotate clockwise False will rotate anti-clockwise. Defaults to True.
		"""    		
		sqr = cube.views[view]
		sqr = [ sqr[[0,1,2], i]  for i in reversed(range(3)) ] if clockwise else [ sqr[[2,1,0], i]  for i in range(3) ] 
		swap_axis = _get_swap_axis(view, clockwise)
		inverse_axis = _get_inverse_axis(swap_axis, clockwise)
		updated_sqr = _rotate_square(sqr, swap_axis=swap_axis, inverse_axis=inverse_axis)
		cube.update_view(view, updated_sqr)



### Functions for Square ###

def _get_swap_axis(view, clockwise):
	"""during rotation of a square, axis directions will get changed for some points. this function takes care
	of it.

	Args:
		view (str): face name getting rotated
		clockwise (bool): direction of rotation True=Clockwise, False=anti-clockwise

	Returns:
		tuple: detail in tuple for axis to be swapped.
	"""	
	swap_axis = {
		front: ('x', 'y'), back: ('y', 'x'),
		left: ('y', 'z'), right: ('z', 'y'),
		top: ('x', 'z'), bottom: ('z', 'x'),
		}
	return swap_axis[view] if clockwise else tuple(reversed(swap_axis[view]))

def _get_inverse_axis(swap_axis, clockwise):
	"""returns the axis which is needed to be inversed based on rotation direction.

	Args:
		swap_axis (tuple): axis details to be swapped during rotations
		clockwise (bool): direction of rotation True=Clockwise, False=anti-clockwisere

	Returns:
		str: axis to be inversed
	"""    	
	return swap_axis[0] if clockwise else swap_axis[1]

def _rotate_square(bands, *args, **kwargs):
	"""rotate given square/band with provided swap axis and inverse_axis details in kwargs.
	kwargs defines = swap_axis, inverse_axis

	Args:
		bands (Square): Square 2D object (containing bands) to be rotated.

	Returns:
		Square: Square 2D object after rotation.
	"""    	
	s = Square(*bands)
	return _change_position(s, *args, **kwargs)


### Functions for Cube ###

def _rotate_cube(squares, *args, **kwargs):
	"""rotate given cube with provided swap axis and inverse_axis details in kwargs. 

	Args:
		squares (Cube): Cube 3D object (containing Squares) to be rotated

	Returns:
		Cube: Cube 3D object
	"""    	
	c = Cube(*squares)
	return _change_position(c, *args, **kwargs)


### Functions Common ###

def _change_position(instance, swap_axis, inverse_axis):
	"""rotate an instance/object (either Square, Cube)

	Args:
		instance (Square, Cube): Either Square-2D , Cube-3D object
		swap_axis ([type]): axis to be swapped
		inverse_axis ([type]): axis to be inversed

	Returns:
		Square, Cube: Either Square-2D , Cube-3D object
	"""    	
	a, b = swap_axis[0], swap_axis[1]
	for point in instance.members.flat:
		point.members[inverse_axis]['direction'] *= -1
		point.members[a], point.members[b] = point.members[b], point.members[a]
	return instance

