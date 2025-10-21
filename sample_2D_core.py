import glfw
from OpenGL.GL import *
import numpy as np

from functions import *

import numpy as np

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
    window = glfw.create_window(800, 600, "Esqueleto OpenGL Core (2D)", None, None)
    if not window:
        glfw.terminate()
        print("Erro: Não foi possível criar a janela GLFW.")
        return

    # Torna o contexto da janela o contexto atual do thread
    glfw.make_context_current(window)

    # 3. Criação dos VAO/VBO e Shaders (Vertex + Frag)
    # 3.1 VAO/VBO
    # Dados do Triângulo (Posicionado à Esquerda)
    triangle_vertices = np.array([
                        # x, y, z       r, g, b
                        -0.7, -0.5, 0.0,    1.0, 0.0, 0.0, # Vértice 1
                        0.0, -0.5, 0.0,     0.0, 1.0, 0.0, # Vértice 2
                        -0.35, 0.5, 0.0,    0.0, 0.0, 1.0 # Vértice 3
                        ], dtype=np.float32)
    # Dados do Quadrado (Posicionado à Direita)
    square_vertices = np.array([
                        0.2, -0.5, 0.0,     1.0, 0.5, 0.2, # Triângulo 1 Vértice 1
                        0.7, -0.5, 0.0,     1.0, 0.5, 0.2, # Triângulo 1 Vértice 2
                        0.7, 0.5, 0.0,      1.0, 0.5, 0.2, # Triângulo 1 Vértice 3
                        0.2, -0.5, 0.0,     1.0, 0.5, 0.2, # Triângulo 2 Vértice 1
                        0.7, 0.5, 0.0,      1.0, 0.5, 0.2, # Triângulo 2 Vértice 2
                        0.2, 0.5, 0.0,      1.0, 0.5, 0.2 # Triângulo 2 Vértice 3
                        ], dtype=np.float32)

    
    vao_tri, vbo_tri = setup_geometry(triangle_vertices) # detalhes em functions.py
    vao_sq, vbo_sq = setup_geometry(square_vertices)
    
    # 3.2 Shaders
    with open('vertex_shader.glsl', 'r') as file:
        vshader = create_shader(GL_VERTEX_SHADER, file.read())
    with open('fragment_shader.glsl', 'r') as file:
        fshader = create_shader(GL_FRAGMENT_SHADER, file.read())

    # 3.3 Programa (shaders)
    program = glCreateProgram()
    glAttachShader(program, vshader)
    glAttachShader(program, fshader)
    glLinkProgram(program)

    #Espeficamos as operações de viewport
    glViewport(0, 0, 800, 600)

    # Define a cor de fundo da janela
    glClearColor(0.3, 0.3, 0.3, 1.0)

    # 4. Loop de Renderização Principal
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)

        # Definicao da matriz de projeção
        proj = np.identity(4, dtype=np.float32)
        
        # Vincular o programa (shaders) que fará as operações
        glUseProgram(program)

        # Envia a matriz de projeção para o shader

        # Enviar uModel_matrix para o Uniform na GPU (glUniformMatrix4fv)

        """ # >>> Espaço para o seu código de desenho aqui (Core) <<<
            # Vincular VAOs/VBOs dos seus desenhos """
        
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
