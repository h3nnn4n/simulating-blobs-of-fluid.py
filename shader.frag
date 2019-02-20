varying vec4 v_color;
uniform vec2 particle_pos[100];

void main() {
    // gl_FragColor = vec4(particle_pos[0].x, particle_pos[0].y, particle_pos[1].x, 1);
    gl_FragColor = v_color;
}