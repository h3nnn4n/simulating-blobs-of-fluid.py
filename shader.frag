#define INTENSITY 2.5
#define GLOW 2.0
#define BASE 20.0

varying vec4 v_color;
uniform vec4 gl_FragCoord;
uniform vec2 particle_pos[300];
uniform vec2 resolution;
uniform float particle_bouding_radius;

vec2 pixel_pos() {
    vec2 bounding_radius = vec2(particle_bouding_radius, particle_bouding_radius);
    vec2 positive_pos = gl_FragCoord.xy - (resolution / 2.0);
    return positive_pos * (bounding_radius / resolution) * 2.1;
}

bool closer_than(float cutover_distance, vec2 pos) {
    return distance(pos, pixel_pos()) < cutover_distance;
}

vec4 blob(vec2 uv, vec3 color) {
    float d = BASE / distance(uv, pixel_pos());
    d = pow(d / INTENSITY, GLOW);

    return vec4(color.r * d, color.g * d, color.b * d, 0);
}

vec4 threshold(vec4 color, float value){
    if (color.x <= value) {
        return vec4(1, 1, 1, 1);
    }

    return vec4(0, 0, 0, 1);
}

void main() {
    int size = 300;
    vec4 color = vec4(0, 0, 0, 1);

    for (int i = 0; i < size; i++) {
        color += blob(particle_pos[i], vec3(1, 0, 0));
    }

    gl_FragColor = threshold(color, 1.0);
}
