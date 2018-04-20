try:
    from omxplayer.player import OMXPlayer
except:
    pass


class video_player:
    def __init__(self, root, message_handler, data, name):
        self.root = root
        self.message_handler = message_handler
        self.data = data
        self.omx_player = None
        self.name = name
        self.omx_running = False
        self.status = 'N/A'
        self.total_length = 0.0
        self.bankslot_number = '*-*'
        self.start = -1.0
        self.end = -1.0
        self.rate = 1
        self.crop_length = 0.0
        self.location = ''
        self.load_attempts = 0

    def try_load(self):
        load_attempts = 0
        while(load_attempts < 2):
            load_attempts = load_attempts + 1
            if self.load():
                print('load success')
                return True
            else:
                print('load failed')
        self.message_handler.set_message('ERROR', 'failed to load')
        self.status = 'ERROR'
        return False
            

    def load(self):
        try:
            self.get_context_for_player()
            first_screen_arg, second_screen_arg = self.set_screen_size()
            self.arguments = ['--no-osd', '--adev', 'local', '--alpha', '0', first_screen_arg, second_screen_arg]
            self.status = 'LOADING'
            print('the location is {}'.format(self.location))
            self.omx_player = OMXPlayer(self.location, args=self.arguments, dbus_name=self.name)
            self.omx_running = True
            self.total_length = self.omx_player.duration() # <-- uneeded once self.duration stores float
            if(self.end is -1): 
                self.end = self.total_length
            if(self.start is -1):
                self.start = 0
            self.crop_length = self.end - self.start
            print('{}: the duration is {}'.format(self.name, self.total_length))
            if self.start > 0.9:
                self.set_position(self.start - 0.9)
            self.pause_at_start()
            #print('set rate to {}'.format(self.rate))
            #self.omx_player.set_rate(self.rate)
            #self.load_attempts = 0
            return True
        except (ValueError, SystemError):
            #self.message_handler.set_message('ERROR', 'load attempt fail')
            return False

    def pause_at_start(self):
        position = self.get_position()
        start_threshold = round(self.start - 0.05,2)
        #print('is playing: {} , position : {} , start_threshold : {}'.format(self.omx_player.is_playing(), position, start_threshold))
        if position > start_threshold:
            self.status = 'LOADED'
            self.omx_player.set_alpha(255)
            self.omx_player.pause()
        elif self.omx_running:
            self.root.after(5, self.pause_at_start)

    def play(self):
        self.status = 'PLAYING'
        #self.omx_player.set_alpha(255)
        self.omx_player.play()
        self.pause_at_end()

    def pause_at_end(self):
        position = self.get_position()
        end_threshold = self.end - 0.2
        if(position > end_threshold):
            self.status = 'FINISHED'
            self.omx_player.pause()
            print('its paused at end!')
        elif(self.omx_running):
            self.root.after(5, self.pause_at_end)

    def reload(self):
        self.exit()
        self.omx_running = False
        self.try_load()

    def is_loaded(self):
        return self.status is 'LOADED'

    def is_finished(self):
        return self.status is 'FINISHED'

    def get_position(self):
        try:
            return self.omx_player.position()
        except:
            print('{}: error get_position'.format(self.name))
            return -1

    def get_context_for_player(self):
        next_context = self.data.get_next_context()
        self.location = next_context['location']
        #self.total_length = next_context['length']
        self.start = next_context['start']
        self.end = next_context['end']
        self.bankslot_number = next_context['bankslot_number']
        self.rate = next_context['rate']

    def toggle_pause(self):
        self.omx_player.play_pause()
        self.status = self.omx_player.playback_status().upper()

    def seek(self, amount):
        position = self.get_position()
        after_seek_position = position + amount
        if after_seek_position > self.start and after_seek_position < self.end:
            self.set_position(after_seek_position)
            #self.player.seek(amount)
        else:
            self.message_handler.set_message('INFO', 'can not seek outside range')

    def change_rate(self, amount):
        new_rate = self.rate + amount
        if (new_rate > self.omx_player.minimum_rate() and new_rate < self.omx_player.maximum_rate()):
            updated_speed = self.omx_player.set_rate(new_rate)
            self.rate = new_rate
            print('max rate {} , min rate {} '.format(self.omx_player.maximum_rate() ,self.omx_player.minimum_rate()))
            return new_rate
        else:
            self.message_handler.set_message('INFO', 'can not set speed outside of range')
            return self.rate

    def set_position(self, position):
        self.omx_player.set_position(position)

    def exit(self):
        try:
            self.omx_player.quit()
            self.status = 'N/A'
            self.omx_running = False
        except:
            pass

    def set_screen_size(self):
        ## only dev mode is needed now that auto handles all modes... can be removed probably ...
        if self.data.get_screen_size_setting() == 'dev_mode':
            return '--win', '50,350,550,750'
        elif self.data.get_screen_size_setting() == 'composite_pal':
            return '--win', '0,0,768,576'
        elif self.data.get_screen_size_setting() == 'composite_ntsc':
            return '--win', '0,0,640,480'
        elif self.data.get_screen_size_setting() == 'composite_converter':
            return '--win', '45,15,970,760'
        elif self.data.get_screen_size_setting() == 'XGA':
            return '--win', '0,0,1024,768'
        else:
            return '--aspect-mode', 'stretch'


class fake_video_player:
    def __init__(self):
        self.player = None
        self.name = 'fake'
        self.omx_running = False
        self.status = 'N/A'
        self.duration = 0
        self.bankslot_number = '*-*'
        self.start = -1
        self.end = -1
        self.length = 0
        self.location = ''



