#version 330 core

// Coordenadas de Vértice
layout (location = 0) in vec3 aPos;

// Coordenadas de Textura
layout (location = 1) in vec3 aColor;
layout (location = 2) in vec2 aTexCoord;

// Passa as coordenadas para o Fragment Shader
out vec3 vColor;
out vec2 UV;

void main()
{
    gl_Position = vec4(aPos, 1.0);
    vColor = aColor;
    UV = aTexCoord;
}