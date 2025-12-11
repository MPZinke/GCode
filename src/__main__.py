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


from gcode import GCode
from gui import GUI


def main():
	gcode = GCode("G1 X1\nG1 Y1\nG1 X0 Y0")
	gui = GUI(gcode, 126)
	gui.draw()
	gui.mainloop()


if(__name__ == "__main__"):
	main()
