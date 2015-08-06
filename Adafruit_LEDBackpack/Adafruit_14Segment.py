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

  chars = [
0x1,    #
0x2,    #
0x4,    #
0x8,    #
0x10,   #
0x20,   #
0x40,   #
0x80,   #
0x100,  #
0x200,  #
0x400,  #
0x800,  #
0x1000, #
0x2000, #
0x4000, #
0x8000, #
0x0,    #
0x0,    #
0x0,    #
0x0,    #
0x0,    #
0x0,    #
0x0,    #
0x0,    #
0x12c9, #
0x15c0, #
0x12f9, #
0xe3,   #
0x530,  #
0x12c8, #
0x3a00, #
0x1700, #
0x0,    # 
0x6,    # !
0x220,  # "
0x12ce, # #
0x12ed, # $
0xc24,  # %
0x235d, # &
0x400,  # '
0x2400, # (
0x900,  # )
0x3fc0, # *
0x12c0, # +
0x800,  # ,
0xc0,   # -
0x0,    # .
0xc00,  # /
0xc3f,  # 0
0x6,    # 1
0xdb,   # 2
0x8f,   # 3
0xe6,   # 4
0x2069, # 5
0xfd,   # 6
0x7,    # 7
0xff,   # 8
0xef,   # 9
0x1200, # :
0xa00,  # ;
0x2400, # <
0xc8,   # =
0x900,  # >
0x1083, # ?
0x2bb,  # @
0xf7,   # A
0x128f, # B
0x39,   # C
0x120f, # D
0xf9,   # E
0x71,   # F
0xbd,   # G
0xf6,   # H
0x1200, # I
0x1e,   # J
0x2470, # K
0x38,   # L
0x536,  # M
0x2136, # N
0x3f,   # O
0xf3,   # P
0x203f, # Q
0x20f3, # R
0xed,   # S
0x1201, # T
0x3e,   # U
0xc30,  # V
0x2836, # W
0x2d00, # X
0x1500, # Y
0xc09,  # Z
0x39,   # [
0x2100, #
0xf,    # ]
0xc03,  # ^
0x8,    # _
0x100,  # `
0x1058, # a
0x2078, # b
0xd8,   # c
0x88e,  # d
0x858,  # e
0x71,   # f
0x48e,  # g
0x1070, # h
0x1000, # i
0xe,    # j
0x3600, # k
0x30,   # l
0x10d4, # m
0x1050, # n
0xdc,   # o
0x170,  # p
0x486,  # q
0x50,   # r
0x2088, # s
0x78,   # t
0x1c,   # u
0x2004, # v
0x2814, # w
0x28c0, # x
0x200c, # y
0x848,  # z
0x949,  # {
0x1200, # |
0x2489, # }
0x520,  # ~
0x3fff  #
]

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

  def writeChar(self, charNumber, value, dot=False):
    "Writes an ascii character on the screen"
    if (charNumber > 7):
      return
    # Set the appropriate character
    self.disp.setBufferRow(charNumber, self.chars[ord(value)] | (dot << 14))


  def setColon(self, state=True):
    "Enables or disables the colon character"
    # Warning: This function assumes that the colon is character '2',
    # which is the case on 4 char displays, but may need to be modified
    # if another display type is used
    if (state):
      self.disp.setBufferRow(2, 0x4000)
    else:
      self.disp.setBufferRow(2, 0)

