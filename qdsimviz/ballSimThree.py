"""
Ball simulation using three.js for 3D rendering.
"""

from .ballSim import BallSim
import H5Gizmos as gz
import numpy as np
from .ball import Ball

start_tag = """<div id='vis' style='width: %s; height: %s;'>
Loading three.js visualization...</div>"""

three_js = "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"
orbit_js = "https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"

class BallSimThree(BallSim):

    max_dots = 33

    def debug_make_dot(self):
        radius = 50
        xyz = np.array([0, 0, 0])
        velocity = np.array([0, 0, 0])
        ball = Ball(xyz, velocity, radius)
        return ball

    #make_dot = debug_make_dot

    def get_diagram(self):
        vis = gz.Html(start_tag % (self.width, self.height))
        vis.remote_js(three_js)
        vis.remote_js(orbit_js)
        return vis
    
    def set_geometry(self, diagram):
        element = diagram.proxy() # proxy to jQuery element for the diagram
        # clear the dom element
        element.html("")
        window_proxy = diagram.window_proxy()
        log = window_proxy.console.log
        log("Setting up three.js visualization", element)
        three = window_proxy.THREE
        log("Loaded three.js", three)
        camera = three.PerspectiveCamera.new(75, self.width / self.height, 0.1, 10000)
        log("Created camera", camera)
        #camera.position.z = 2
        camera.position.z = self.width * 2
        camera.position.y = self.height * 0.7
        camera.position.x = self.width * 1.2
        #camera.position.set(100, 100, 14)
        #camera.position.set(self.width * 1.2, self.height * 0.7, -self.width * 3)
        h = self.height
        lookAt = [h/2, h/2, h/2]
        #camera.lookAt(0, 0, 0)
        #camera.position.set(h * 1.2, h*0.7, -h * 3)
        camera.lookAt(*lookAt)
        #camera.lookAt(200, 200, 200)
        renderer = three.WebGLRenderer.new()
        log("Created renderer", renderer)
        renderer.setSize(self.width, self.height)
        element.append(renderer.domElement)
        #orbiter = three.OrbitControls.new(camera, renderer.domElement)
        sphereGeometry = three.SphereGeometry.new(1, 16, 16)
        #sphereMaterial = three.MeshBasicMaterial.new({"color": 0xffffff, "wireframe": True})
        # for debug just create a single mesh for the ball, we will switch to an instanced mesh later
        #sphere = three.Mesh.new(sphereGeometry, sphereMaterial)
        #log("Created sphere mesh", sphere)
        sphereMaterial = three.MeshLambertMaterial.new({"color": 0xffffff})
        #sphereMaterial.vertexColors = True
        maxdots = self.max_dots
        # instanced mesh for the balls
        mesh = three.InstancedMesh.new(sphereGeometry, sphereMaterial, maxdots)
        log("Created instanced mesh", mesh)
        scene = three.Scene.new()
        log("Created scene", scene)
        scene.background = three.Color.new(0x12171a)
        scene.add(mesh)
        # add lights
        ambientLight = three.AmbientLight.new(0x404040)
        scene.add(ambientLight)
        directionalLight = three.DirectionalLight.new(0xffffff, 0.5)
        directionalLight.position.set(-h, h, h*3)
        scene.add(directionalLight)
        # debug -- add a cube.
        material = three.MeshBasicMaterial.new({"color": 0x00ff00, "wireframe": True})
        geometry = three.BoxGeometry.new()
        cube = three.Mesh.new(geometry, material)
        log("cube", cube)
        cube.position.set(h/2, h/2, h/2)
        cube.scale.set(h, h, h)
        scene.add(cube)
        #scene.add(sphere)
        # save structures for later use
        self.three = three
        self.camera = camera
        self.renderer = renderer
        self.scene = scene
        self.mesh = mesh
        self.window_proxy = window_proxy
        self.log = log
        self.log("Three.js setup complete")
        self.colorize_instances()
        self.update_positions()
        #self.renderer.render(self.scene, self.camera)

    def mark(self, location, radius):
        # we will use an instanced mesh, so we don't create individual meshes for each ball
        return None

    def colorize_instances(self):
        ndots = len(self.dots)
        colors = np.random.random((ndots, 3)).astype(np.float32)
        scolors = (colors * 0.5 + 0.5).clip(0, 1) # make colors brighter
        three = self.three
        mesh = self.mesh
        mesh.instanceColor = three.InstancedBufferAttribute.new(scolors.flatten(), 3)
        mesh.instanceColor.needsUpdate = True
        #mesh.instanceColor.setUsage(three.DynamicDrawUsage)
        mesh.material.color.set(0xffffff)
        mesh.material.vertexColors = True
        mesh.material.needsUpdate = True

    def update_positions(self):
        ndots = len(self.dots)
        matrices = np.zeros((ndots, 4, 4), dtype=np.float32)  
        for i, dot in enumerate(self.dots):
            matrix = matrices[i]  # use the pre-allocated array
            # for debug hack the radius and position
            #dot.radius = 1
            #dot.pos = np.array([0, -1, 0])
            # end debug hack
            matrix[0, 0] = dot.radius
            matrix[1, 1] = dot.radius
            matrix[2, 2] = dot.radius
            matrix[3, 0] = dot.pos[0]
            matrix[3, 1] = dot.pos[1]
            matrix[3, 2] = dot.pos[2]
            matrix[3, 3] = 1.0
        self.mesh.count = ndots
        self.mesh.instanceMatrix.set(matrices.flatten())
        self.mesh.instanceMatrix.needsUpdate = True
        log = self.log
        log("Updated positions for", ndots, "balls")
        self.renderer.render(self.scene, self.camera)
