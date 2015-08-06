#!/usr/bin/python

import time
import datetime
import sys
from Adafruit_14Segment import FourteenSegment
from Adafruit_LEDBackpack import LEDBackpack

# ===========================================================================
# Ascii characters enumeration - tests all segments and LCD dimming
# ===========================================================================
lcd = LEDBackpack(address=0x70)
segment = FourteenSegment(address=0x70)
print "Press CTRL+Z to exit"

for pos in range(127):
  segment.writeChar(0,chr(pos))
  segment.writeChar(1,chr(pos))
  segment.writeChar(2,chr(pos))
  segment.writeChar(3,chr(pos))
  time.sleep(0.3)

byeword="Done     "
for pos in range(4):
  segment.writeChar(pos,byeword[pos])

# demoes dimming function
for level in range(16):
  lcd.setBrightness(level)
  time.sleep(0.3)

for level in reversed(range(16)):
  lcd.setBrightness(level)
  time.sleep(0.3)

# make byeword scroll away
for c in range(5):
  segment.writeChar(0,byeword[0])
  segment.writeChar(1,byeword[1])
  segment.writeChar(2,byeword[2])
  segment.writeChar(3,byeword[3])
  byeword=byeword[1:]
  time.sleep(0.3)
