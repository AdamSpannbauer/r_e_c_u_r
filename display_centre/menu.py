import os

class Menu(object):
    def __init__(self, data, menu_height):
        self.data = data        
        self.open_folders = []
        self.menu_list = []
        self.menu_height = menu_height
        self.top_menu_index = 0

        self.selected_list_index = 0
    
    def navigate_menu_up(self):
        if self.selected_list_index != 0:
            if self.selected_list_index == self.top_menu_index:
                self.top_menu_index -= 1
            self.selected_list_index -= 1
        else:
            last_list_index = len(self.menu_list) - 1
            self.selected_list_index = last_list_index
            self.top_menu_index = last_list_index - (self.menu_height - 1)
            if self.top_menu_index < 0:
                self.top_menu_index = 0

    def navigate_menu_down(self):
        last_list_index = len(self.menu_list) - 1
        if self.selected_list_index != last_list_index:
            bot_menu_index = self.top_menu_index + self.menu_height - 1
            if self.selected_list_index == bot_menu_index:
                self.top_menu_index += 1
            self.selected_list_index += 1
        else:
            self.top_menu_index = 0
            self.selected_list_index = self.top_menu_index
        
    def update_open_folders(self, folder_name):
        if folder_name not in self.open_folders:
            self.open_folders.append(folder_name)
        else:
            self.open_folders.remove(folder_name)
    
    def _check_folder_state(self, folder_name):
        ######## used for displaying folders as open or closed ########
        if folder_name in self.open_folders:
            return True, '/'
        else:
            return False, '|'
 
    def generate_browser_list(self):
        ######## starts the recursive process of listing all folders and video files to display ########
        self.browser_list = []
        for path in PATHS_TO_BROWSER:
            self._add_folder_to_browser_list(path, 0)
        
        for browser_line in self.browser_list:
            is_file, name = self.extract_file_type_and_name_from_browser_format(browser_line['name'])
            if is_file:
                is_slotted, bankslot_number = self._is_file_in_memory_bank(name)
                if is_slotted:
                    browser_line['slot'] = bankslot_number
        
    def generate_settings_list(self):
        self.settings_list = []
        for sub_setting in self.settings.keys():
            if sub_setting in self.settings_open_folders:
                self.settings_list.append(dict(name=sub_setting + '/', value=''))
                for setting in self.settings[sub_setting]:
                    setting_value = self.make_empty_if_none(self.settings[sub_setting][setting]['value'])
                    self.settings_list.append(dict(name=' ' + setting, value=setting_value))
            else:   
                self.settings_list.append(dict(name=sub_setting + '|', value=''))

    @staticmethod
    def extract_file_type_and_name_from_menu_format(dir_name):
        # removes whitespace and folder state from display item ########
        if dir_name.endswith('|') or dir_name.endswith('/'):
            return False, dir_name.lstrip()[:-1]
        else:
            return True, dir_name.lstrip()

class BrowserMenu(Menu):    
    def __init__(self, data, menu_height):
        Menu.__init__(self, data, menu_height)
        self.generate_browser_list()

    def generate_browser_list(self):
        ######## starts the recursive process of listing all folders and video files to display ########
        self.menu_list = []
        for path in self.data.PATHS_TO_BROWSER:
            self._add_folder_to_browser_list(path, 0)
        
        for browser_line in self.menu_list:
            is_file, name = self.extract_file_type_and_name_from_menu_format(browser_line['name'])
            if is_file:
                is_slotted, bankslot_number = self._is_file_in_bank_data(name)
                if is_slotted:
                    browser_line['slot'] = bankslot_number

    def _add_folder_to_browser_list(self, current_path, current_level):
        ######## adds the folders and mp4 files at the current level to the results list. recursively recalls at deeper level if folder is open ########
        # TODO make note of / investigate what happens with multiple folders of same name
        root, dirs, files = next(os.walk(current_path))

        indent = ' ' * 4 * (current_level)
        for folder in dirs:
            is_open, char = self._check_folder_state(folder)
            self.menu_list.append(dict(name='{}{}{}'.format(indent, folder, char), slot='x'))
            if (is_open):
                next_path = '{}/{}'.format(root, folder)
                next_level = current_level + 1
                self._add_folder_to_browser_list(next_path, next_level)

        for f in files:
            split_name = os.path.splitext(f)
            if (split_name[1] in ['.mp4', '.mkv', '.avi', '.mov']):
                self.menu_list.append(dict(name='{}{}'.format(indent, f), slot='-'))

    def _is_file_in_bank_data(self, file_name):
        ######## used for displaying the mappings in browser view ########
        for bank_index, bank in enumerate(self.data.bank_data):
            for slot_index, slot in enumerate(bank):
                if file_name == slot['name']:
                    return True, '{}-{}'.format(bank_index,slot_index)
        return False, ''
        

    def enter_on_browser_selection(self):
        is_file, name = self.extract_file_type_and_name_from_menu_format(
            self.menu_list[self.selected_list_index]['name'])
        if is_file:
            is_successful = self.data.create_new_slot_mapping_in_first_open(name)
            if not is_successful:
                self.message_handler.set_message('INFO', 'current bank is full')
        else:
            self.update_open_folders(name)
        self.generate_browser_list()


class SettingsMenu(Menu):
    def __init__(self, data, menu_height):
        Menu.__init__(self, data, menu_height)
        self.generate_settings_list()

    def generate_settings_list(self):
        self.menu_list = []
        for setting_folder_key, setting_folder_item in self.data.settings.items():
            if setting_folder_key in self.open_folders:
                self.menu_list.append(dict(name='{}/'.format(setting_folder_key), value=''))
                for setting_key, setting_details in setting_folder_item.items(): 
                    self.menu_list.append(dict(name='   {}'.format(setting_key), value=self.data.make_empty_if_none(setting_details['value'])))
            else:   
                self.menu_list.append(dict(name='{}|'.format(setting_folder_key), value=''))

    def enter_on_setting_selection(self):
        is_file, name = self.extract_file_type_and_name_from_menu_format(
            self.menu_list[self.selected_list_index]['name'])
        if is_file:
            return True, self.data.return_setting_details(name)
        else:
            self.update_open_folders(name)
            self.generate_settings_list()
            return False, ''
        




