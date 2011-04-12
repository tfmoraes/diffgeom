#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import math
import random

import numpy
import pygtk
pygtk.require('2.0')

import gtk

from gtk import gdk

RADIUS = 2.0

LAMBDA = 0.63
MU = -0.67

class Polygon(object):
    def __init__(self, points):
        self.points = points

    def add_point(self, p):
        self.points.append(p)

    def _calculate_points(self, w, h):
        self.point_to_draw = [(i*w, j*h) for i, j in self.points]

    def smooth(self, steps, lambda_):
        new_points = copy.deepcopy(self.points)
        n = len(new_points)
        for step in xrange(steps):
            dv = {}
            for vi in xrange(n):
                dv[vi] = self._calculate_dvi(new_points, vi) 

            for vi in xrange(n):
                new_points[vi][0] += dv[vi][0] * lambda_
                new_points[vi][1] += dv[vi][1] * lambda_

        return Polygon(new_points)

    def taubin_smooth(self, steps, lambda_, mu):
        new_points = copy.deepcopy(self.points)
        n = len(new_points)
        for step in xrange(steps):
            dv = {}
            for vi in xrange(n):
                dv[vi] = self._calculate_dvi(new_points, vi) 

            for vi in xrange(n):
                new_points[vi][0] += dv[vi][0] * lambda_
                new_points[vi][1] += dv[vi][1] * lambda_

            for vi in xrange(n):
                dv[vi] = self._calculate_dvi(new_points, vi) 

            for vi in xrange(n):
                new_points[vi][0] += dv[vi][0] * mu
                new_points[vi][1] += dv[vi][1] * mu

        return Polygon(new_points)

    def _calculate_dvi(self, points, vi):
        n = len(points)
        x = 0.5 * (points[(vi - 1)%n][0] - points[vi][0]) + \
                0.5 * (points[(vi + 1)%n][0] - points[vi][0]) 
        y = 0.5 * (points[(vi - 1)%n][1] - points[vi][1]) + \
                0.5 * (points[(vi + 1)%n][1] - points[vi][1]) 
        return x, y

    def calculate_vectors(self):
        n = len(self.points)
        vectors = []
        for vi in xrange(n):
            vectors.append(self._calculate_dvi(self.points, vi))
        return vectors



class PolygonDrawer(gtk.DrawingArea):
    def __init__(self, polygon):
        gtk.DrawingArea.__init__(self)
        self.connect("expose_event", self.expose)
        self.connect("button_press_event", self.button_click)

        self.add_events(gdk.BUTTON_PRESS_MASK |
                        gdk.BUTTON_RELEASE_MASK |
                        gdk.POINTER_MOTION_MASK)

        self.polygon = polygon
        self._show_vectors = False

    def set_polygon(self, polygon):
        self.polygon = polygon
        self.queue_draw()

    def show_vectors(self, value):
        self._show_vectors = value
        self.queue_draw()

    def _calculate_points(self, points, w, h):
         return [(i*w, j*h) for i, j in points]

    def expose(self, widget, event):
        self.context = widget.window.cairo_create()
        self.context.rectangle(event.area.x, event.area.y, event.area.width, event.area.height)
        self.context.clip()
        self.draw(self.context, event.area.width, event.area.height)

        return False

    def button_click(self, widget, event):
        w, h = self.window.get_size()
        x, y = event.x, event.y

        self.polygon.add_point([x / float(w), y / float(h)])

        rect = self.get_allocation()
        self.window.invalidate_rect(rect, True)
        self.window.process_updates(True)

    def draw(self, ctx, w, h):
        ctx.set_source_rgb(1, 1, 1)
        ctx.rectangle(0, 0, w, h)
        ctx.fill()
        ctx.set_source_rgb(0, 0, 0)
        ctx.stroke()
        ctx.set_line_width(2)
        if self.polygon and self.polygon.points:
            vertices = self._calculate_points(self.polygon.points, w, h)
            for x,y in vertices:
                self._draw_point(ctx, x, y)

            #ctx.set_line_width(0.5)
            ctx.move_to(*vertices[0])
            for x,y in vertices:
                ctx.line_to(x, y)
            ctx.line_to(*vertices[0])
            ctx.stroke()

            if self._show_vectors:
                ctx.set_source_rgb(1, 0, 0)
                vectors = self._calculate_points(self.polygon.calculate_vectors(), w, h)
                for n, v in enumerate(vertices):
                    ctx.move_to(*v)
                    ctx.line_to(vectors[n][0] + v[0], vectors[n][1] + v[1])
                ctx.stroke()

    def _draw_point(self, ctx, x, y):
        ctx.arc(x, y, RADIUS, 0.0, 2 * math.pi)
        ctx.fill()


class MainWindow(gtk.Window):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.polygon = Polygon([])
        self.polygon_drawer = PolygonDrawer(self.polygon)
        self.smoothed_polygon_drawer = PolygonDrawer(None)
        self.taubin_smoothed_polygon_drawer = PolygonDrawer(None)

        self.steps = gtk.HScale()
        self.steps.set_range(1, 100)
        self.steps.set_digits(0)

        self.lambda_ = gtk.HScale()
        self.lambda_.set_range(0, 1)
        self.lambda_.set_digits(3)
        self.lambda_.set_value(LAMBDA)

        self.mu = gtk.HScale()
        self.mu.set_range(-1, 0)
        self.mu.set_digits(3)
        self.mu.set_value(MU)

        button = gtk.Button("Smooth")
        button.connect("clicked", self.do_smooth_and_draw)

        bvectors = gtk.Button("Draw vectors")
        bvectors.connect("clicked", self.do_show_vectors)

        hlayout = gtk.HBox(True, 5)
        hlayout.pack_start(self.polygon_drawer, True, True, 5)
        hlayout.pack_start(self.smoothed_polygon_drawer, True, True, 5)
        hlayout.pack_start(self.taubin_smoothed_polygon_drawer, True, True, 5)

        hlayout2 = gtk.HBox(True, 5)
        hlayout2.pack_start(self.steps, False, True, 5)
        hlayout2.pack_start(self.lambda_, False, True, 5)
        hlayout2.pack_start(self.mu, False, True, 5)
        hlayout2.pack_start(button, False, True, 5)
        hlayout2.pack_start(bvectors, False, True, 5)

        main_layout = gtk.VBox(False, 5)
        main_layout.pack_start(hlayout, True, True, 5)
        main_layout.pack_start(hlayout2, False, True, 5)

        self.add(main_layout)
        self.connect("delete-event", gtk.main_quit)
        self.set_size_request(500, 500)
        self.show_all()

    def do_smooth_and_draw(self, widget):
        steps = int(self.steps.get_value())
        lambda_ = self.lambda_.get_value()
        mu = self.mu.get_value()

        new_polygon = self.polygon.smooth(steps, lambda_)
        self.smoothed_polygon_drawer.set_polygon(new_polygon)

        taubin_new_polygon = self.polygon.taubin_smooth(steps, lambda_, mu)
        self.taubin_smoothed_polygon_drawer.set_polygon(taubin_new_polygon)

    def do_show_vectors(self, widget):
        self.polygon_drawer.show_vectors(True)
        self.smoothed_polygon_drawer.show_vectors(True)
        self.taubin_smoothed_polygon_drawer.show_vectors(True)

def main():
    window = MainWindow()
    gtk.main()

if __name__ == '__main__':
    main()
