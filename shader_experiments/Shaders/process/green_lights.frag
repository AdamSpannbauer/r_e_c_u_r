
varying vec2 v_texcoord;
uniform sampler2D u_tex0;
uniform vec2 u_resolution;
uniform float u_time;

void main() {
    vec2 pos = gl_FragCoord.xy;
    vec4 texColor = texture2D(u_tex0, v_texcoord);

    texColor.r *= (sin(0.05*pos.x - cos(u_time))       + cos(0.05*pos.x/(0.1 + abs(cos(u_time/5.0)))));
    texColor.r *= (sin(0.05*pos.y - cos(u_time/5.0)) + cos(0.05*pos.y/(0.1 + abs(cos(u_time/5.0)))));

    gl_FragColor = vec4(texColor.b, texColor.r, texColor.g, texColor.a);
}

