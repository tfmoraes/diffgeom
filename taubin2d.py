#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

    def smooth(self):
        new_points = self.points[:]
        n = len(new_points)
        for step in xrange(10):
            dv = {}
            for vi in xrange(new_points):
                dv[vi] = 0.5 * (new_points[(vi - 1)%n] - new_points[vi]) + \
                         0.5 * (new_points[(vi + 1)%n] - new_points[vi]) 

            for vi in xrange(new_points):
                new_points[vi] += dv[vi] * LAMBDA

            for vi in xrange(new_points):
                dv[vi] = 0.5 * (new_points[(vi - 1)%n] - new_points[vi]) + \
                         0.5 * (new_points[(vi + 1)%n] - new_points[vi]) 

            for vi in xrange(new_points):
                new_points[vi] += dv[vi] * MU

        return Polygon(new_points)



class PolygonDrawer(gtk.DrawingArea):
    def __init__(self, polygon):
        gtk.DrawingArea.__init__(self)
        self.connect("expose_event", self.expose)
        self.connect("button_press_event", self.button_click)

        self.add_events(gdk.BUTTON_PRESS_MASK |
                        gdk.BUTTON_RELEASE_MASK |
                        gdk.POINTER_MOTION_MASK)

        self.polygon = polygon

    def set_polygon(self, polygon):
        self.polygon = polygon

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
        if self.polygon and self.polygon.points:
            vertices = self._calculate_points(self.polygon.points, w, h)
            for x,y in vertices:
                self._draw_point(ctx, x, y)

            ctx.set_line_width(0.5)
            ctx.move_to(*vertices[0])
            for x,y in vertices:
                ctx.line_to(x, y)
            ctx.line_to(*vertices[0])
            ctx.stroke()

    def _draw_point(self, ctx, x, y):
        ctx.arc(x, y, RADIUS, 0.0, 2 * math.pi)
        ctx.fill()

def main():
    polygon = Polygon([])

    polygon_drawer = PolygonDrawer(polygon)
    smoothed_polygon_drawer = PolygonDrawer(None)

    scale = gtk.HScale()
    scale.set_range(1, 100)
    scale.set_digits(0)

    button = gtk.Button("Smooth")

    hlayout = gtk.HBox(True, 5)
    hlayout.pack_start(polygon_drawer, True, True, 5)
    hlayout.pack_start(smoothed_polygon_drawer, True, True, 5)

    hlayout2 = gtk.HBox(True, 5)
    hlayout2.pack_start(scale, False, True, 5)
    hlayout2.pack_start(button, False, True, 5)

    main_layout = gtk.VBox(False, 5)
    main_layout.pack_start(hlayout, True, True, 5)
    main_layout.pack_start(hlayout2, False, True, 5)

    window = gtk.Window()
    window.add(main_layout)
    window.connect("delete-event", gtk.main_quit)
    window.set_size_request(500, 500)
    window.show_all()

    gtk.main()

if __name__ == '__main__':
    main()
