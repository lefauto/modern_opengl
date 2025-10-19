from OpenGL.GL import *

def setup_geometry(vertices):
    vao = glGenVertexArrays(1) # cria array (cartao de instruções de como ler os dados)
    vbo = glGenBuffers(1) # cria buffer (caixa que guarda os dados)
    
    glBindVertexArray(vao) # vincula a array
    
    glBindBuffer(GL_ARRAY_BUFFER, vbo) # define tipo de buffer, esse vincula os vértices (buffer de vértices)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW) # preenche o buffer com os dados dos vértices

    glEnableVertexAttribArray(0) # habilita o uso de "x" atributos (0 = posição)
    glVertexAttribPointer(
    0, # just vertex information, attribute index is 0
    2, # size (2 components per vertex, e.g., x, y)
    GL_FLOAT, # type of data
    GL_FALSE, # not normalized
    8, # stride (2 floats * 4 bytes (per float) = 8 bytes)
    None # offset (None or 0 for start of buffer, others need ‘pad’)
    ) # configura a array
    return vao, vbo