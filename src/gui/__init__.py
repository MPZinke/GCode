
import math
from tkinter import *
from tkinter import ttk


from gcode import GCode
from geometry import Path, Point, X, Y, Z


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
		self._current_location = [0, 0, 18]
		self._current_rotation = [0, 0, 0]
		self._screen_distance_from_lense = 18

		# Drawing
		self._canvas_frame = Frame(self)
		self._canvas_frame.pack(fill=BOTH, expand=1)
		self._canvas = Canvas(self._canvas_frame)
		self._pixels_per_inch: float = pixels_per_inch
		self._screen_size: tuple[int, int] = [1440, 847]

		self.bind("<Up>", self.on_scroll)
		self.bind("<Down>", self.on_scroll)

		self.gcode = gcode


	def on_scroll(self, event):
		# self._current_location[Z] += event.delta/120
		self._current_location[Z] += 1 if(event.keysym == "Up") else -1
		self.redraw()


	def redraw(self):
		self._canvas.delete("all")
		self.draw()


	def draw(self):
		# self._canvas.create_line([1440//2, 847//2, 126+1440//2, 847//2], fill="white", width="1i")
		# TODO: Make dynamic
		# Determine zoom (distance to center) to determine line length
		# origin_distance_ratio: float = math.sqrt(
		# 	self._current_location[X]**2
		# 	+ self._current_location[Y]**2
		# 	+ self._current_location[Z]**2
		# ) / self._screen_distance_from_lense
		# x_axis_path = Path(Point(0, 0, 0), Point(origin_distance_ratio, 0, 0))
		# y_axis_path = Path(Point(0, 0, 0), Point(0, origin_distance_ratio, 0))
		# z_axis_path = Path(Point(0, 0, 0), Point(0, 0, origin_distance_ratio))
		# # Translate

		# # Rotate

		# self.draw_line(x_axis_path, "red")
		# self.draw_line(y_axis_path, "green")
		# self.draw_line(z_axis_path, "blue")

		# Draw axes
		for path in self.gcode:
			path.draw(self)

		self.draw_origin()

		self._canvas.pack(fill=BOTH, expand=1)


	def draw_line(self, path: Path, color: str):
		# TODO: project for view point
		projected_points: list[Point] = path.project(self._current_location[Z], self._screen_distance_from_lense)

		# Translate for GUI display (inverted y-axis and translated x & y axes).
		scale_and_invert_y_matrix = [self._pixels_per_inch, -self._pixels_per_inch]
		scaled_and_inverted_y_points: list[Point] = [point.scale(*scale_and_invert_y_matrix) for point in projected_points]

		center_matrix = [self._screen_size[WIDTH]//2, self._screen_size[HEIGHT]//2]
		centered_points: list[Point] = [point.translate(*center_matrix) for point in scaled_and_inverted_y_points]

		coordinates: list[int] = [int(coordinate) for point in centered_points for coordinate in point]

		self._canvas.create_line(*coordinates, fill=color, width=2)


	def draw_origin(self):
		axes_paths: list[Path] = [
			Path(Point(0, 0, 0), Point(self._pixels_per_inch, 0, 0)),
			Path(Point(0, 0, 0), Point(0, -self._pixels_per_inch, 0)),
			Path(Point(0, 0, 0), Point(0, 0, self._pixels_per_inch)),
		]


		center_matrix = [self._screen_size[WIDTH]//2, self._screen_size[HEIGHT]//2]
		for axes_path, color in zip(axes_paths, ["red", "green", "blue"]):
			# Translate
			# Rotate
			# Project
			projected_points: list[Point] = axes_path.project(self._screen_distance_from_lense, self._screen_distance_from_lense)

			# Translate for GUI display (inverted y-axis and translated x & y axes).
			centered_points: list[Point] = [point.translate(*center_matrix) for point in projected_points]
			coordinates: list[int] = [int(coordinate) for point in centered_points for coordinate in point]
			self._canvas.create_line(*coordinates, fill=color, width=2)
