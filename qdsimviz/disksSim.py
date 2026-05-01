"""
A simulation of disks bouncing around in a page.
"""

from .disk import Disk
from .page import Page
import numpy as np
import wassilypy
import H5Gizmos as gz
import time
import asyncio

def randomRGBString():
    r = np.random.randint(0, 256)
    g = np.random.randint(0, 256)
    b = np.random.randint(0, 256)
    return f"rgb({r}, {g}, {b})"

class DisksSim:

    width = 1000
    height = 1000
    min_radius = 10
    max_radius = 80
    min_speed = 10
    max_speed = 60
    max_dots = 10
    sim_running = False
    last_update_time = None
    gravity = False
    gravitational_constant = 100.0
    earth = False
    earth_acceleration = 100.0

    def __init__(self):
        self.border = self.make_border()
        self.dots = []
        for _ in range(self.max_dots):
            self.dots.append(self.make_dot())

    def make_border(self):
        return Page(self.width, self.height)

    def make_dot(self):
        radius = np.random.uniform(self.min_radius, self.max_radius)
        xy = np.random.uniform(radius, self.width - radius, size=2)
        speed = np.random.uniform(self.min_speed, self.max_speed)
        angle = np.random.uniform(0, 2 * np.pi)
        velocity = speed * np.array((np.cos(angle), np.sin(angle)))
        disk = Disk(xy, velocity, radius)
        return disk
    
    def update(self, dt):
        for disk in self.dots:
            disk.move(dt)
            disk.boundary_bounce(self.border)
        for i in range(len(self.dots)):
            for j in range(i + 1, len(self.dots)):
                if self.dots[i].collides_with(self.dots[j]):
                    #print(f"Collision between disk {i} and disk {j}")
                    self.dots[i].bounce(self.dots[j])
        if self.gravity:
            for i in range(len(self.dots)):
                for j in range(i + 1, len(self.dots)):
                    self.dots[i].gravity(self.dots[j], dt, G=self.gravitational_constant)
        if self.earth:
            for dot in self.dots:
                dot.velocity[1] += self.earth_acceleration * dt

    async def sync_display(self):
        # xxx this should be a basic feature of H5Gizmos, not something we have to do manually in the sim
        gizmo = self.frame.on_diagram.gizmo
        reconnect_id = gizmo.H5GIZMO_INTERFACE.reconnect_id
        got_id = await gz.get(reconnect_id)
        #print (f"Got reconnect id: {got_id}")
        return got_id

    async def display(self):
        diagram = wassilypy.Diagram(self.width, self.height)
        startButton = gz.Button("Start").set_on_click(self.toggle_start)
        gravityButton = gz.Button("Gravity").set_on_click(self.toggle_gravity)
        earthButton = gz.Button("Earth").set_on_click(self.toggle_earth)
        self.startButton = startButton
        self.gravityButton = gravityButton
        self.earthButton = earthButton
        dashboard = gz.Stack([
            diagram,
            startButton,
            gravityButton,
            earthButton,
        ])
        await dashboard.link()
        #frame = diagram.mainFrame
        #self.frame = frame
        self.set_geometry(diagram)
        dot_marks = []
        for dot in self.dots:
            #circle = frame.circle(disk.xy, disk.radius).colored(randomRGBString())
            mark = self.mark(dot.pos, dot.radius)
            dot_marks.append([dot, mark])
        self.dot_marks = dot_marks

    def set_geometry(self, diagram):
        self.frame = diagram.mainFrame

    def mark(self, location, radius):
        return self.frame.circle(location, radius).colored(randomRGBString())

    def toggle_earth(self, *ignored):
        self.earth = not self.earth
        if self.earth:
            self.earthButton.text("No Earth")
        else:
            self.earthButton.text("Earth")

    def toggle_gravity(self, *ignored):
        self.gravity = not self.gravity
        if self.gravity:
            self.gravityButton.text("No Gravity")
        else:
            self.gravityButton.text("Gravity")

    def toggle_start(self, *ignored):
        if self.sim_running:
            self.sim_running = False
            self.startButton.text("Start")
        else:
            self.startButton.text("Stop")
            gz.schedule_task(self.run_simulation())

    async def run_simulation(self):
        if self.sim_running:
            return
        try:
            self.sim_running = True
            self.last_update_time = time.time()
            self.startButton.text("Stop")
            while self.sim_running:
                # sleep for a short time to avoid blocking the event loop
                await asyncio.sleep(0.03)
                current_time = time.time()
                dt = current_time - self.last_update_time
                self.last_update_time = current_time
                self.update(dt)
                self.update_positions()
                await self.sync_display()
        finally:
            self.sim_running = False
            self.startButton.text("Start")

    def update_positions(self):
        for dot, mark in self.dot_marks:
            mark.centerAt(dot.pos)
