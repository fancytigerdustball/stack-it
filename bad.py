''' Bar Alignment Dropper (BAD)

AI that waits until the bars are align, and than drops the bar 

It got 204 points?! '''

from time import perf_counter as clock
from engine import *
import pygame as pg

eng = Eng()
space = False
winrect = win.get_rect()

# RGB of window coordinate
get_at = lambda x, y: win.get_at((x, y))[:3]

# Figure out the background color
eng.draw_screen()
bg_color = get_at(0, winrect.height - 1)
# Figure out the block color
for x in range(winrect.width):
    color = get_at(x, winrect.height - 1)
    if color != bg_color:
        bar_color = color[:]
        break

last_dropped = clock()
while True:
    for event in pg.event.get():
        if (event.type == pg.QUIT or
        (event.type == pg.KEYDOWN and event.key == pg.K_q)):
            eng.stop()

    space = False
    for x in range(winrect.width - 1):
        if get_at(x, winrect.height - 1) == bar_color:
            # Check if bars are aligned
            for i in range(0, (clock() - last_dropped).__floor__()): # Allows more error for how long bar has not been dropped
                if get_at(x - (1 + i), 0) == bar_color and get_at(x - (2 + i), 0) == bg_color:
                    space = True
            if space:
                last_dropped = clock()
            break
            
    eng.loop(space)