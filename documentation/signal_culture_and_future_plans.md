
# signal culture + future plans

this is an update on the progress and new ideas as a direct result of my residency at signal culture (sept-oct 2018) and an outline of some of my future plans with this project

the initial hack that became recur was in response to a specific hole in my video-hardware workflow (~dec2017). the incouragement and enthusism for the idea on VideoCircuits was enough to motivate me to tidy and share recur_v1 on github/fb (may2018). a dozon or so people building this and talking about it was satifying but i had no imediate plans to continue developing for it, besides maintance, bugfixes, simple user requests etc...

however after being invited to a 3-week toolmaker residency in Owego NY i felt incouraged and enabled to explore some bigger new ideas for the instrument.

the name __r_e_c_u_r__ refers to the video sampling/looping feature at the core of this device. as the scope of what it can do is expanded, naming and originising the (optional) extensions helps define their use.

## c_a_p_t_u_r

_an optional extension for live sampling through the pi camera input_

this was paritally included in v1 although limited to inputs from the rpi-camera. while at SC i had the chance to try it with a piCaptureSd1 hat which allows sd video input from composite, component and svideo. some settings have been added to improve the captur image.

## c_o_n_j_u_r

_an alternative openframeworks backend for extended video control and glsl-shader intergration_

this is the largest addition from the v1 release. although omxplayer is a gpu-accelerated videoplayer that is stable and forgiving it is designed as a mediaplayer for watching films etc, not as a platform for creative coding. r_e_c_u_r can sequence omxplayer to playback samples exactly how they are (and seek etc for sublooping) but is limiting for any futher playback manipulation - even varying playback speed was quite difficult through omxplayer.

openframeworks is more suited for video manipulation and opens a lot of possiblites to how the samples can be played. one example is the ability to adjust the playback speed, including playing videos backwards.

### shaders

a few other projects have been based around using a raspberry pi as a visual instrument in another way - instead of focusing on video-clip playback, these play glsl-shaders, fragments of code that run directly on the gpu, allowing the creation of interesting digital visual generation.

although generated in real time, shader-playback is similar to video playback in that you can select a prepared source (video-file or shader-code) and peform with it - trigger when to start and stop, interact with parameters live (video start/stop/alpha/position/speed or user defined shader parameters).

recur already has the ui to browse folders and files, select and map them, to display the relivent infomation, and openframeworks has the ability to load and play shaders much like you would load and play videos. this seemed like a logical and powerful extension to the sampler core.

## i_n_c_u_r

_become subject to (something unwelcome or unpleasant) as a result of one's own behavior or actions_

this is related to extending recurs sequencing/performablity by exposing its controls to external manipulation.

usb-midi control over recur actions was in the v1 release including the first example of continous inputs via midi-cc. this gives control over parameters which otherwise are difficult to interact with on a numpad alone (video/preview alpha). as the amount of control increases so does the need for continous inputs.

at SC i created a circuit that allows 8 analog inputs (4 pots, 4 0-5v cv) and serial(din)-midi into recur.

## modulation

having defined these different areas of the __r_e_c_u_r__ video instrument, we also have created some powerful combinations (some are trival/obvious like _i_n_c_u_r_ + _r_e_c_u_r_ for external sequencing of video samples, or _c_a_p_t_u_r_ + _r_e_c_u_r_ for recording live input directly followed by sampling it) others include:

- _r_e_c_u_r_ + _c_o_n_j_u_r_ : at first i was thinking of video-files and glsl-shaders as seperate sources for creating video. however then i discovered how you can also _use_ a glsl-shader to process a video-file (shaders can take textures as input, one of which can be a video), leading me to make the distintion in recur between _generating shaders_ and _processing shaders_ .

- c_a_p_t_u_r_ + _c_o_n_j_u_r_ : not only can _processing shaders_ accept video as a texture-input, they can also take texture from a live input (a camera or capture card for example). this means recur can also be used to process live video input in real time.

## direction

what started as a simple solution for seamless prerecorded video playback is starting to look something closer to the video equivalent to audios groovebox - where a (good) groovebox may include sampling, sequencing, synth-presets, audio-effects and live-input/effect-through , this new __r_e_c_u_r__ + _i_n_c_u_r_ + _c_o_n_j_u_r_ + _c_a_p_t_u_r_ may come close to a fully open, customizable and diy video analogue.
