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


from itertools import zip_longest
import json
import math
from typing import Optional


Point = type("Point", (), {})


X = 0
Y = 1
Z = 2


class Point:
	__size__: Optional[int] = None


	def __class_getitem__(cls, __size__: int):
		if(not isinstance(__size__, int)):
			raise TypeError(f"For Point[size], size must be of type int, not {type(__size__).__name__}")

		name = f"""{cls.__name__}[{__size__}]"""
		return type(name, (cls,), {"__size__": __size__})


	def __init__(self, *coordinates: list[int|float]):
		if(self.__size__ is not None and len(coordinates) != self.__size__):
			raise ValueError(f"Expect size {self.__size__}, received {len(coordinates)}")

		for coordinate in coordinates:
			if(not isinstance(coordinate, (int, float))):
				raise TypeError(f"Invalid coordinate type {type(coordinate).__name__}")

		self.coordinates: list[int|float] = list(coordinates)


	def __iter__(self) -> iter:
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


	def __mul__(left: Point, right: int|float|Point|list[int|float]) -> int|Point:
		# TODO: Probably worthless—clean up
		if(isinstance(right, (int, float))):
			return Point(*[point * right for point in left])

		if(isinstance(right, list)):
			return Point(*map(lambda a, b: a * b, left, right))

		# Dot product
		if(isinstance(right, Point)):
			return sum(a * b for a, b in zip(left, right))

		raise TypeError(f"Expected int, float or Point not '{type(right).__name__}'")


	def __or__(left: Point, right: Point) -> Point:
		"""
		Create a copy of left and replace any None values with right's value.
		"""
		if(len(left) != len(right)):
			raise ValueError(f"Left size {left.__size__} does not match right size {len(right)}")

		selector = lambda left, right: left if(left is not None) else right
		return Point[len(left)](*map(selector, left.coordinates, right.coordinates))


	def __rmul__(right, left) -> int:
		return right.__mul__(left)


	def __pow__(left, right: float) -> Point:
		return Point(*[a ** right for a in left])


	def __sub__(left, right) -> Point:
		return Point(*[a - b for a, b in zip(left, right)])


	@property
	def x(self) -> Point:
		if(len(self.coordinates) <= X):
			return NotImplemented  # Pointless Point?

		return self.coordinates[X]


	@property
	def y(self) -> Point:
		if(len(self.coordinates) <= Y):
			return NotImplemented

		return self.coordinates[Y]


	@property
	def z(self) -> Point:
		if(len(self.coordinates) <= Z):
			return NotImplemented

		return self.coordinates[Z]


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
		return Point[len(self)-1](*[coordinate * ratio for coordinate in self.coordinates[:-1]])


	def scale(self, *scalings: list[float]) -> Point:
		scaled_coordinates: list[int|float] = []
		for coordinate, scaling in zip_longest(self, scalings):
			scaled_coordinates.append(coordinate * (scaling or 1))

		return Point[len(self)](*scaled_coordinates)


	def rotate(self, x_matrix: list[list[int|float]], y_matrix: list[list[int|float]], z_matrix: list[list[int|float]]):
		"""
		FROM: https://www.analyzemath.com/linear-algebra/applications-of-matrices/matrix-transformations-in-computer-graphics.html#google_vignette
		"""
		# TODO


	def translate(self, *translations: list[int|float]) -> Point:
		translated_coordinates: list[int|float] = []
		for coordinate, translation in zip_longest(self, translations):
			translated_coordinates.append(coordinate + (translation or 0))

		return Point[len(self)](*translated_coordinates)
