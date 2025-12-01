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


from io import IOBase
import pathlib
from typing import Optional


from tkinter import Canvas


from geometry import Path, Point, X, Y, Z


class Command:
	def __init__(self, command: str, *args: list[str]):
		self.command: str = command
		self.args: list[str] = list(args)

		self._command_iterator: Optional[iter] = None


	def __repr__(self) -> str:
		return str(self)


	def __str__(self) -> str:
		return f"{self.command} {' '.join(self.args)}"


	def path(self, start: Point) -> Optional[Path]:
		match(self.command):
			case "G0" | "G1":
				return Path(start, self._line_end() | start)


	def _line_end(self) -> Point:
		x = next(map(lambda p: int(p[1:]), filter(lambda p: p.upper().startswith("X"), self.args)), None)
		y = next(map(lambda p: int(p[1:]), filter(lambda p: p.upper().startswith("Y"), self.args)), None)
		z = next(map(lambda p: int(p[1:]), filter(lambda p: p.upper().startswith("Z"), self.args)), None)

		return Point(x, y, z)


class GCode:
	def __init__(self, data: bytes|str|IOBase|Path):
		self.commands: list[Command] = []
		self._interpret(data)

		self._current_command_index: int = 0
		self._current_location = Point(0, 0, 0)



	def _interpret(self, data: bytes|str|IOBase|Path) -> None:
		match(data):
			case bytes():
				data: str = data.decode()

			case str():
				pass

			case IOBase():
				contents: str|bytes = data.read()
				if(isinstance(contents, bytes)):
					contents = contents.decode()
				data: str = contents

			case pathlib.Path():
				with open(data, "r") as file:
					data: str = file.read()

			case _:
				raise TypeError(f"Expected GCode::data expected bytes, str, IOBase, Path not {type(data).__name__}")

		for line in data.split("\n"):
			stripped_line: str = line.strip()
			if(stripped_line == ""):
				continue

			raw_command: str = stripped_line.split(";")[0]
			self.commands.append(Command(*filter(None, raw_command.split())))


	def __iter__(self) -> iter:
		self._command_iterator = iter(self.commands)
		self._current_location = Point(0, 0, 0)

		return self


	def __next__(self) -> Path:
		path: Optional[Path] = next(self._command_iterator).path(self._current_location)
		while path is None:
			path: Optional[Path] = next(self._command_iterator).path(self._current_location)

		self._current_location = path[-1]
		return path
