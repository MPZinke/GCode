
from tkinter import *
from tkinter import ttk


from gcode import GCode
from geometry import Path, X, Y, Z


class GUI(Tk):
	def __init__(self, gcode: GCode):
		super().__init__()
		self.title("Image")
		self.geometry("1440x847")

		# View point
		self._current_location = [0, 0, 1]
		self._current_rotation = [0, 0, 0]

		# Drawing
		self._canvas_frame = Frame(self)
		self._canvas_frame.pack(fill=BOTH, expand=1)
		self._canvas = Canvas(self._canvas_frame)

		self.gcode = gcode


	def draw(self):
		# TODO: Make dynamic
		self._canvas.create_line([1440//2, 847//2, 1440, 847//2], fill="red", width=5)
		self._canvas.create_line([1440//2, 847//2, 1440//2, 0], fill="green", width=5)

		# Draw axes
		for path in self.gcode:
			path.draw(self)


	def draw_line(self, path: Path, color: str):
		print(path)
		path: Path = path.scale(200, 200, 200)
		print(path)
		coordinates = [coordinate for point in path.project(self._current_location[Z], 1) for x, coordinate in enumerate(point) if x < 2]
		print(coordinates)

		# Translate for GUI display (inverted y-axis and translated x & y axes)
		inverted_points = [(coordinate * (-1 if(x & 1) else 1)) for x, coordinate in enumerate(coordinates)]
		centered_points = [(coordinate + (847 if(x & 1) else 1440)//2) for x, coordinate in enumerate(inverted_points)]  # TODO: HEIGHT & WIDTH

		print(centered_points, end="\n\n")

		self._canvas.create_line(*centered_points, fill=color, width=2)

		self._canvas.pack(fill=BOTH, expand=1)
