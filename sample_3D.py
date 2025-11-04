import glfw
from OpenGL.GL import *
import numpy as np
import cv2

from functions import *

def main():
    # 1. Initialize GLFW
    if not glfw.init():
        print("Erro: Não foi possível inicializar o GLFW.")
        return

    # Request OpenGL Core Profile 3.3
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    # glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, glfw.TRUE)  # Uncomment if needed (MacOS)

    # 2. Criação da Janela de Aplicação
    window = glfw.create_window(800, 600, "Esqueleto OpenGL Core (3D)", None, None)
    if not window:
        glfw.terminate()
        print("Erro: Não foi possível criar a janela GLFW.")
        return

    # Torna o contexto da janela o contexto atual do thread
    glfw.make_context_current(window)

    # 3. Criação dos VAO/VBO e Shaders (Vertex + Frag)
    # 3.1 VAO/VBO
    # Dados do Triângulo (centralizado)
    # Estrutura: Posição (x, y, z) + Cor (r,g,b)
    triangle_vertices = np.array([
        -0.5, -0.5, -1.0, 1.0, 0.0, 0.0, #V1
        0.5, -0.5, -1.0, 0.0, 1.0, 0.0, #V2
        0.0, 0.5, -1.0, 0.0, 0.0, 1.0 #V3
    ], dtype=np.float32)

    # Dados do Quadrado (centralizado)
    # Usando cor sólida para todos os vértices
    square_vertices = np.array([
        -0.3, -0.3, -2.0, 1.0, 0.5, 0.2, # T1 V1
        0.3, -0.3, -2.0, 1.0, 0.5, 0.2, # T1 V2
        0.3, 0.3, -2.0, 1.0, 0.5, 0.2, # T1 V3
        -0.3, -0.3, -2.0, 1.0, 0.5, 0.2, # T2 V1
        0.3, 0.3, -2.0, 1.0, 0.5, 0.2, # T2 V2
        -0.3, 0.3, -2.0, 1.0, 0.5, 0.2 # T2 V3
    ], dtype=np.float32)

    vao_tri, vbo_tri = setup_geometry(triangle_vertices, [3, 3])
    vao_sq, vbo_sq = setup_geometry(square_vertices, [3, 3])

    # Matriz de modelo
    scale = create_scale(1.0, 1.0, 1.0)
    rotation = create_rotation3d(0)
    translation = create_translation(0.0, 0.0, 1.0)


    model = translation @ rotation @ scale # Aplique uma translação no eixo Z para trazer
    #model = np.identity(4, dtype=np.float32)


    # Posição da câmera
    eye = np.array([0.0, 0.0, 3.0], dtype=np.float32)
    # Para onde a câmera olha
    target = np.array([0.0, 0.0, -1.0], dtype=np.float32)
    # Vetor "para cima"
    up = np.array([0.0, 1.0, 0.0], dtype=np.float32)
    # Matriz de View
    view = get_view_matrix(eye, target, up)

    # Matriz de Projeção
    projection = get_projection_matrix(45.0, 800 / 600, 0.1, 100.0)
    """ projection_matrix = create_perspective(fov=45.0, # Graus
                                               aspect= aspect_ratio, # largura / altura (janela)
                                               near=0.1, # z-distance
                                               far=100.0 # z-distance
                                               ) """

    # 3.2 Shaders
    with open('vertex_shader3.glsl', 'r') as file:
        vshader = create_shader(GL_VERTEX_SHADER, file.read())
    with open('fragment_shader3.glsl', 'r') as file:
        fshader = create_shader(GL_FRAGMENT_SHADER, file.read())

    # 3.3 Programa (shaders)
    program = glCreateProgram()
    glAttachShader(program, vshader)
    glAttachShader(program, fshader)
    glLinkProgram(program)

    # Espeficamos as operações de viewport
    glViewport(0, 0, 800, 600)

    # Define a cor de fundo da janela
    glClearColor(0.3, 0.3, 0.3, 1.0)

    # Envia os valores das matrizes para o shader
    model_loc = glGetUniformLocation(program, "model")
    view_loc = glGetUniformLocation(program, "view")
    projection_loc = glGetUniformLocation(program, "projection")

    # Vincular o programa (shaders) que fará as operações
    glUseProgram(program)

    glEnable(GL_DEPTH_TEST)

    # 4. Loop de Renderização Principal
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Vincule o programa dentro do loop
        glUseProgram(program)

        # Enviando matrizes separadas para melhor ilustração
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, model.flatten())
        glUniformMatrix4fv(view_loc, 1, GL_FALSE, view.flatten())
        glUniformMatrix4fv(projection_loc, 1, GL_FALSE, projection.flatten())

        # Desenha o triângulo
        glBindVertexArray(vao_tri) 
        glDrawArrays(GL_TRIANGLES, 0, 3)
        glBindVertexArray(0)
        
        # Desenha o quadrado
        glBindVertexArray(vao_sq)
        glDrawArrays(GL_TRIANGLES, 0, 6)
        glBindVertexArray(0)

        # Desvincular o programa (shaders)
        glUseProgram(0)

        # Verifica e processa eventos da janela
        glfw.poll_events()

        # Troca os buffers front e back para exibir a imagem renderizada
        glfw.swap_buffers(window)


    # 5. Finalização
    glfw.terminate()

    # Também será necessário limpar os VAOs/VBOs e Program/Shaders
    
    glDeleteVertexArrays(1, vao_tri)
    glDeleteBuffers(1, vbo_tri)
    glDeleteVertexArrays(1, vao_sq)
    glDeleteBuffers(1, vbo_sq)
    glDeleteProgram(program)

if __name__ == "__main__":
    main()
