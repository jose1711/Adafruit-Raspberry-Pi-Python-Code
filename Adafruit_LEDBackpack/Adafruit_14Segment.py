#!/usr/bin/python

import time
import datetime
from Adafruit_LEDBackpack import LEDBackpack

# ===========================================================================
# 14-Segment Display
# ===========================================================================

#   11111111111111
# 32           1  2
# 32  2   5   0   2
# 32   5  1  2    2
# 32    6 2 4     2
#     64      128
# 16    2 4 8     4
# 16   0  0  1    4
# 16  4   9   9   4
# 16 8    6    2  4
#   88888888888888   16384


# This class is meant to be used with the four-character, fourteen segment
# displays available from Adafruit

class FourteenSegment:
  disp = None
 
  # Hexadecimal character lookup table (row 1 = 0..9, row 2 = A..F)
  digits = [ 0x3F, 0x06, 0xDB, 0xCF, 0xE6, 0xED, 0xFD, 0x07, 0xFF, 0xEF, \
             0xF7, 0xFC, 0x39, 0xDE, 0x79, 0x71 ]

  # Constructor
  def __init__(self, address=0x70, debug=False):
    if (debug):
      print "Initializing a new instance of LEDBackpack at 0x%02X" % address
    self.disp = LEDBackpack(address=address, debug=debug)

  def writeDigitRaw(self, charNumber, value):
    "Sets a digit using the raw 16-bit value"
    if (charNumber > 7):
      return
    # Set the appropriate digit
    self.disp.setBufferRow(charNumber, value)

  def writeDigit(self, charNumber, value, dot=False):
    "Sets a single decimal or hexademical value (0..9 and A..F)"
    if (charNumber > 7):
      return
    if (value > 0xF):
      return
    # Set the appropriate digit
    self.disp.setBufferRow(charNumber, self.digits[value] | (dot << 14))

  def setColon(self, state=True):
    "Enables or disables the colon character"
    # Warning: This function assumes that the colon is character '2',
    # which is the case on 4 char displays, but may need to be modified
    # if another display type is used
    if (state):
      self.disp.setBufferRow(2, 0x4000)
    else:
      self.disp.setBufferRow(2, 0)

