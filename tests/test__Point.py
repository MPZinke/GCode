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


from geometry import Point


def test__Point__bitor():
	assert (Point(None, 2, 3) | Point(3, 2, 1)).coordinates == [3, 2, 3]


def test__Point__equals():
	assert Point(1, 2, 3) == Point(1, 2, 3)


def test__Point__not_equals():
	assert Point(1, 2, 3) != Point(3, 2, 1)
