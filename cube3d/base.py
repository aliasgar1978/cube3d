
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

	def __init__(self, **kwargs):
		self.members = {'x':{'direction': None , 'xiscolor': None}, 
			'y':{'direction': None , 'xiscolor': None}, 
			'z':{'direction': None , 'xiscolor': None} }
		self.set(**kwargs)
	
	def set(self, **kwargs):
		for k, v in kwargs.items():
			if k in XISCOLOR: self.members[k[0]]['xiscolor'] = v
			if k in AXISES: self.members[k[0]]['direction'] = v

class Band(Members): pass
class Square(Members): pass

class Cube(Members):

	def __init__(self, *arg):
		super().__init__(*arg)
		self.set_initial_views()

	def set_initial_views(self):
		self.views = {
			front: 	self[0],
			back: 	np.flip(np.flip(self[2]), 1),
			left: 	np.flip(self[...,0].T, 1),
			right: 	self[...,2].T,
			top: 	self[[0,1,2], 2],
			bottom: np.flip(np.flip(self[[0,1,2], 0]), 1),
			}

	def show(self, view):
		op_dic = []
		xis = view_dir[view]
		for band in self.views[view]:
			for piece in band:
				op_dic.append(piece.members[xis])
		op_dic = np.array(op_dic)
		op_dic.resize(3,3)
		return op_dic

	def update_view(self, view, updated_sqr):
		for i, band in enumerate(self.views[view]):
			for j, piece in enumerate(band):
				
				self.views[view][i, j] = updated_sqr.members.flat[i*3+j]


	def is_solved(self):
		for view, xis in view_dir.items():
			for band in self.views[view]:
				if not self.all_points_same(band, xis): return False
		return True

	@staticmethod
	def all_points_same(band, xis):
		xiscolor = ''
		for piece in band:
			piece_color = piece.members[xis]['xiscolor']#[:3]
			if xiscolor == '':
				xiscolor = piece_color
				continue
			elif xiscolor != piece_color:
				return False
		return True

	# Rotation of Cube --------------------------------

	def change_to_bottom(cube):
		l = [cube[[2,1,0], i] for i in range(3)]
		return rotate_cube(l, swap_axis=('y', 'z'), inverse_axis='z')

	def change_to_top(cube):
		l = [cube[[0,1,2], i] for i in reversed(range(3))]
		return rotate_cube(l, swap_axis=('y', 'z'), inverse_axis='y')

	def change_to_left(cube):
		l = np.array([cube[...,j][[2,1,0], i] for j in range(3) for i in range(3)])
		l.resize(3,3,3)
		return rotate_cube(l, swap_axis=('x', 'z'), inverse_axis='z')

	def change_to_right(cube):
		l = np.array([cube[...,j][[0,1,2], i] for j in reversed(range(3)) for i in range(3)])
		l.resize(3,3,3)
		return rotate_cube(l, swap_axis=('x', 'z'), inverse_axis='x')

	def change_to_back(cube):
		_cube = cube.change_to_top()
		return _cube.change_to_top()

	def change_to(cube, view):
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
		sqr = cube.views[view]
		sqr = [ sqr[[0,1,2], i]  for i in reversed(range(3)) ] if clockwise else [ sqr[[2,1,0], i]  for i in range(3) ] 
		swap_axis = get_swap_axis(view, clockwise)
		inverse_axis = get_inverse_axis(swap_axis, clockwise)
		updated_sqr = rotate_square(sqr, swap_axis=swap_axis, inverse_axis=inverse_axis)
		cube.update_view(view, updated_sqr)



### Functions for Square ###

def get_swap_axis(view, clockwise):
	swap_axis = {
		front: ('x', 'y'), back: ('y', 'x'),
		left: ('y', 'z'), right: ('z', 'y'),
		top: ('x', 'z'), bottom: ('z', 'x'),
		}
	return swap_axis[view] if clockwise else tuple(reversed(swap_axis[view]))

def get_inverse_axis(swap_axis, clockwise):
	return swap_axis[0] if clockwise else swap_axis[1]

def rotate_square(bands, *args, **kwargs):
	s = Square(*bands)
	return change_position(s, *args, **kwargs)


### Functions for Cube ###

def rotate_cube(squares, *args, **kwargs):
	c = Cube(*squares)
	return change_position(c, *args, **kwargs)


### Functions Common ###

def change_position(instance, swap_axis, inverse_axis):
	a, b = swap_axis[0], swap_axis[1]
	for point in instance.members.flat:
		point.members[inverse_axis]['direction'] *= -1
		point.members[a], point.members[b] = point.members[b], point.members[a]
	return instance

