import glfw
from OpenGL.GL import *
import numpy as np

from functions import setup_geometry

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
    tri_vertices = np.array([
                -0.7, -0.5,
                0.0, -0.5,
                -0.35, 0.5,
                ], dtype=np.float32)
    # Dados do Quadrado (Posicionado à Direita)
    sq_vertices = np.array([
                0.2, -0.5,
                0.7, -0.5,
                0.7, 0.5,
                0.2, -0.5,
                0.7, 0.5,
                0.2, 0.5,
                ], dtype=np.float32) 

    
    vao_tri, vbo_tri = setup_geometry(tri_vertices) # detalhes em functions.py
    vao_sq, vbo_sq = setup_geometry(sq_vertices)
    
    # 3.2 Shaders

    # 3.3 Programa (shaders)

    #Espeficamos as operações de viewport
    glViewport(0, 0, 800, 600)

    # Define a cor de fundo da janela
    glClearColor(0.3, 0.3, 0.3, 1.0)

    # 4. Loop de Renderização Principal
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)

        #Definicao da matriz de projeção
        proj = np.identity(4, dtype=np.float32)
        
        """ # Vincular o programa (shaders) que fará as operações
        # Envia a matriz de projeção para o shader

        # >>> Espaço para o seu código de desenho aqui (Core) <<<
        # Vincular VAOs/VBOs dos seus desenhos
        # Chamadas de desenho das primitivas (usando programa/shader vinculado)

        # Desvincular VAOs/VBOs
        # Desvincular o programa (shaders) """ # Especificações para trabalhar na aula de 20/10
        
        glBindVertexArray(vao_tri) # Ativa o estado de leitura do Triângulo
        glDrawArrays(GL_TRIANGLES, 0, 3)
        glBindVertexArray(0) # desvincula
        
        glBindVertexArray(vao_sq) # Ativa o estado de leitura do Quadrado
        glDrawArrays(GL_TRIANGLES, 0, 6) # O quadrado tem 6 vértices (2 triângulos)
        glBindVertexArray(0) # desvincula


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

if __name__ == "__main__":
    main()
