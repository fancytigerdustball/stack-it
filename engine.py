''' Game engine for stack it '''

from constants import *
import pygame as pg

pg.font.init()
win = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Stack it!')
winrect = win.get_rect()
font = pg.font.Font(None, FONTSIZE)

class Bar:
    ''' Class for holding and moving bar coordinates '''
    def __init__(self):
        self.rect = pg.Rect(0, 0, BARWIDTH, BARHEIGHT)
        self.xmul = 1
        self.x = self.y = 0
        self.speed = STARTSPEED

    def update(self):
        ''' Move bar left or right '''
        self.x += self.speed * self.xmul
        self.rect.x = self.x
        if self.x < 0 or self.x + self.rect.width > WIDTH:
            # If gone past edge
            self.x -= self.speed * self.xmul
            self.rect.x = self.x
            self.speed *= -1

    def fall(self, eng):
        ''' Drop bar '''
        slits = []
        hits = 0
        # Break the bar down into slits that drop down the window
        for i in range(self.rect.width):
            slit = pg.Rect(self.rect.x + i, 0, 1, BARHEIGHT)
            slits.append(slit)
        while True:
            # Drop slits
            for slit in slits:
                slit.y += 1
                if slit.colliderect(eng.target):
                    slits.remove(slit)
                    hits += 1
                if slit.y > HEIGHT:
                    slits.remove(slit)

            if not slits:
                break
            eng.draw_screen(slits)

        self.rect.width = hits
        self.rect.topleft = (0, 0)
        self.x = 0

    def draw(self):
        ''' Draw bar on screen '''
        pg.draw.rect(win, (0, 0, 255), self.rect)

class Eng:
    ''' Engine '''
    def __init__(self):
        ''' Create game engine '''
        self.start()

    def start(self):
        ''' Initialize bars and score '''
        self.bar = Bar()
        self.target = Bar()
        self.target.rect.midbottom = winrect.midbottom
        self.score = 0

    def stop(self):
        ''' Quit game '''
        pg.quit()
        raise SystemExit(0)

    def loop(self, space):
        ''' Update bar and draw screen '''
        self.bar.update()
        if space:
            # Drop bar
            self.bar.fall(self)
            if not self.bar.rect.width:
                self.start()
            else:
                self.score += 1
            self.target.rect.width = self.bar.rect.width
            self.target.rect.midbottom = winrect.midbottom
        self.draw_screen()
        if self.bar.speed >= 0:
            self.bar.speed += SPEEDUP
        else:
            self.bar.speed -= SPEEDUP

    def draw_screen(self, slits=None):
        ''' Draw screen '''
        win.fill((0, 0, 0))
        fimage = font.render(f'Score: {self.score}', True, (255, 255, 255))
        win.blit(fimage, fimage.get_rect())
        fimage = font.render(f'Width: {self.bar.rect.width}', True, (255, 255, 255))
        frect = fimage.get_rect()
        frect.topright = winrect.topright
        win.blit(fimage, frect)
        if slits is not None:
            for slit in slits:
                pg.draw.rect(win, (0, 0, 255), slit)
        else:
            self.bar.draw()
        self.target.draw()
        pg.display.flip()


__all__ = ['Eng', 'win']
