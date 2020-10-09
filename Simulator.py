import pygame as pg
from pygame.locals import *
import physics as phy


# the whole program as main() function
def main():
    # initialize pygame
    pg.init()

    # creating window
    LOGO = pg.image.load('logo.png')
    pg.display.set_icon(LOGO)
    pg.display.set_caption('Planetary Motion Simulator')

    SCREENWIDTH = 800
    SCREENHEIGHT = 800
    DISPLAY = pg.display.set_mode((SCREENWIDTH, SCREENHEIGHT))

    # draw functions
    def draw_vectors(vectors, display, width=5):
        if hasattr(vectors, '__iter__'):
            for i in range(len(vectors)):
                try:
                    vector, color = vectors[i]
                except:
                    raise ValueError('Please provide tuples of the vectors and their respective colors')
                
                pg.draw.line(display, color, (int(vector.x1()), 10*int(vector.y1())), (int(vector.x2()), 10*int(vector.y2())), width)
        else:
            raise ValueError('Please provide an iteratable for the \'vectors\' parameter')

    def draw_bodies(bodies, display):
        if hasattr(bodies, '__iter__'):
            for body in bodies:
                try:
                    display.blit(body.image, (int(body.x), int(body.y)))                
                except:
                    pg.draw.circle(display, body.color, (int(body.x), int(body.y)), int(body.radius))
        else:
            raise TypeError('Please provide an iterable containing the given \'Body objects\'')

    # simulation parameters
    FPS = 1
    FPS_CLOCK = pg.time.Clock()
    DT_PERFRAME = 0.0000000000000000000000001
    
    # simulation objects
    img_earth = pg.image.load('earth.png')
    EARTH = phy.Body(100000, 20, (0, 0, 255), 100, 250, 50, 50, [], img_earth)

    img_sun = pg.image.load('sun.png')
    SUN = phy.Body(999999, 100, (255, 200, 0), 200, 500, 1, 1, [], img_sun)

    # the main (infinite) game loop
    while True:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()

        pg.draw.rect(DISPLAY, (255, 255, 255), (0, 0, SCREENWIDTH, SCREENHEIGHT))
        
        draw_vectors([(EARTH.netForce(), (0, 0, 0)), (SUN.netForce(), (0, 0, 0))], DISPLAY)
        #draw_bodies([EARTH, SUN], DISPLAY)

        EARTH.applyForces([EARTH.get_gForce([SUN], 'polar')])
        SUN.applyForces([SUN.get_gForce([EARTH], 'polar')])

        pg.display.update()

        EARTH.move('xy', DT_PERFRAME)
        SUN.move('xy', DT_PERFRAME)

        FPS_CLOCK.tick(FPS)

if __name__ == '__main__':
    main()
