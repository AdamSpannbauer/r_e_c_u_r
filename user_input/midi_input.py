import string
import datetime
import mido
import subprocess

class MidiInput(object):
    def __init__(self, root, message_handler, display, actions, data):
        self.root = root
        self.message_handler = message_handler
        self.display = display
        self.actions = actions
        self.data = data
        self.midi_mappings = data.midi_mappings
        self.midi_device = None
        self.midi_delay = 1
        self.serial_port_process = None
        self.try_open_port()

    def try_open_port(self):
        midi_setting = self.data.settings['midi']['INPUT']['value']
        #print('try open port : midi setting is {}'.format(midi_setting))
        if midi_setting == 'usb':
            self.stop_serial_port_process()
            self.open_this_port_and_start_listening(20)
        elif midi_setting == 'serial':
            self.create_serial_port_process()
            self.open_this_port_and_start_listening(128)
        else:
            self.stop_serial_port_process()     
        self.root.after(1000, self.try_open_port)

    def open_this_port_and_start_listening(self, port_number):
        midi_ports = mido.get_input_names()
        print('midi ports are {}'.format(midi_ports))
        midi_device_on_port = [s for s in midi_ports if '{}:0'.format(port_number) in s]
        if midi_device_on_port:
            if self.data.midi_status == 'disconnected':
                self.midi_device = mido.open_input(midi_device_on_port[0])
                self.data.midi_status = 'connected'
                self.message_handler.set_message('INFO', 'connected to midi device {}'.format(self.midi_device.name))
                self.poll_midi_input()
        elif self.data.midi_status == 'connected':
            self.data.midi_status = 'disconnected'

    def poll_midi_input(self):
        i = 0
        cc_dict = dict()
        for message in self.midi_device.iter_pending():
            i = i + 1
            message_dict = message.dict()
            midi_channel = midi_setting = self.data.settings['midi']['CHANNEL']['value'] - 1
            if not message_dict['channel'] == midi_channel:
                pass
            ## turning off noisey clock messages for now - may want to use them at some point
            elif message_dict['type'] == 'clock':
                pass
            ## trying to only let through step cc messages to increase response time
            elif message_dict['type'] == 'control_change':
                control_number = message_dict['control']
                if not control_number in cc_dict.keys():
                    cc_dict[control_number] = message_dict['value']
                else:
                    step_size = 4
                    ignore_range = range(cc_dict[control_number] - step_size,cc_dict[control_number] + step_size)
                    if not message_dict['value'] in ignore_range:
                        cc_dict[control_number] = message_dict['value']
                        self.on_midi_message(message_dict)
                print(cc_dict)
            else:       
                self.on_midi_message(message_dict)
        if i > 0:
            print('the number processed {}'.format(i))
        self.root.after(self.midi_delay, self.poll_midi_input)

    def on_midi_message(self, message_dict):
        if message_dict['type'] == 'note_on' and message_dict['velocity'] == 0:
            ## edge case where on note of zero alternative for off note.
            message_dict['type'] = 'note_off'
        mapped_message_name = message_dict['type']
        mapped_message_value = None
        if 'note' in message_dict:
            mapped_message_name = '{} {}'.format(mapped_message_name,message_dict['note'])
        if 'control' in message_dict:
            mapped_message_name = '{} {}'.format(mapped_message_name,message_dict['control'])
            mapped_message_value = message_dict['value']
        
        if mapped_message_name in self.midi_mappings.keys():
            self.run_action_for_mapped_message(mapped_message_name, mapped_message_value)
        else:
            print('{} is not in midi map'.format(mapped_message_name))

    def run_action_for_mapped_message(self, message_name, mapped_message_value):
        this_mapping = self.midi_mappings[message_name]
        if self.data.control_mode in this_mapping:
            mode = self.data.control_mode
        elif 'DEFAULT' in this_mapping:
            mode = 'DEFAULT'

        if self.data.function_on and len(this_mapping[mode]) > 1:
            method_name = this_mapping[mode][1]
            self.data.function_on = False
        else:
            method_name = this_mapping[mode][0]

        print('the action being called is {}'.format(method_name))
        if mapped_message_value is not None:
            norm_message_value = mapped_message_value/127 
        else:
            norm_message_value = None
        self.call_method_name(method_name, norm_message_value)
        ## only update screen if not continuous - seeing if cc can respond faster if not refreshing screen on every action
        if 'continuous' not in message_name:
            self.display.refresh_display()

    def call_method_name(self, method_name, argument=None):
        if argument is not None:
            getattr(self.actions, method_name)(argument)
        else:
            getattr(self.actions, method_name)()

    def create_serial_port_process(self):
        if self.serial_port_process == None:
            self.serial_port_process = subprocess.Popen("exec " + "ttymidi -s /dev/serial0 -b 38400 -n serial", shell=True)
            print('created the serial port process ? {}'.format(self.serial_port_process))        

    def stop_serial_port_process(self):
        if self.serial_port_process is not None:
            self.serial_port_process.kill()
            self.serial_port_process = None






