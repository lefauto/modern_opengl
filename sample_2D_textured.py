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
    window = glfw.create_window(800, 600, "Esqueleto OpenGL Core (2D)", None, None)
    if not window:
        glfw.terminate()
        print("Erro: Não foi possível criar a janela GLFW.")
        return

    # Torna o contexto da janela o contexto atual do thread
    glfw.make_context_current(window)

    # 3. Criação dos VAO/VBO e Shaders (Vertex + Frag)
    # 3.1 VAO/VBO
    # Dados do Quadrado com Textura
    square_vertices = np.array([
                        # Triângulo 1
                        0.5, 0.5, 0.0,   1.0, 0.5, 0.2,  1.0, 1.0, # Canto superior direito
                        0.5, -0.5, 0.0,  1.0, 0.5, 0.2,  1.0, 0.0, # Canto inferior direito
                        -0.5, -0.5, 0.0, 1.0, 0.5, 0.2,  0.0, 0.0, # Canto inferior esquerdo
                        # Triângulo 2
                        -0.5, -0.5, 0.0, 1.0, 0.5, 0.2,  0.0, 0.0, # Canto inferior esquerdo
                        -0.5, 0.5, 0.0,  1.0, 0.5, 0.2,  0.0, 1.0, # Canto superior esquerdo
                        0.5, 0.5, 0.0,   1.0, 0.5, 0.2,  1.0, 1.0 # Canto superior direito
                        ], dtype=np.float32)

    vao_sq, vbo_sq = setup_geometry(square_vertices, [3, 3, 2])

    # Carregamento da textura usando OpenCV
    image = cv2.imread("laranjas.jpg")
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.flip(image, 0)
    height, width, channels = image.shape

    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, image)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glBindTexture(GL_TEXTURE_2D, 0)


    # 3.2 Shaders
    with open('vertex_shader2.glsl', 'r') as file:
        vshader = create_shader(GL_VERTEX_SHADER, file.read())
    with open('fragment_shader2.glsl', 'r') as file:
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
        
    # Envia a valor da textura para o shader
    texture_loc = glGetUniformLocation(program, "frameColor")
    control_loc = glGetUniformLocation(program, "Control")
    
    # Vincular o programa (shaders) que fará as operações
    glUseProgram(program)

    # Enviar uModel_matrix para o Uniform na GPU (glUniformMatrix4fv)
    glUniform1i(texture_loc, 0) # Texture unit 0
    # glUniform1i(control_loc, 0) # Usar cores
    glUniform1i(control_loc, 1) # Usar textura
    
    # 4. Loop de Renderização Principal
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)

        # Definição da matriz de projeção
        proj = np.identity(4, dtype=np.float32)

        # Vincule o programa dentro do loop
        glUseProgram(program)
        
        # Bind da textura
        glActiveTexture(GL_TEXTURE0) # Ativa a unidade de textura 0
        glBindTexture(GL_TEXTURE_2D, texture_id) # lá do começo com glGenTextures

        # Desenha o quadrado
        glBindVertexArray(vao_sq)
        glDrawArrays(GL_TRIANGLES, 0, 6)

        # Unbind
        glBindTexture(GL_TEXTURE_2D, 0)
        glBindVertexArray(0)
        glUseProgram(0)

        # Verifica e processa eventos da janela
        glfw.poll_events()

        # Troca os buffers front e back para exibir a imagem renderizada
        glfw.swap_buffers(window)


    # 5. Finalização
    glfw.terminate()

    # Também será necessário limpar os VAOs/VBOs e Program/Shaders
    
    glDeleteVertexArrays(1, vao_sq)
    glDeleteBuffers(1, vbo_sq)
    glDeleteProgram(program)

if __name__ == "__main__":
    main()
