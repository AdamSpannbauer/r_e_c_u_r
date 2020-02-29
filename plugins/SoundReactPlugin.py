import math
import data_centre.plugin_collection
from data_centre.plugin_collection import ActionsPlugin, SequencePlugin, DisplayPlugin, AutomationSourcePlugin

import pyaudio
import numpy as np
#import matplotlib.pyplot as plt

np.set_printoptions(suppress=True) # don't use scientific notationn

class SoundReactPlugin(ActionsPlugin,SequencePlugin,DisplayPlugin):
    disabled = False

    DEBUG = False

    active = True
    stop_flag = False
    pause_flag = False

    CHUNK = 4096 # number of data points to read at a time
    RATE = 48000 #44100 # time resolution of the recording device (Hz)
    
    frequency = 10 # how often messages are sampled+calculated+sent, not anything to do with audio frequency

    config = {}

    def __init__(self, plugin_collection):
        super().__init__(plugin_collection)

        #self.PRESET_FILE_NAME = "ShaderLoopRecordPlugin/frames.json"
        if self.active and not self.disabled:
            try:
                p=pyaudio.PyAudio()
                self.stream=p.open(format=pyaudio.paInt16,channels=1,rate=self.RATE,input=True,
                    frames_per_buffer=self.CHUNK)
            except:
                print("Failed to open sound device - disabling SoundReactPlugin!")
                self.disabled = True
                return

        print ("now setting to run automation..")

        self.pc.shaders.root.after(500, self.run_automation)

    @property
    def sources(self):
        # TODO: write more interpreters
        return {
            "energy": self.energy,
            #"low": self.low,
            #"mid": self.mid,
            #"high": self.high,
            "peakfreq": self.peakfreq
        }

    values = {}
    levels = {
            "energy": [ 0.0, 0.0, 1.0, 0.0 ],
            "peakfreq": [ 0.0, 0.0, 0.0, 1.0 ]
    }
    last_values = {}
    display_values = {}
    # triggers?
    #   sudden drop - sudden leap?

    # DisplayPlugin methods
    def get_display_modes(self):
        return ['SOUNDMOD','NAV_SND']

    def show_plugin(self, display, display_mode):
        from tkinter import Text, END
        #super(DisplayPlugin).show_plugin(display, display_mode)
        display.display_text.insert(END, '{} \n'.format(display.body_title))
        display.display_text.insert(END, "SoundReactPlugin - ")

        display.display_text.insert(END, "ACTIVE\n" if self.active else "not active\n")

        #display.display_text.insert(END, "\tSpeed: {:03.2f}\n\n".format(self.speed))

        for sourcename in sorted(self.sources):
            value = self.display_values.get(sourcename) or "{:03.2f}%".format(self.values.get(sourcename,0)*100) or "None"
            value += "\t"
            for i,l in enumerate(self.levels[sourcename]):
                bar = u"_\u2581\u2582\u2583\u2584\u2585\u2586\u2587\u2588"
                g = "ABCD"[i]+'%s '%bar[int(l*(len(bar)-1))]
                value += g
            display.display_text.insert(END, "{}:\t{}\n".format(sourcename,value))
            """display.display_text.insert(END, "%s\n" %self.last_lfo_status[lfo])
            display.display_text.insert(END, "\t%s\n" % self.formula[lfo])"""

        #display.display_text.insert(END, "\nLevels:%s\n\n" % self.levels)
        display.display_text.insert(END, "\n\n\n")


    def run_sequence(self, position):
        # position is irrelvant for this plugin, we just want to run continuously
        if not self.active:
            return

        data = np.fromstring(self.stream.read(self.CHUNK, exception_on_overflow = False),dtype=np.int16)

        for sourcename in self.sources:
            value = self.sources[sourcename](data)
            self.values[sourcename] = value
            if value is None: 
                continue
            for slot,level in enumerate(self.levels.get(sourcename,[])):
                if level>0.0 and self.values.get(sourcename)!=self.last_values.get(sourcename):
                    self.pc.actions.call_method_name("modulate_param_%s_to_amount_continuous"%slot, self.values[sourcename])
                    self.last_values[sourcename] = self.values[sourcename]

    config.setdefault('energy',{})['gain'] = 0.5 # how much to multiply signal by
    config.setdefault('energy',{})['threshold'] = 0.5 # subtract from post-gain signal (hence ignore all values below)
    GAIN_MULT = 1.0
    def energy(self,data):
        peak=np.average(np.abs(data))*2
        value = (peak/2**16)/16 * 100

        value *= (self.GAIN_MULT * self.config['energy']['gain'])

        value = value - self.config['energy']['threshold']
        if value<0.0:
            value = 0.0
        if value>1.0:
            value = 1.0

        bars="#"*int(50*value)
        if self.DEBUG: print("energy:\t\t%05d %s\t(converted to %s)"%(peak,bars,value))
        bar = u"_\u2581\u2582\u2583\u2584\u2585\u2586\u2587\u2588"
        g = '%s'%bar[int(value*(len(bar)-1))]
        self.display_values['energy'] = "{} g{:03.2f} t{:03.2f}".format(g, self.config['energy']['gain'], self.config['energy']['threshold'])

        return value 

    # dont think this works properly, or maybe it do just be like that
    def peakfreq(self,data):
        data = data.copy() * np.hanning(len(data)) # smooth the FFT by windowing data
        fft = abs(np.fft.fft(data).real)
        fft = fft[:int(len(fft)/2)] # keep only first half
        freq = np.fft.fftfreq(self.CHUNK,1.0/self.RATE)
        freq = freq[:int(len(freq)/2)] # keep only first half
        freqPeak = freq[np.where(fft==np.max(fft))[0][0]]+1
        if freqPeak<400:
            return False
        value = freqPeak/16000
        value = value**16/16
        if self.DEBUG: print("peak frequency:\t%d\tHz\t(converted to %s)"%(freqPeak,value))
        self.display_values['peakfreq'] = ("%d Hz\t"%freqPeak) + "{:03.2f}".format(value)

        return value


    # ActionsPlugin methods
    @property
    def parserlist(self):
        return [
                ( r"^toggle_sound_react_active$", self.toggle_active ),
                ( r"^sound_set_config_([a-z]*)_([a-z]*)$", self.set_config ),
                ( r"^sound_set_modulation_([a-z]*)_slot_([0-3])_level$", self.set_modulation_source_slot_level ),
        ]

    def set_modulation_source_slot_level(self, sourcename, slot, level):
        self.levels.setdefault(sourcename,[0.0,0.0,0.0,0.0])[slot] = level

    def set_config(self, sourcename, setting, value):
        if type(self.config.get(sourcename,{}).get(setting)) is str:
            print ("SoundReactPlugin: type of existing setting is string, probably doesnt make sense to set this to a value of this type!")
        self.config[sourcename][setting] = value

    def toggle_active(self):
        self.active = not self.active
