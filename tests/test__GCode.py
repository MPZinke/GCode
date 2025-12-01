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


from pathlib import Path
import sys
SOURCE_DIR = Path(__file__).parents[1] / "src"
sys.path.append(str(SOURCE_DIR))


from io import BytesIO, StringIO


from gcode import GCode


def test__GCode__bytes():
	gcode = GCode(b"G1 X0")


def test__GCode__str():
	gcode = GCode("G1 X0")


def test__GCode__BytesIO():
	gcode = GCode(BytesIO(b"G1 X0"))


def test__GCode__StringIO():
	gcode = GCode(StringIO("G1 X0"))


def test__GCode__file():
	with open("test", "w+") as file:
		gcode = GCode(file)


def test__GCode__Path():
	gcode = GCode(Path(__file__))


def test__GCode__str__command():
	gcode = GCode("G1 ; test")
	assert gcode.commands[0].command == "G1"
	assert gcode.commands[0].args == []


def test__GCode__str__args():
	gcode = GCode("G1 X0 Y0")
	assert gcode.commands[0].args == ["X0", "Y0"]


def test__GCode__iter_single():
	for path in GCode("G1 X1 Y1"):
		print(path)


def test__GCode__iter_multiple():
	for path in GCode("G1 X1 Y1 F5\nG1 X0 F5"):
		print(path)


def test__GCode__iter_multiple_ignore():
	for path in GCode("G1 X1 Y1 F5\nG-1\nG1 X0 F5\n"):
		print(path)
