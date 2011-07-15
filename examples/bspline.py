from __future__ import division
from pycurve import Bspline
import pygame
from pygame import display, draw, event, PixelArray, Rect, Surface
from pygame.locals import *


SCREEN_SIZE = (800, 600)
SCREEN = display.set_mode(SCREEN_SIZE)


STEP_N = 1000


################################################################################
def main():
    rect = Rect((0, 0), SCREEN_SIZE)
    surface = Surface(SCREEN_SIZE)
    pxarray = PixelArray(surface)
    P = [(0, 100), (100, 0), (200, 0), (300, 100), (400, 200), (500, 200),
         (600, 100), (400, 400), (700, 50), (800, 200)]
    n = len(P) - 1 # n = len(P) - 1; (P[0], ... P[n])
    k = 3          # degree of curve
    m = n + k + 1  # property of b-splines: m = n + k + 1
    _t = 1 / (m - k * 2) # t between clamped ends will be evenly spaced
    # clamp ends and get the t between them
    t = k * [0] + [t_ * _t for t_ in xrange(m - (k * 2) + 1)] + [1] * k

    S = Bspline(P, t, k)
    # insert a knot (just to demonstrate the algorithm is working)
    S.insert(0.9)

    step_size = 1 / STEP_N
    for i in xrange(STEP_N):
        t_ = i * step_size
        try: x, y = S(t_)
        # if curve not defined here (t_ is out of domain): skip
        except AssertionError: continue
        x, y = int(x), int(y)
        pxarray[x][y] = (255, 0, 0)
    del pxarray

    for p in zip(S.X, S.Y): draw.circle(surface, (0, 255, 0), p, 3, 0)
    SCREEN.blit(surface, (0, 0))

    while 1:
        for ev in event.get():
            if ev.type == KEYDOWN:
                if ev.key == K_q: exit()
        display.update()


if __name__ == '__main__':
    try:
        import psyco
        psyco.full()
    except ImportError: pass
    pygame.init()
    main()
