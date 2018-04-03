# how to build r_e_c_u_r

## get some parts

these are the parts you need to get. to reduce costs i sourced them through aliexpress.com but if you have other parts lying around try them out and let me know how it goes.

### main parts:

- [raspberry pi3] *37 USD* (watch this space for experiments with other models/sbc's)

- [raspberry pi screen] *12 USD*

- [usb keypad] *9 USD*

![main parts][main parts]

other bits and pieces:

- 4x m2 and 7x m3 screws - a few dollars (exact lengths/links etc coming soon)

- 8 gig or greater mircoSD card

- stable 5volt1A microUsb power supply

- a usb for samples

- hdmi cable for output...

## print some things

- 3d print the front panel, back panel and spaces from these files

- 2d print these [key stickers] (or modify/create your own!) onto vinyl, label paper or normal paper with double sided tape...

## put it together

- using [etcher] (or otherwise) flash the micro sd with this modified image of raspberian (or follow these [dotfile] instructions)

- insert sd card into pi

- attach screen via the pi header pins and use screen spacers (with a little bluetac) to fasten it in

- use the small screws to attach pi+screen to the back panel

- attach keypad to the back panel and fasten in with a extra screw if necessary

- put large screws through back panel facing up and use spacers

- attach top panel and hold with nuts

## try it owt

[raspberry pi3]:https://www.aliexpress.com/item/RS-Version-2016-New-Raspberry-Pi-3-Model-B-Board-1GB-LPDDR2-BCM2837-Quad-Core-Ras/32789942633.html?spm=a2g0s.9042311.0.0.FkRWty
[main parts]: build_all.jpg
[raspberry pi screen]:https://www.aliexpress.com/item/3-5-Inch-TFT-LCD-Moudle-For-Raspberry-Pi-2-Model-B-RPI-B-raspberry-pi/32707058182.html?spm=a2g0s.13010208.99999999.262.bV4EPV
[usb keypad]:https://www.aliexpress.com/item/2-4G-Wireless-Keyboard-USB-Numeric-Keypad-19-Keys-Mini-Digital-Keyboard-Ultra-Slim-Number-Pad/32818206308.html?spm=a2g0s.9042311.0.0.FkRWty
[key stickers]: https://docs.google.com/document/d/1vhXv5QTfyUqsZuMdQu1lh2dMfEk5HMNVyp8uhrc-I2w/edit?usp=sharing
[etcher]: https://etcher.io
[dotfile]: ../dotfiles/README.md
