#version 330 core

layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aColor;

out vec3 vColor;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main()
{
    // Multiplica a MVP (4x4) pela posição (4x1) do vértice
    // O resultado é a posição no Clip Space (gl_Position)
    gl_Position = projection * view * model * vec4(aPos, 1.0);
    vColor = aColor;
}