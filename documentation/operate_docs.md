# how to use r_e_c_u_r

## getting started

- insert a usb with some videos you want to sample
- connect the hdmi output to the display you want to use
- power the raspberry pi. you should see red lights on the pi board, some boot text on the hdmi out and the lcd display light up
- after a few moments , a video should play on the display output , the raspberian desktop will load on lcd and then (after a few moments) the r_e_c_u_r display will load
- the `DSPLY` key can be used to cycle through _display_modes_

## controls

the controls on r_e_c_u_r work by mapping `keys` to `actions`. (custom mappings ?) by default most keys map to the same action independant of the state (ie display mode) the r_e_c_u_r is in.

The exceptions to this are the control keys:

- `<` and `>` : used for navigation when applicable (see below) ; used for seeking current sample in `SAMPLER` mode
- `■` : used as 'enter' for navigation ; used to toggle pause/play in `SAMPLER` mode.

the display modes described below are cycled by using the `DISPLAY` key. some actions are accessable through a `2ND FUNC` layer, toggled by the corrosponding key.
other controls include:

- `→` is used to trigger the next loaded sample to play
- loading the sample in slot `x` to play next; where `x` is a key from `0` to `9`
- cropping the current sample to start  (`[`) or end (`]`) at the current time
- cycling forward back (`PRV BNK`) or (`NXT BNK`) through the banks of sample , or clearing a bank (`CLR BNK`) (note not implemented yet)
- `< SPD` and `> SPD` are used to decrease and increase the speed of the currently playing clip (note not implemented yet)

some keys are empty to leave room for future features. i encourage you to make a custom key map (link to doc) or add actions (another link) you would like to use.

## `PLAYER` display

this section displays infomation about what is in the video player : the position from start and end of currently playing video, what [slot] is playing now and what slot is loaded [next] 

## `BROWSER` display mode

this is where you can load samples from your usb into the `SAMPLER`

- in this mode ,  the `<` and `>` keys will move the selection up and down
- folders are displayed ending in `|` for closed and `/` for open , the depth is displayed as indentation
- pressing the `■` key while a folder is selected toggles it open/closed
- pressing the `■` key while a video is selected loads it into the next avaliable slot (note : you can see the first slot a video is loaded into on right colunm)

## `SAMPLER` display mode

this is the main display mode for using r_e_c_u_r. from this view you can see details of all the samples loaded into the sampler. a `bank` contains 10 `slots` labeled `0` - `9`. pressing the corrosponding `key` will load the `sample` in this `slot` to start when the current sample finishes. the `slot` of the currently playing sample is highlighted.

## `SETTINGS` display mode

this is where you can configure r_e_c_u_r's settings.

- navigate the menu with `<` and `>` keys like about
- pressing `■` on a setting will either cycle through it's `options` or run an `action` depending on its type (an `action` setting will always have value `run_action`)


