#version 330 core

// A coordenada (U, V) INTERPOLADA
in vec3 vColor;
in vec2 UV;

// Cor de saída
out vec4 FragColor;

// Samplers
uniform sampler2D frameColor;

// Control
uniform int Control;

void main()
{
    if (Control == 1)
    {
        // Usa a textura
        FragColor = texture2D(frameColor, UV);
    }
    else
    {
        // Usa a cor do vértice
        FragColor = vec4(vColor, 1.0);
    }
}