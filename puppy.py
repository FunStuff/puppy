#!/usr/bin/env python3

"""
Copyright (c) August Yip (http://august.hk/)
"""

import time
import curses

from curses import wrapper
import sys, traceback

from lib.core.data import config
from lib.source.yahoo import yahoo

def main() :

  try :
    stdscr.addstr(1,1, 'Loading...')
    stdscr.refresh()

    while True:

      stdscr.addstr(0, 0, 'puppy - version: 0.9.3.14159265')
      stdscr.addstr(1, 0, 'current data source: yahoo, last refresh: ' + time.strftime('%H:%M:%S'))

      quotes = yahoo.quotes()

      placeholder_str = '{symbol:10}{name:15}{price:6}{change:10}{percent:49}'

      columns = {
        'symbol' : 'Symbol',
        'name' : 'Name',
        'price' : 'Price'.rjust(6),
        'change' : 'Change'.rjust(10),
        'percent' : 'Percent'.rjust(10),
      }

      row = 3

      stdscr.addstr(row, 0, placeholder_str.format(**columns), curses.A_REVERSE)

      for q in quotes:
        row += 1

        data = {
          'symbol' : q['symbol'],
          'name' : q['Name'],
          'price' : q['LastTradePriceOnly'].rjust(6),
          'change' : q['Change'].rjust(10),
          'percent' : q['ChangeinPercent'].rjust(10)
        }

        stdscr.addstr(row, 0, placeholder_str.format(**data))
      stdscr.refresh()
      time.sleep(float(config['Default']['refresh']))

  finally :
    curses.endwin()

if __name__ == '__main__':

  try :

    # Initialize curses
    stdscr=curses.initscr()

    # Turn off echoing of keys, and enter cbreak mode,
    # where no buffering is performed on keyboard input
    curses.noecho()
    curses.cbreak()
    
    # In keypad mode, escape sequences for special keys
    # (like the cursor keys) will be interpreted and
    # a special value like curses.KEY_LEFT will be returned
    stdscr.keypad(1)
    wrapper(main())

    # Enter the main loop
    # Set everything back to normal
    stdscr.keypad(0)
    curses.echo()
    curses.nocbreak()
    curses.endwin()
    # Terminate curses

  except :

    # In event of error, restore terminal to sane state.
    stdscr.keypad(0)
    curses.echo()
    curses.nocbreak()
    curses.endwin()
    traceback.print_exc()
    # Print the exception
