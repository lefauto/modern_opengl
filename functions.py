from OpenGL.GL import *
import numpy as np
import math

def setup_geometry(vertices, attributes):
    # VBO
    vbo = glGenBuffers(1) # Cria
    glBindBuffer(GL_ARRAY_BUFFER, vbo) # Vincula
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW) # Envia

    # VAO
    vao = glGenVertexArrays(1) # Cria
    glBindVertexArray(vao) # Vincula

    stride = sum(attributes) * vertices.itemsize  # Total por vértice
    offset = 0
    for index, size in enumerate(attributes):
        glEnableVertexAttribArray(index)# Habilita VAO
        glVertexAttribPointer(
        index, # Índice do atributo
        size, # Número de componentes por vértice
        GL_FLOAT, # Tipo dos dados
        GL_FALSE, # Normalização
        stride, # Stride (tam. de cada vértice em byes)
        ctypes.c_void_p(offset) # Offset (onde começa o primeiro valor)
        ) # Configura
        offset += size * vertices.itemsize

    #UNBINDING
    glBindBuffer(GL_ARRAY_BUFFER, 0) # Desvincula o VBO
    glBindVertexArray(0) # Desvincula o VAO
    return vao, vbo

def create_shader(shader_type, source): # Tipo, conteúdo/código
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)
    return shader

def create_translation(tx, ty, tz):
    return np.array([[1.0, 0.0, 0.0, tx],
                     [0.0, 1.0, 0.0, ty],
                     [0.0, 0.0, 1.0, tz],
                     [0.0, 0.0, 0.0, 1.0]], dtype=np.float32)

def create_scale(sx, sy, sz):
    return np.array([[sx, 0.0, 0.0, 0.0],
                     [0.0, sy, 0.0, 0.0],
                     [0.0, 0.0, sz, 0.0],
                     [0.0, 0.0, 0.0, 1.0]], dtype=np.float32)

def create_rotation(angle_degrees):
    angle_radians = math.radians(angle_degrees)
    cos_a = math.cos(angle_radians)
    sin_a = math.sin(angle_radians)
    return np.array([[cos_a, -sin_a, 0.0, 0.0],
                     [sin_a, cos_a, 0.0, 0.0],
                     [0.0, 0.0, 1.0, 0.0],
                     [0.0, 0.0, 0.0, 1.0]], dtype=np.float32)

def create_rotation3d(angle_degrees):
    angle_radians = math.radians(angle_degrees)
    cos_a = math.cos(angle_radians)
    sin_a = math.sin(angle_radians)
    return [np.array([[1.0, 0.0, 0.0, 0.0],
                     [0.0, cos_a, -sin_a, 0.0],
                     [0.0, sin_a, cos_a, 0.0],
                     [0.0, 0.0, 0.0, 1.0]], dtype=np.float32), # X axis 
            np.array([[cos_a, 0.0, sin_a, 0.0],
                     [0.0, 1.0, 0.0, 0.0],
                     [-sin_a, 0.0, cos_a, 0.0],
                     [0.0, 0.0, 0.0, 1.0]], dtype=np.float32), # Y axis
            np.array([[cos_a, -sin_a, 0.0, 0.0],
                     [sin_a, cos_a, 0.0, 0.0],
                     [0.0, 0.0, 1.0, 0.0],
                     [0.0, 0.0, 0.0, 1.0]], dtype=np.float32)] # Z axis

def get_view_matrix(camera_pos, camera_front, camera_up):
    #camera_front = camera_front - camera_pos
    z_axis = -camera_front / np.linalg.norm(camera_front)

    x_axis = np.cross(camera_up, z_axis)
    x_axis = x_axis / np.linalg.norm(x_axis)

    y_axis = np.cross(z_axis, x_axis)
    
    # Create view matrix (transpose)
    return np.array([[x_axis[0], y_axis[0], z_axis[0], 0], #s u f
                     [x_axis[1], y_axis[1], z_axis[1], 0], 
                     [x_axis[2], y_axis[2], z_axis[2], 0], 
                     [-np.dot(x_axis, camera_pos), -np.dot(y_axis, camera_pos), -np.dot(z_axis, camera_pos), 1]], dtype=np.float32)

def get_projection_matrix(fov, aspect_ratio, near, far):
    f = 1.0 / math.tan(math.radians(fov) / 2.0)
    proj = np.zeros((4, 4), dtype=np.float32)
    # Create projection matrix (transpose)
    proj[0, 0] = f / aspect_ratio
    proj[1, 1] = f
    proj[2, 2] = (far + near) / (near - far)
    proj[2, 3] = -1.0
    proj[3, 2] = (2.0 * far * near) / (near - far)
    return proj
