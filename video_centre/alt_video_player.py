

class AltVideoPlayer:
    def __init__(self, root, message_handler, data, osc_client, name):
        self.root = root
        self.message_handler = message_handler
        self.data = data
        self.name = name
        self.player_running = False
        self.status = 'EMPTY'
        self.total_length = 0.0
        self.bankslot_number = '*-*'
        self.start = -1.0
        self.end = -1.0
        self.rate = 1
        self.crop_length = 0.0
        self.location = ''
        self.load_attempts = 0
        self.alpha = 0
### new stuff
        self.client = osc_client

        self.position = -1


    def try_load(self, layer):
        load_attempts = 0
        while(load_attempts < 2):
            load_attempts = load_attempts + 1
            if self.load(layer):
                print('load success')
                return True
            else:
                print('load failed')
        self.message_handler.set_message('ERROR', 'failed to load')
        self.status = 'ERROR'
        return False
            

    def load(self, layer):
        #try:
        self.get_context_for_player()
        #is_dev_mode, first_screen_arg, second_screen_arg = self.set_screen_size_for_dev_mode()
        #arguments = ['--no-osd', '--layer', str(layer), '--adev', 'local', '--alpha', '0', first_screen_arg, second_screen_arg]
        #if not is_dev_mode:
         #   arguments.append('--blank=0x{}'.format(self.data.get_background_colour()))
        print('the location is {}'.format(self.location))
        if self.location == '':
            self.status = 'EMPTY'
            return True

        if(self.end is -1): 
            self.end = self.total_length
        if(self.start is -1):
            self.start = 0
        self.client.send_message("/player/{}/load".format(self.name[0]), [self.location, self.start / self.total_length, self.end / self.total_length])
        self.crop_length = self.end - self.start
        if 'show' in self.data.settings['sampler']['ON_LOAD']['value']:
            self.set_alpha_value(255)
        else:
            pass
            self.set_alpha_value(0)
        return True
        #except (ValueError, SystemError) as e:
          #  print(e)
            #self.message_handler.set_message('ERROR', 'load attempt fail')
            #return False

    def start_video(self):
        if 'play' in self.data.settings['sampler']['ON_START']['value']:
            self.status = 'PLAYING'
            self.client.send_message("/player/{}/play".format(self.name[0]), True)
        else:
            self.status = 'START'
        if 'show' in self.data.settings['sampler']['ON_START']['value']:
            self.set_alpha_value(255)
        else:
            self.set_alpha_value(0)




    def reload(self, layer):
        self.exit()
        self.player_running = False
        self.try_load(layer)

    def is_loaded(self):
        return self.status == 'LOADED'

    def is_finished(self):
        return self.status == 'FINISHED'

    def get_context_for_player(self):
        next_context = self.data.get_next_context()
        self.location = next_context['location']
        self.total_length = next_context['length']
        self.start = next_context['start']
        self.end = next_context['end']
        self.bankslot_number = next_context['bankslot_number']
        self.rate = next_context['rate']

    def toggle_pause(self):
        if self.status == "PLAYING":
            self.client.send_message("/player/{}/pause".format(self.name[0]), True)
        elif self.status == "PAUSED" or self.status == "LOADED":
            self.client.send_message("/player/{}/play".format(self.name[0]), True)
        else:
            print("error toggling pause when video is neither playing or paused")

    def toggle_show(self):
        if self.alpha > 127:
            self.show_toggle_on = False
            self.set_alpha_value(0)
        else:
            self.show_toggle_on = True
            self.set_alpha_value(255)

    def set_alpha_value(self, amount):
        self.client.send_message("/player/{}/alpha".format(self.name[0]), amount)
        self.alpha = amount

    def seek(self, amount):
        position = self.position
        after_seek_position = position + amount
        if after_seek_position > self.start and after_seek_position < self.end:
            self.set_position(after_seek_position)
        else:
            self.message_handler.set_message('INFO', 'can not seek outside range')

    def change_rate(self, amount):
        pass
        #new_rate = self.rate + amount
        #if (new_rate > self.omx_player.minimum_rate() and new_rate < self.omx_player.maximum_rate()):
         #   updated_speed = self.omx_player.set_rate(new_rate)
          #  self.rate = new_rate
            #print('max rate {} , min rate {} '.format(self.omx_player.maximum_rate() ,self.omx_player.minimum_rate()))
            #return new_rate
        #else:
          #  self.message_handler.set_message('INFO', 'can not set speed outside of range')
            #return self.rate

    def get_position(self):
        return self.position

    def set_position(self, position):
        self.client.send_message("/player/{}/position".format(self.name[0]), position / self.total_length)

    def exit(self):
        try:
            self.client.send_message("/player/{}/quit".format(self.name[0]),True) 
            self.player_running = False
        except:
            pass

    ## not sure if i am going to implement this atm 
    def set_screen_size_for_dev_mode(self):
        if self.data.settings['other']['DEV_MODE_RESET']['value'] == 'on':
            ##self.client.send_message("/player/{}/alpha".format(self.name[0]), amount)
            return True, '--win', '50,350,550,750'
        else:
            aspect_mode = self.data.settings['video']['SCREEN_MODE']['value']
            return False, '--aspect-mode', aspect_mode














