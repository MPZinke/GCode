
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
	def __init__(self, pixels_per_inch: float=127.0):
		super().__init__()
		self.tk.call('tk', 'scaling', 175.0/100.0)
		self.title("Image")
		self.geometry("1440x847")

		# View point
		self._current_location = [0, 0, 18]
		self._current_rotation = [0, 0, 0]
		self._screen_distance_from_lense = 18

		self.bind("<Up>", self.on_scroll)
		self.bind("<Down>", self.on_scroll)
		self.bind("<Left>", self.on_scroll)
		self.bind("<Right>", self.on_scroll)

		# Drawing
		self._canvas_frame = Frame(self)
		self._canvas_frame.pack(fill=BOTH, expand=1)
		self._canvas = Canvas(self._canvas_frame)
		self._pixels_per_inch: float = pixels_per_inch
		self._screen_size: tuple[int, int] = [1440, 847]

		self._paths: list[Path] = []


	def on_scroll(self, event):
		print(event.keysym)
		# self._current_location[Z] += event.delta/120
		# TODO: make relative based on current rotation
		match(event.keysym):
			case "Up":
				self._current_location[Z] += 1

			case "Down":
				self._current_location[Z] -= 1

			case "Left":
				self._current_location[X] -=1

			case "Right":
				self._current_location[X] +=1

			case _:
				print(event.keysym)

		self.redraw()


	def redraw(self):
		self._canvas.delete("all")
		self.draw()


	def draw(self):
		for path in self._paths:
			translated_path: Path = path.translate(self._current_location[X], self._current_location[Y])
			# TODO: Rotate
			translated_path.draw(self)

		self.draw_origin()

		self._canvas.pack(fill=BOTH, expand=1)


	def add_path(self, path: Path) -> None:
		self._paths.append(path)


	def draw_line(self, path: Path, color: str):
		projected_points: list[Point] = path.project(self._current_location[Z], self._screen_distance_from_lense)

		# Translate for GUI display (inverted y-axis and translated x & y axes).
		scale_and_invert_y_matrix = [self._pixels_per_inch, -self._pixels_per_inch]
		scaled_and_inverted_y_points: list[Point] = [point.scale(*scale_and_invert_y_matrix) for point in projected_points]

		center_matrix = [self._screen_size[WIDTH]//2, self._screen_size[HEIGHT]//2]
		centered_points: list[Point] = [point.translate(*center_matrix) for point in scaled_and_inverted_y_points]

		coordinates: list[int] = [int(coordinate) for point in centered_points for coordinate in point]

		self._canvas.create_line(*coordinates, fill=color, width=2)


	def draw_origin(self):
		origin_distance: float = math.sqrt(
			self._current_location[X]**2
			+ self._current_location[Y]**2
			+ self._current_location[Z]**2
		)
		axes_paths: list[Path] = [
			Path(Point(0, 0, 0), Point(1, 0, 0)),
			Path(Point(0, 0, 0), Point(0, 1, 0)),
			Path(Point(0, 0, 0), Point(0, 0, 1)),
		]

		for axis_path, color in zip(axes_paths, ["red", "green", "blue"]):
			translated_path: Path = axis_path.translate(self._current_location[X], self._current_location[Y])
			self.draw_line(translated_path, color)


	def render(self):
		self.draw()
		self.mainloop()
