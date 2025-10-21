from OpenGL.GL import *
import numpy as np
import math

def setup_geometry(vertices, attributes=[3, 3]):
    # VBO
    vbo = glGenBuffers(1) # Cria
    glBindBuffer(GL_ARRAY_BUFFER, vbo) # Vincula
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW) # Envia

    # VAO
    vao = glGenVertexArrays(1) #Cria
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