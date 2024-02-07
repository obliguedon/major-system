from kivy.config import Config

Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '700')

import kivy
kivy.require('1.10.0')
  
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
  
import finder as fnd
import yaml
import logging

# Inherit Kivy's App class which represents the window
# for our widgets
# MyApp inherits all the fields and methods
# from Kivy
class MyApp(App):
  
    # This returns the content we want in the window
    def build(self):
        with open('./src/etc/default_settings.yml', 'r') as stream:
            try:
            # Converts yaml document to python object
                self.settings=yaml.safe_load(stream)
            # Printing dictionary
                logging.info(self.settings)
            except yaml.YAMLError as e:
                print(e)
        self.appLayout = ScreenManager()

        # ==================================================================
        # MENU SCREEN
        menuScreen = Screen(name = 'Menu')

        menuLayout = GridLayout(cols=1, rows=3, spacing=10)

        settings_btn = Button(text="...",
                              font_size = 16,
                              size_hint_y = None,
                              size_hint_x = None,
                              height = 30,
                              width = 30,
                              on_press = self.go_to_settings)
        settings_btn_placed = AnchorLayout(size_hint_y = None,
                                           height = settings_btn.height,
                                           anchor_x = "right")
        settings_btn_placed.add_widget(settings_btn)

        # Adding the text input 
        num_str = TextInput(font_size = 13,
                                 size_hint_y = None,
                                 size_hint_x = None,
                                 height = 30,
                                 width = 100,
                                 multiline = False,
                                 input_filter='int',
                                 halign = 'center',
                                 use_handles = False,
                                 hint_text = "a number")
        num_str.bind(text = self.update)
        num_str_centered = AnchorLayout(size_hint_y = None, height=num_str.height)
        num_str_centered.add_widget(num_str)

        word_list = ScrollView(do_scroll_x = False, do_scroll_y = True)

        self.label = Label(text = "await input", size_hint_y = None, font_size = 13)
        self.label.texture_update()
        self.label.height = self.label.texture_size[1]
        word_list.add_widget(self.label)

        menuLayout.add_widget(settings_btn_placed)
        menuLayout.add_widget(num_str_centered)
        menuLayout.add_widget(word_list)
        
        menuScreen.add_widget(menuLayout)

        # ==================================================================
        # SETTINGS SCREEN
        settingScreen = Screen(name = 'Settings')

        settingsLayout = GridLayout(cols=1, rows=3, spacing=10)

        menu_btn = Button(text="<=",
                              font_size = 16,
                              size_hint_y = None,
                              size_hint_x = None,
                              height = 30,
                              width = 30,
                              on_press = self.go_to_menu)
        menu_btn_placed = AnchorLayout(size_hint_y = None,
                                       height = menu_btn.height,
                                       anchor_x = "left")
        menu_btn_placed.add_widget(menu_btn)

        settingsLayout.add_widget(menu_btn_placed)

        settingScreen.add_widget(settingsLayout)

        # ==================================================================
        # APP SCREENS

        self.appLayout.add_widget(menuScreen)
        self.appLayout.add_widget(settingScreen)
        self.appLayout.current = 'Menu'

        self.update(obj=None, text='')

        return self.appLayout
    
    def update(self, obj, text):
        file_dir = f"{self.settings['dict_path']}/{self.settings['lang']}.csv"

        logging.info(f"symbols = {self.settings['symbols'][self.settings['lang']]}")

        symbols = self.settings['symbols'][self.settings['lang']]

        data = fnd.Finder(file_dir, symbols)

        filtered_data = data.get_matches(text)

        my_label = ""
        for word in filtered_data['alphabet']:
            my_label += f"{word}\n"

        self.label.text = my_label
        self.label.texture_update()
        self.label.height = self.label.texture_size[1]

    def go_to_settings(self, obj):
        self.appLayout.transition.direction = 'right'
        self.appLayout.current = 'Settings'

    def go_to_menu(self, obj):
        self.appLayout.transition.direction = 'left'
        self.appLayout.current = 'Menu'
  
if __name__ == '__main__':
    MyApp().run()