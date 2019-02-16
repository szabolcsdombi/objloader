'''
    This is a testbed for various "objloader"'s features.

    Uses objloader itself together with ModenGL package and "example_window.py" Qt facilitator.

    For contributing code see: https://github.com/cprogrammer1994/ModernGL/tree/master/examples

    This example's "Render" function deliberately uses non-refactored code.
    
    adopted by: Alex Zakrividoroga
'''

import os
import moderngl
from objloader import Obj
from PIL import Image
from pyrr import Matrix44, Vector3, vector, Quaternion
import numpy as np

from example_window import Example, run_example


class LoadingOBJ(Example):
    def __init__(self):
        self.ctx = moderngl.create_context()

        self.obj = Obj.open(os.path.join(os.path.dirname(__file__), 'data', 'viper.obj'))
        self.wood = Image.open(os.path.join(os.path.dirname(__file__), 'data', 'viper.png'))

        self.prog = self.ctx.program(
            vertex_shader='''
                #version 330

                uniform mat4 Mvp;

                in vec3 in_vert;
                in vec3 in_norm;
                in vec2 in_text;

                out vec3 v_vert;
                out vec3 v_norm;
                out vec2 v_text;

                void main() {
                    v_vert = in_vert;
                    v_norm = in_norm;
                    v_text = in_text;
                    gl_Position = Mvp * vec4(v_vert, 1.0);
                }
            ''',
            fragment_shader='''
                #version 330

                uniform sampler2D Texture;
                uniform vec4 Color;
                uniform vec3 Light;

                in vec3 v_vert;
                in vec3 v_norm;
                in vec2 v_text;

                out vec4 f_color;

                void main() {
                    float lum = dot(normalize(v_norm), normalize(v_vert - Light));
                    lum = acos(lum) / 3.14159265;
                    lum = clamp(lum, 0.0, 1.0);
                    lum = lum * lum;
                    lum = smoothstep(0.0, 1.0, lum);
                    lum *= smoothstep(0.0, 80.0, v_vert.z) * 0.3 + 0.7;
                    lum = lum * 0.8 + 0.2;

                    vec3 color = texture(Texture, v_text).rgb;
                    color = color * (1.0 - Color.a) + Color.rgb * Color.a;
                    f_color = vec4(color * lum, 1.0);
                }
            ''',
        )

        self.light = self.prog['Light']
        self.color = self.prog['Color']
        self.mvp = self.prog['Mvp']

        self.texture = self.ctx.texture(self.wood.size, 3, self.wood.tobytes())
        self.texture.build_mipmaps()

        self.vbo = self.ctx.buffer(self.obj.pack('vx vy vz nx ny nz tx ty'))
        self.vao = self.ctx.simple_vertex_array(self.prog, self.vbo, 'in_vert', 'in_norm', 'in_text')

    def render(self):
        width, height = self.wnd.size
        self.ctx.viewport = self.wnd.viewport
        self.ctx.clear(1.0, 1.0, 1.0)
        self.ctx.enable(moderngl.DEPTH_TEST)

        _field_of_view_degrees = 30.0
        _z_near = 0.1
        _z_far = 100
        _screen_ratio = width / height

        #building proj matrix
        proj = Matrix44.perspective_projection(
            _field_of_view_degrees,
            _screen_ratio,
            _z_near,
            _z_far)

        #deciding where, once built, to position the camera: 
        _move_camera_y = 7      #up
        _move_camera_x = 5      #"left"

        #deciding how, once built, to yaw the camera (left, right):
        _rotate_camera_horizontally_deg = -24 #rotating "right"
        _rotate_camera_horizontally_rad = float(_rotate_camera_horizontally_deg) * np.pi / 180
        _rotation_horizontal_quat = Quaternion.from_y_rotation(_rotate_camera_horizontally_rad) 

        #deciding how, once built, to pitch the camera (up, down):
        _rotate_camera_vertically_deg = -40  #rotating "down"
        _rotate_camera_vertically_rad = float(_rotate_camera_vertically_deg) * np.pi / 180
        _rotation_vertical_quat = Quaternion.from_x_rotation(_rotate_camera_vertically_rad)   

        #building camera position matrix 
        _camera_front = (
            _rotation_vertical_quat *
            _rotation_horizontal_quat *                                     #Rotating camera right
            Vector3 ([0.0, 0.0, -1.0]))                                     #Camera's actual front vector
        
        _camera_up = Vector3 ([0.0, 1.0, 0.0])
        
        _camera_position = (
            Vector3 ([0.0, 0.0, 10.0]) +                                    #Camera's actual position vector
            _camera_up * _move_camera_y -                                   #Shifting camera's position up
            vector.normalize(_camera_front ^ _camera_up) * _move_camera_x   #Shifting camera's position "left"
            )

        #look at matrix
        _cameras_target = _camera_position + _camera_front
        lookat = Matrix44.look_at(
            _camera_position,
            _cameras_target,
            _camera_up)

        self.light.value = (-140.0, -300.0, 350.0)
        self.color.value = (1.0, 1.0, 1.0, 0.25)
        self.mvp.write((proj * lookat).astype('f4').tobytes())

        self.texture.use()
        self.vao.render()


run_example(LoadingOBJ)
