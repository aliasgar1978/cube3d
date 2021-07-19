
import numpy as np

# --------------------------------------------------------------------------------------------
AXISES = ('x', 'y', 'z')
XISCOLOR = ('x_color', 'y_color', 'z_color')												# color of a cube
front, back, top, bottom, left, right = ('front', 'back', 'top', 'bottom', 'left', 'right')	# different views/directions
view_dir = {front:'z', back:'z', top:'y', bottom:'y', left:'x', right:'x'}					# axis/direction to which view belongs to
axis_map = {																				# -1, 1 : direction of axis
	front: {'z': -1},
	back: {'z': 1},
	top: {'y': 1},
	bottom: {'y': -1},
	left: {'x': -1},
	right: {'x': 1},
}
# --------------------------------------------------------------------------------------------

class Members():
	"""Papa class"""
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
	"""Point class defining a single Pag and its properties/methods on Rubix cube"""

	def __init__(self, **kwargs):
		self.members = {'x':{'direction': None , 'xiscolor': None}, 
			'y':{'direction': None , 'xiscolor': None}, 
			'z':{'direction': None , 'xiscolor': None} }
		self.set(**kwargs)
	
	def set(self, **kwargs):
		"""set the properties of Point instance
		valid arguments should be from XISCOLOR and AXISES variable
		"""
		for k, v in kwargs.items():
			if k in XISCOLOR: self.members[k[0]]['xiscolor'] = v
			if k in AXISES: self.members[k[0]]['direction'] = v

# Child class defining a sting/band(1D) object or a square(2D) object
class Band(Members): pass
class Square(Members): pass

class Cube(Members):
	"""Child class defining cube(3D) object and its methods/properties"""

	def __init__(self, *arg):
		super().__init__(*arg)
		self.set_initial_views()

	def set_initial_views(self):
		"""property setting: views of a cube - initial setting"""
		self.views = {
			front: 	self[0],
			back: 	np.flip(np.flip(self[2]), 1),
			left: 	np.flip(self[...,0].T, 1),
			right: 	self[...,2].T,
			top: 	self[[0,1,2], 2],
			bottom: np.flip(np.flip(self[[0,1,2], 0]), 1),
			}

	def show(self, view):
		"""Return a particular view in list
		valid views are from view_dir keys
		--> numpy.ndarray
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
		"""set a particular view from given updated_sqr (numpy 2D array)
		valid views are from view_dir keys
		"""
		for i, band in enumerate(self.views[view]):
			for j, piece in enumerate(band):
				self.views[view][i, j] = updated_sqr.members.flat[i*3+j]


	def is_solved(self):
		"""verfication: if cube is solved or not
		--> boolean
		"""
		for view, xis in view_dir.items():
			for band in self.views[view]:
				if not self.all_points_same(band, xis): return False
		return True

	@staticmethod
	def all_points_same(band, xis, prefix_match_char=0):
		"""verification: if all colors towards given axis of a band/square are same or not
		prefix_match_char: numeric value to match only given prefix characters of colors intead of full string.
		--> boolean
		"""
		xiscolor = ''
		for piece in band:
			if prefix_match_char:
				piece_color = piece.members[xis]['xiscolor'][:prefix_match_char]
			else:
				piece_color = piece.members[xis]['xiscolor']
			if xiscolor == '':
				xiscolor = piece_color
				continue
			elif xiscolor != piece_color:
				return False
		return True

	# Rotation of Cube --------------------------------

	def _change_to_bottom(cube):
		l = [cube[[2,1,0], i] for i in range(3)]
		return _rotate_cube(l, swap_axis=('y', 'z'), inverse_axis='z')

	def _change_to_top(cube):
		l = [cube[[0,1,2], i] for i in reversed(range(3))]
		return _rotate_cube(l, swap_axis=('y', 'z'), inverse_axis='y')

	def _change_to_left(cube):
		l = np.array([cube[...,j][[2,1,0], i] for j in range(3) for i in range(3)])
		l.resize(3,3,3)
		return _rotate_cube(l, swap_axis=('x', 'z'), inverse_axis='z')

	def _change_to_right(cube):
		l = np.array([cube[...,j][[0,1,2], i] for j in reversed(range(3)) for i in range(3)])
		l.resize(3,3,3)
		return _rotate_cube(l, swap_axis=('x', 'z'), inverse_axis='x')

	def _change_to_back(cube):
		_cube = cube._change_to_top()
		return _cube._change_to_top()

	def change_to(cube, view):
		"""Move the eye: Change the front view to another face of cube
		valid views are from view_dir keys
		"""
		maps = {
			left: cube._change_to_left(),
			right: cube._change_to_right(),
			top: cube._change_to_top(),
			bottom: cube._change_to_bottom(),
			back: cube._change_to_back(),
		}
		return maps[view]

	# Rotation of a Square --------------------------------

	def rotate_square(cube, view, clockwise=True):
		"""Action: rotate a plane/Square (9-pieces) of a given view in either direction,
		 w.r.t front view of the plane.
		valid views are from view_dir keys
		clockwise (boolean) - True = Clockwise / False = Anti-clock wise rotation of plane
		"""
		sqr = cube.views[view]
		sqr = [ sqr[[0,1,2], i]  for i in reversed(range(3)) ] if clockwise else [ sqr[[2,1,0], i]  for i in range(3) ] 
		swap_axis = _get_swap_axis(view, clockwise)
		inverse_axis = _get_inverse_axis(swap_axis, clockwise)
		updated_sqr = _rotate_square(sqr, swap_axis=swap_axis, inverse_axis=inverse_axis)
		cube.update_view(view, updated_sqr)

# --------------------------------------------------------------------------------------------

### Functions for Square ###

def _get_swap_axis(view, clockwise):
	"""returns a tuple of axis which are to be swapped based on view and rotation
	valid views are from view_dir keys
	clockwise (boolean) - True = Clockwise / False = Anti-clock wise rotation of plane
	--> tuple
	"""
	swap_axis = {
		front: ('x', 'y'), back: ('y', 'x'),
		left: ('y', 'z'), right: ('z', 'y'),
		top: ('x', 'z'), bottom: ('z', 'x'),
		}
	return swap_axis[view] if clockwise else tuple(reversed(swap_axis[view]))

def _get_inverse_axis(swap_axis, clockwise):
	"""returns an axis which require to be inversed ( +1/-1 ) based on the swapping axis and rotation
	swap_axis : tuple of axis which are to be swapped.
	clockwise (boolean) - True = Clockwise / False = Anti-clock wise rotation of plane
	--> str
	"""
	return swap_axis[0] if clockwise else swap_axis[1]

def _rotate_square(bands, *args, **kwargs):
	"""Rotate the Square/Band
	args/kwargs: should include, swap_axis and inverse_axis details.
	"""
	s = Square(*bands)
	return _change_position(s, *args, **kwargs)

# --------------------------------------------------------------------------------------------

### Functions for Cube ###

def _rotate_cube(squares, *args, **kwargs):
	"""Rotate the Cube
	args/kwargs: should include, swap_axis and inverse_axis details.
	"""
	c = Cube(*squares)
	return _change_position(c, *args, **kwargs)


# --------------------------------------------------------------------------------------------

### Functions:  Common ###

def _change_position(instance, swap_axis, inverse_axis):
	"""changes position of points on an instance ( Either Band or Cube )
	swap_axis: tuple of axis to be swapped
	inverse_axis: axis to be inversed direction	
	--> updated instance
	"""
	a, b = swap_axis[0], swap_axis[1]
	for point in instance.members.flat:
		point.members[inverse_axis]['direction'] *= -1
		point.members[a], point.members[b] = point.members[b], point.members[a]
	return instance

# --------------------------------------------------------------------------------------------

