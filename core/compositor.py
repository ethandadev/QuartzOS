"""
core/quartz_compositor.py

Manages the pygame display window and main render loop for Quartz OS.

"""
import pygame as pg
from display_utils import get_backing_scale_factor


class QuartzCompositor:
    def __init__(self, logical_width=1200, logical_height=800):
        """
        Initializes pygame and creates the display window.
        """
        pg.init()
        self.scale_factor = get_backing_scale_factor()
        self.logical_size = (logical_width, logical_height)
        self.flags = pg.SCALED | pg.RESIZABLE | pg.DOUBLEBUF
        self.screen = pg.display.set_mode(self.logical_size, flags=self.flags)
        self.clock = pg.time.Clock()
        self.is_running = True
        self.FPS = 60

    def handle_events(self):
        """
        Polls and handles pending pygame events (quit, resize).
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.is_running = False
            elif event.type == pg.VIDEORESIZE:
                new_w = max(400, event.w)
                new_h = max(300, event.h)
                self.logical_size = (new_w, new_h)
                self.screen = pg.display.set_mode(self.logical_size, self.flags)

    def render_frame(self):
        """
        Renders a single frame and flips the display buffer.
        """
        self.screen.fill((255, 255, 255))
        pg.display.flip()

    def run_loop(self):
        """
        Runs the main event/render loop until the window is closed.
        """
        while self.is_running:
            self.handle_events()
            self.render_frame()
            self.clock.tick(self.FPS)
        pg.quit()


if __name__ == "__main__":
    QuartzCompositor().run_loop()