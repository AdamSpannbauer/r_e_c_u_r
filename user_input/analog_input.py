import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

class AnalogInput(object):
    def __init__(self, root, message_handler, display, actions, data):
        self.root = root
        self.message_handler = message_handler
        self.display = display
        self.actions = actions
        self.data = data
        self.analog_mappings = data.analog_mappings
        self.analog_delay = 50
        self.last_readings = [0,0,0,0,0,0,0,0]

        SPI_PORT   = 1
        SPI_DEVICE = 2
        self.analog_input = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
        self.check_if_listening_enabled()
        

    def check_if_listening_enabled(self):
        if self.data.settings['other']['ANALOG_INPUT']['value'] == 'enabled':
            self.poll_analog_inputs()
        else:
            self.root.after(1000, self.check_if_listening_enabled)

    def poll_analog_inputs(self):
        if self.data.settings['other']['ANALOG_INPUT']['value'] == 'enabled':
            for i in range(0,8):        
                if str(i) in self.analog_mappings:
                    this_reading = self.analog_input.read_adc(i)
                    if this_reading - self.last_readings[i] > 3:
                        self.run_action_for_mapped_channel(i, this_reading)
                    self.last_readings[i] = this_reading
            self.root.after(self.analog_delay, self.poll_analog_inputs)
        else:
            self.check_if_listening_enabled()

    def run_action_for_mapped_channel(self, channel, channel_value):
        this_mapping = self.analog_mappings[str(channel)]
        if self.data.control_mode in this_mapping:
            mode = self.data.control_mode
        elif 'DEFAULT' in this_mapping:
            mode = 'DEFAULT'

        if self.data.function_on and len(this_mapping[mode]) > 1:
            method_name = this_mapping[mode][1]
            self.data.function_on = False
        else:
            method_name = this_mapping[mode][0]

        if channel_value is not None:
            norm_channel_value = channel_value/1023 
        else:
            norm_channel_value = None

        print('the action being called is {}'.format(method_name))
        self.call_method_name(method_name, norm_channel_value)
        ## not sure whether we want to update the screen in general; here - probably not most of the time ...
        #if 'cc' not in message_name:
         #   self.display.refresh_display()

    def call_method_name(self, method_name, argument=None):
        if argument is not None:
            getattr(self.actions, method_name)(argument)
        else:
            getattr(self.actions, method_name)()

            
