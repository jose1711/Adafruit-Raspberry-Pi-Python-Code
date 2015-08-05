#!/usr/bin/python

import time
import datetime
from Adafruit_14Segment import FourteenSegment

# ===========================================================================
# Clock Example
# ===========================================================================
segment = FourteenSegment(address=0x70)

print "Press CTRL+Z to exit"

# Continually update the time on a 4 char, 14-segment display
while(True):
  now = datetime.datetime.now()
  hour = now.hour
  minute = now.minute
  second = now.second
  # Set hours
  segment.writeDigit(0, int(hour / 10))     # Tens
  # Set minutes
  segment.writeDigit(2, int(minute / 10))   # Tens
  segment.writeDigit(3, minute % 10)        # Ones
  # Toggle colon
  if second % 2:
    segment.writeDigit(1, hour % 10, True)    # Ones, dot on
  else:
    segment.writeDigit(1, hour % 10)          # Ones, dot off
  # Wait one second
  time.sleep(1)
