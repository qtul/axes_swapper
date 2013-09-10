axes_swapper
============

Tool to swap axes in G code (e.g. to wrap 2.5D program around rotary axis)


Author
------

Yi Yao, Founder of Qtul Enterprises
http://qtul.com/


License
-------

    Tool to swap axes in G code (e.g. to wrap 2.5D program around rotary axis)
    Copyright (C) 2013 Qtul Enterprises (http://qtul.com/)

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.


Usage
-----

```shell
axis_swapper.py Circumference InFile OutFile
```

or

```shell
python axis_swapper.py Circumference InFile OutFile
```

Where:
* Circumference is the length in the Y axis which corresponds to a 360 degrees rotation
* InFile is the file which will be converted
* OutFile is the file where all Y axis references are converted to A axis and scaled


For example:

```shell
axis_swapper.py 5 Test_input.ngc Test_output.ngc
```

The above example will wrap the toolpaths contained in Test_input.ngc around a
1.592 diameter workpiece. The results will be written to Test_output.ngc. Note
that there's no explicit notion of units. The unit could be inches or mm,
depending on your G code interpreter's defaults and any G20 or G21 commands.


Details
-------

This tool will swap the Y axis to A axis in a G code program. This is useful for
wrapping 2.5D G code programs around a rotary axes.

This program partially handles feedrate (F word) scaling. F words are
interpretted as the pythagorean mean of feedrates of all axes. This is fine when
only linear axes are concerned, but is incorrect if you have a rotary axis. For
example, 1 inch per second usually does not equal to 1 degree per second. If F
words are not scaled, the result is usually unbearably slow G code. This program
handles F word scaling, but it is not numerically accurate. For most cases, the
result is close enough and doesn't matter.

All toolpaths in your code must be linear (i.e. G0 and G1, no G2 and G3). Most
CAM software have an option to do this.

This program does all its parsing conversion through a bunch of regular
expressions.

Future improvements should include:
* Numerically correct F word scaling
* GUI
* Abitrary axes to axes swap
* Handling of circular toolpaths (G2 and G3)
