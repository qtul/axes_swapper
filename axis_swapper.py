#! /usr/bin/env python

#    Tool to swap axes in G code (e.g. to wrap 2.5D program around rotary axis)
#    Copyright (C) 2013 Qtul Enterprises (http://qtul.com/)
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

#Script to convert a 2.5D G code file to a rotary axis
#Specifically, this converts the Y axis to A axis
#A axis needs to be negated to maintain mirror correctness

import math
import re
import sys


if len(sys.argv) != 4:
	print len(sys.argv)
	print('Usage:')
	print(sys.argv[0] + ' Circumference InFile OutFile')
	print("""Where:
\tCircumference is the length in the Y axis which corresponds to a 360 degrees rotation
\tInFile is the file which will be converted
\tOutFile is the file where all Y axis references are converted to A axis and scaled
""")
	sys.exit(1)

#Parse arguments
Circ = float(sys.argv[1])
InFile = open(sys.argv[2], 'r')
OutFile = open(sys.argv[3], 'w')

#Verify dimensions and conversion with user
print('Circumference = ' + str(Circ) + '\tDiameter = ' + str(Circ / math.pi))
print('1 length unit = ' + str(360 / Circ) + ' degrees\t1 degree = ' + str(Circ / 360) + ' length units')

#Search for all Y words and replace them with A words
FeedRate = AngularFeedRate = 0
for line in InFile:
	#A combined linear and rotational axis move has a (dimensionally) incorrect tangential feed rate
	#For the most part this is not a significant issue since the linear axis dominate numerically
	#When the rotational axis move appears by itself, the feed rate causes the axis to move unbearably slow
	#Because of this, we have to assign angular feed rates when the rotational axis appears by itself
	#Likewise, in all other cases, we must assign tangential feed rates

	#Update F word (tangential feed rate)
	Matches = re.search(r'[fF]([-+]?[0-9]*\.?[0-9]+)\s*[a-zA-z]*', line)
	if Matches:
		FeedRate = float(Matches.group(1))
		#Calculate angular feed rate
		AngularFeedRate = FeedRate * 360 / Circ

	#Swap Y and A words
	Matches = re.search(r'[yY]([-+]?[0-9]*\.?[0-9]+)\s*[a-zA-z]*', line)
	if Matches:
		#Calculate A word
		Angle = -float(Matches.group(1)) * 360 / Circ
		#Replace Y word with A word
		line = re.sub(r'[yY][-+]?[0-9]*\.?[0-9]+', 'A' + str(Angle), line)

	#Add or replace F word
	#If linear axes are present ...
	if re.search(r'[xX][-+]?[0-9]*\.?[0-9]+', line) or re.search(r'[zZ][-+]?[0-9]*\.?[0-9]+', line):
		#... and no F word is specified ...
		if not re.search(r'[fF]', line):
			#... then we should add our own F word (tangential feed rate)
			line = line.strip() + ' F' + str(FeedRate) + '\n'
	#No linear axes are present ...
	else:
		#... but there might be a rotational axis by itself
		if re.search(r'[aA][-+]?[0-9]*\.?[0-9]+', line):
			#Replace the F word if it exists
			if re.search(r'[fF]', line):
				line = re.sub(r'[fF][-+]?[0-9]*\.?[0-9]+', 'F' + str(AngularFeedRate), line)
			#Add it to the end if it doesn't
			else:
				line = line.strip() + ' F' + str(AngularFeedRate) + '\n'

	OutFile.write(line)

