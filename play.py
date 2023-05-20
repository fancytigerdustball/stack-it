''' Module for playing stack it '''

from constants import *
from engine import *
import pygame as pg

eng = Eng()
space = False

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            eng.stop()

        elif event.type == pg.KEYDOWN:
            # Check key presses
            if event.key == pg.K_q:
                eng.stop()
            elif event.key == pg.K_r:
                eng.start()
            elif event.key == pg.K_SPACE:
                space = True

        elif event.type == pg.KEYUP and event.key == pg.K_SPACE:
            # If key space released
            space = False
            
    eng.loop(space)
    if space:
        space = False
