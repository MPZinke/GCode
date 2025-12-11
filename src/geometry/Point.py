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
import math


Point = type("Point", (), {})


X = 0
Y = 1
Z = 2


class Point:
	def __init__(self, *coordinates: list[int]):
		self.coordinates: list[int] = list(coordinates)


	def __iter__(self) -> list:
		yield from self.coordinates


	def __str__(self) -> str:
		return json.dumps(list(self))


	def __len__(self) -> int:
		return len(self.coordinates)


	def __getitem__(self, index: int) -> int:
		return self.coordinates[index]


	def __abs__(self) -> Point:
		return Point(*[abs(a) for a in self])


	def __add__(left: Point, right: Point) -> Point:
		return Point(*[a + b for a, b in zip(left, right)])


	def __eq__(left: Point, right: Point) -> bool:
		return left.coordinates == right.coordinates


	def __truediv__(left: Point, right: float) -> Point:
		return Point(*[a / right if(right) else 0 for a in left])


	def __mul__(left: Point, right: int|float|Point) -> int:
		# TODO: Probably worthless—clean up
		if(isinstance(right, (int, float))):
			return Point(*[point * right for point in left])

		# Dot product
		if(isinstance(right, Point)):
			return sum(a * b for a, b in zip(left, right))

		raise TypeError(f"Expected int, float or Point not '{type(right).__name__}'")


	def __or__(left: Point, right: Point) -> Point:
		"""
		Create a copy of left and replace any None values with right's value.
		"""
		return Point(
			*[left if(left is not None) else right for left, right in zip(left.coordinates, right.coordinates)]
		)


	def __rmul__(right, left) -> int:
		return right * left


	def __pow__(left, right: float) -> Point:
		return Point(*[a ** right for a in left])


	def __sub__(left, right) -> Point:
		return Point(*[a - b for a, b in zip(left, right)])


	@property
	def x(self) -> Point:
		return self.coordinates[0]


	@property
	def y(self) -> Point:
		return self.coordinates[1]


	@property
	def z(self) -> Point:
		return self.coordinates[2]


	def copy(self) -> Point:
		return Point(*self.coordinates)


	def magnitude(self) -> int:
		"""
		Magnitude from 0, 0, ...
		"""
		return math.sqrt(sum(value ** 2 for value in self))


	def project(self, point_distance_from_lense: int, screen_distance_from_lense: int) -> Point:
		# TODO: Make relative lense coordinate.
		"""
		FROM https://www.scratchapixel.com/lessons/3d-basic-rendering/computing-pixel-coordinates-of-3d-point/mathematics-computing-2d-coordinates-of-3d-points
		---
		    (self.x / point_distance_from_lense) == (x / screen_distance_from_lense)
		    => x = (self.x * screen_distance_from_lense / point_distance_from_lense)
		"""
		ratio = screen_distance_from_lense / point_distance_from_lense if(point_distance_from_lense) else 0
		return self * ratio


	def rotate(x_matrix: list[list[int]], y_matrix: list[list[int]], z_matrix: list[list[int]]):
		"""
		FROM: https://www.analyzemath.com/linear-algebra/applications-of-matrices/matrix-transformations-in-computer-graphics.html#google_vignette
		"""
		# TODO


	def translate(self, *translations: list[int]) -> None:
		for i, translation in enumerate(translations):
			self.coordinates[i] += translation
