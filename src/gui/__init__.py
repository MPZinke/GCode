
from tkinter import *
from tkinter import ttk


from gcode import GCode
from geometry import Path, X, Y, Z


Width = int
Height = int
WIDTH = 0
HEIGHT = 1




class GUI(Tk):
	def __init__(self, gcode: GCode, pixels_per_inch: float=227.0):
		super().__init__()
		self.tk.call('tk', 'scaling', 175.0/100.0)
		self.title("Image")
		self.geometry("1440x847")


		# View point
		self._current_location = [0, 0, 4]
		self._current_rotation = [0, 0, 0]
		self._screen_distance_from_lense = 18

		# Drawing
		self._canvas_frame = Frame(self)
		self._canvas_frame.pack(fill=BOTH, expand=1)
		self._canvas = Canvas(self._canvas_frame)
		self._pixels_per_inch: float = pixels_per_inch
		self._screen_size: tuple[int, int] = [1440, 847]

		self.gcode = gcode


	def draw(self):
		self._canvas.create_line([1440//2, 847//2, 126+1440//2, 847//2], fill="white", width="1i")
		# TODO: Make dynamic
		center = [self._screen_size[WIDTH]//2, self._screen_size[HEIGHT]//2]
		self._canvas.create_line([center[WIDTH], center[HEIGHT], self._screen_size[WIDTH], center[HEIGHT]], fill="red", width=5)
		self._canvas.create_line([center[WIDTH], center[HEIGHT], center[WIDTH], 0], fill="green", width=5)

		# Draw axes
		for path in self.gcode:
			path.draw(self)


	def draw_line(self, path: Path, color: str):
		path: Path = path.scale(*[self._pixels_per_inch]*3)  # God bless python
		coordinates = [coordinate for point in path.project(self._current_location[Z], self._screen_distance_from_lense) for x, coordinate in enumerate(point) if x < 2]

		# Translate for GUI display (inverted y-axis and translated x & y axes)
		inverted_points = [(coordinate * (-1 if(x & 1) else 1)) for x, coordinate in enumerate(coordinates)]
		centered_points = [(coordinate + (self._screen_size[HEIGHT] if(x & 1) else self._screen_size[WIDTH])//2) for x, coordinate in enumerate(inverted_points)]  # TODO: HEIGHT & WIDTH

		print(centered_points, end="\n\n")

		self._canvas.create_line(*centered_points, fill=color, width=2)

		self._canvas.pack(fill=BOTH, expand=1)
