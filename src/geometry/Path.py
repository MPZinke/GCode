#!/opt/homebrew/bin/python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2025.11.30                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


import json
from math import sin, cos
from typing import Optional


from tkinter import BOTH, Canvas, Frame, Tk


from geometry.Point import Point


Path = type("Path", (), {})
θ = int|float


class Path:
	__size__: Optional[int] = None


	def __class_getitem__(cls, __size__: int):
		if(not isinstance(__size__, int)):
			raise TypeError(f"For Point[size], size must be of type int, not {type(__size__).__name__}")

		name = f"""{cls.__name__}[{__size__}]"""
		return type(name, (cls,), {"__size__": __size__})


	def __init__(self, *points: tuple[Point]):
		self.points: list[Point] = list(points)


	def __getitem__(self, index: int) -> int:
		return self.points[index]


	def __iter__(self) -> list:
		yield from [point.copy() for point in self.points]


	def __str__(self) -> str:
		return json.dumps(list(self))


	def __len__(self) -> int:
		return len(self.points)


	def draw(self, gui, color: str="yellow") -> None:
		if(len(self.points) == 2):
			gui.draw_line(self, color)


	def is_visible(self) -> bool:
		return -1 * self.normal() * self.points[0] >= 0


	# ———————————————————————————————————————————————— LINEAR ALGEBRA ———————————————————————————————————————————————— #

	def normal(self) -> Point:
		if(len(self) < 3):
			raise Exception("Cannot normalize a shape that is less than 3 points")

		# TODO: Fix for >3 points
		a1, a2, a3 = list(self.points[1] - self.points[0])
		b1, b2, b3 = list(self.points[2] - self.points[1])
		return Point((a2 * b3 - a3 * b2), (a3 * b1 - a1 * b3), (a1 * b2 - a2 * b1))


	def project(self, lense_z: int, plane_depth: int) -> Path:
		return Path(*[point.project(lense_z, plane_depth) for point in self.points[:2]])


	def rotate(self, x_rotation: θ, y_rotation: θ, z_rotation: θ) -> Path:
		"""
		FROM: https://www.analyzemath.com/linear-algebra/applications-of-matrices/matrix-transformations-in-computer-graphics.html#google_vignette
		"""
		x_rotation_matrix = [
			[1,               0,                0, 0],
			[0, cos(x_rotation), -sin(x_rotation), 0],
			[0, sin(x_rotation),  cos(x_rotation), 0],
			[0,               0,                0, 1],
		]
		y_rotation_matrix = [
			[ cos(y_rotation), 0, sin(y_rotation), 0],
			[               0, 1,               0, 0],
			[-sin(y_rotation), 0, cos(y_rotation), 0],
			[               0, 0,               0, 1],
		]
		z_rotation_matrix = [
			[cos(z_rotation), -sin(z_rotation), 0, 0],
			[sin(z_rotation),  cos(z_rotation), 0, 0],
			[              0,                0, 1, 0],
			[              0,                0, 0, 1],
		]

		return Path(*[point.rotate(x_rotation_matrix, y_rotation_matrix, z_rotation_matrix) for point in self.points])


	def scale(self, *scalings: list[int|float]) -> Point:
		return Path[len(self)](*map(lambda point: point.scale(*scalings), self))


	def translate(self, *translations: list[int|float]):
		return Path[len(self)](*map(lambda point: point.translate(*translations), self.points))
