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
    max_disks = 10
    sim_running = False
    last_update_time = None
    gravity = False
    gravitational_constant = 100.0

    def __init__(self):
        self.page = Page(self.width, self.height)
        self.disks = []
        for _ in range(self.max_disks):
            radius = np.random.uniform(self.min_radius, self.max_radius)
            xy = np.random.uniform(radius, self.width - radius, size=2)
            speed = np.random.uniform(self.min_speed, self.max_speed)
            angle = np.random.uniform(0, 2 * np.pi)
            velocity = speed * np.array((np.cos(angle), np.sin(angle)))
            disk = Disk(xy, velocity, radius)
            self.disks.append(disk)
    
    def update(self, dt):
        for disk in self.disks:
            disk.move(dt)
            disk.boundary_bounce(self.page)
        for i in range(len(self.disks)):
            for j in range(i + 1, len(self.disks)):
                if self.disks[i].collides_with(self.disks[j]):
                    #print(f"Collision between disk {i} and disk {j}")
                    self.disks[i].bounce(self.disks[j])
        if self.gravity:
            for i in range(len(self.disks)):
                for j in range(i + 1, len(self.disks)):
                    self.disks[i].gravity(self.disks[j], dt, G=self.gravitational_constant)

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
        self.startButton = startButton
        self.gravityButton = gravityButton
        dashboard = gz.Stack([
            diagram,
            startButton,
            gravityButton,
        ])
        await dashboard.link()
        frame = diagram.mainFrame
        self.frame = frame
        disk_circles = []
        for disk in self.disks:
            circle = frame.circle(disk.xy, disk.radius).colored(randomRGBString())
            disk_circles.append([disk, circle])
        self.disk_circles = disk_circles

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
                for disk, circle in self.disk_circles:
                    circle.centerAt(disk.xy)
                await self.sync_display()
        finally:
            self.sim_running = False
            self.startButton.text("Start")
