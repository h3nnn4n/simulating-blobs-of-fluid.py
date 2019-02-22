varying vec4 v_color;
uniform vec4 gl_FragCoord;
uniform vec2 particle_pos[100];
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

void main() {
    int size = 100;
    bool is_close;

    for (int i = 0; i < size; i++) {
        is_close = closer_than(4.0, particle_pos[i]);

        if (is_close) {
            gl_FragColor = vec4(1, 0, 0, 1);
            return;
        }
    }

    gl_FragColor = vec4(0, 0, 0, 1);
}
