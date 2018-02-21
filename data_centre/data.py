import json
import os
from random import randint
import inspect
from itertools import cycle
try:
    from omxplayer.player import OMXPlayer
except:
    pass

from data_centre.browser_data import BrowserData

def get_the_current_dir_path():
    # TODO: investigate weird path formatting differences
    current_file_path = inspect.stack()[0][1]
    return os.path.split(current_file_path)[0]

BANK_DATA_JSON = 'display_data.json'
NEXT_BANKSLOT_JSON = 'next_bankslot_number.json'
SETTINGS_JSON = 'settings.json'
KEYPAD_MAPPING = 'keypad_action_mapping.json'
EMPTY_SLOT = dict(name='', location='', length=-1, start=-1, end=-1)
PATH_TO_DATA_OBJECTS = '{}/json_objects/'.format(get_the_current_dir_path())

def read_json(file_name):
    with open(PATH_TO_DATA_OBJECTS + file_name) as data_file:
        data = json.load(data_file)
    return data


def update_json(file_name, data):
    with open('{}{}'.format(PATH_TO_DATA_OBJECTS, file_name), 'w') as data_file:
        json.dump(data, data_file)



def get_path_to_browser():
    return read_json('path_to_browser.json')

PATH_TO_BROWSER = get_path_to_browser()


class Data(object):
    def __init__(self, message_handler):
        self.browser_data = BrowserData(PATH_TO_BROWSER)
        self.message_handler = message_handler

        self.has_omx = self._try_import_omx()
        print('has_omx: {}'.format(self.has_omx))

    def get_screen_size_setting(self):
        return read_json(SETTINGS_JSON)[0]['options'][0]

    def create_new_slot_mapping_in_first_open(self, file_name, bank_number):
        ######## used for mapping current video to next available slot ########
        memory_bank = read_json(BANK_DATA_JSON)
        for index, slot in enumerate(memory_bank[bank_number]):
            if (not slot['name']):
                self.create_new_slot_mapping(bank_number, index, file_name)
                return True
        return False

    def create_new_slot_mapping(self,bank_number, slot_number, file_name):
        ######## used for mapping current video to a specific slot ########
        has_location, location = self._get_path_for_file(file_name)
        print('file_name:{},has_location:{}, location:{}'.format(file_name,has_location, location))
        length = self._get_length_for_file(location)
        new_slot = dict(name=file_name, location=location, length=length, start=-1, end=-1)
        self._update_a_slots_data(bank_number, slot_number, new_slot)

    @staticmethod
    def clear_all_slots(bank_number):
        memory_bank = read_json(BANK_DATA_JSON)  
        for index, slot in enumerate(memory_bank[bank_number]):
            memory_bank[bank_number][index] = EMPTY_SLOT
        update_json(BANK_DATA_JSON, memory_bank)

    def update_next_slot_number(self, bank_number, new_value):
        memory_bank = read_json(BANK_DATA_JSON)
        if memory_bank[bank_number][new_value]['location'] == '':
            print('its empty!')
            self.message_handler.set_message('INFO', 'the slot you pressed is empty')
        else:
            update_json(NEXT_BANKSLOT_JSON, '{}-{}'.format(bank_number,new_value))

    def add_open_folder(self, folder_name):
        self.browser_data.update_open_folders(folder_name)

    def check_if_setting_selection_is_action_otherwise_cycle_value(self, setting_index):
        ######## update the value of selected setting by cycling through valid options ########
        selected_setting = read_json(SETTINGS_JSON)[setting_index]
        if(selected_setting['options'][0] == 'run_action'):
            return True,  selected_setting['name']
        else:
            self.cycle_setting_value(setting_index)
            return False, None

    def cycle_setting_value(self, setting_index):
            settings = read_json(SETTINGS_JSON)
            this_setting_option = settings[setting_index]['options']
            this_setting_option= this_setting_option[len(this_setting_option)-1:]+this_setting_option[0:len(this_setting_option)-1]
            settings[setting_index]['options'] = this_setting_option
            update_json(SETTINGS_JSON, settings)

    def rewrite_browser_list(self):
        return self.browser_data.generate_browser_list()

    def return_browser_list(self):
        return self.browser_data.browser_list

    @classmethod
    def split_bankslot_number(cls, slot_number):
        split = slot_number.split('-')
        print(split)
        is_bank_num_int , converted_bank_number = cls.try_convert_string_to_int(split[0])
        is_slot_num_int , converted_slot_number = cls.try_convert_string_to_int(split[1])
        return converted_bank_number, converted_slot_number

    @staticmethod
    def try_convert_string_to_int(string_input):
        try:
            return True , int(string_input)
        except ValueError:
            return False , '*'

    @staticmethod
    def get_settings_data():
        return read_json(SETTINGS_JSON)

    @staticmethod
    def get_keypad_mapping_data():
        return read_json(KEYPAD_MAPPING)

    @staticmethod
    def get_sampler_data():
        return read_json(BANK_DATA_JSON)

    def get_next_context(self):
        ######## loads the slot details, uses settings to modify them and then set next slot number ########
        next_bankslot_number = read_json(NEXT_BANKSLOT_JSON)
        memory_bank = read_json(BANK_DATA_JSON)
        bank_num , slot_num = self.split_bankslot_number(next_bankslot_number)
        next_slot_details = memory_bank[bank_num][slot_num]
        start_value = next_slot_details['start']
        end_value = next_slot_details['end']
        length = next_slot_details['length']

        context = dict(location=next_slot_details['location'], name=next_slot_details['name'],
                       length=next_slot_details['length'], start=start_value, end=end_value,
                       slot_number=next_bankslot_number)
        return context

    def update_slot_start_to_this_time(self, bank_number, slot_number, position):
        memory_bank = read_json(BANK_DATA_JSON)
        memory_bank[bank_number][slot_number]['start'] = position
        update_json(BANK_DATA_JSON, memory_bank)

    def update_slot_end_to_this_time(self,bank_number, slot_number, position):
        memory_bank = read_json(BANK_DATA_JSON)
        memory_bank[bank_number][slot_number]['end'] = position
        update_json(BANK_DATA_JSON, memory_bank)

    def _get_length_for_file(self, path):
        if self.has_omx:
            temp_player = OMXPlayer(path, args=['--alpha', '0'], dbus_name='t.t')
            duration = temp_player.duration()
            temp_player.quit()
            return duration
        else:
            return -1

    def _get_path_for_file(self, file_name):
        ######## returns full path for a given file name ########
        for root, dirs, files in os.walk(PATH_TO_BROWSER):
            if file_name in files:
                return True, '{}/{}'.format(root, file_name)
        return False, ''

    @staticmethod
    def _update_a_slots_data(bank_number, slot_number, slot_info):
        ######## overwrite a given slots info with new data ########
        memory_bank = read_json(BANK_DATA_JSON)
        memory_bank[bank_number][slot_number] = slot_info
        update_json(BANK_DATA_JSON, memory_bank)

    @staticmethod
    def _try_import_omx():
        try:
            from omxplayer.player import OMXPlayer
            return True
        except:
            return False







